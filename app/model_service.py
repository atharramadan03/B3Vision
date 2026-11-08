# Layanan inferensi model MobileNetV2

import io
import json
import time
from pathlib import Path
from PIL import Image

try:
    import tensorflow as tf
except ImportError:
    tf = None

from core.preprocessor import load_and_preprocess_image
from config.settings import CLASSES, CONFIDENCE_THRESHOLD

MODEL_PATH = Path("models/mobilenetv2_limbah_b3.keras")
CLASS_NAMES_PATH = Path("models/class_names.json")
MODEL_VERSION = "v2.0-mobilenetv2-12class"

# Daftar kelas default
CLASS_KEYS = [
    "battery", "biological", "brown-glass", "cardboard", "clothes",
    "green-glass", "metal", "paper", "plastic", "shoes", "trash", "white-glass"
]

if CLASS_NAMES_PATH.exists():
    try:
        with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
            CLASS_KEYS = json.load(f)
        print(f"[SUCCESS] Daftar {len(CLASS_KEYS)} kelas dimuat dari {CLASS_NAMES_PATH}")
    except Exception as e:
        print(f"[WARN] Gagal membaca {CLASS_NAMES_PATH}, menggunakan default 12 kelas: {e}")

# Load model saat inisialisasi
model = None
if MODEL_PATH.exists() and tf is not None:
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        print(f"[SUCCESS] Model berhasil dimuat dari {MODEL_PATH} (Output: {model.output_shape})")
    except Exception as e:
        print(f"[ERROR] Gagal memuat model dari {MODEL_PATH}: {e}")
        model = None
elif not MODEL_PATH.exists():
    print(f"[WARN] File model belum ditemukan di {MODEL_PATH}")
else:
    print("[WARN] Modul TensorFlow belum terpasang di environment ini.")


def is_model_ready() -> bool:
    # Cek kesiapan model
    return model is not None


def predict_image_bytes(image_bytes: bytes, filename: str = "upload.jpg") -> dict:
    # Inferensi citra dan mapping hasil ke kelas limbah
    if model is None:
        raise RuntimeError(f"Model belum terpasang di '{MODEL_PATH}'. Pastikan file mobilenetv2_limbah_b3.keras sudah ada dan dependensi TensorFlow tersedia.")

    start_time = time.perf_counter()

    # Preprocessing citra menjadi resolusi target (224x224x3)
    pil_image = Image.open(io.BytesIO(image_bytes))
    _, preprocessed_batch = load_and_preprocess_image(pil_image)

    # Inferensi probabilitas untuk ke-12 kelas
    preds = model.predict(preprocessed_batch, verbose=0)[0]
    probabilities = {CLASS_KEYS[i]: round(float(preds[i]), 4) for i in range(len(CLASS_KEYS))}
    sorted_probs = sorted(probabilities.items(), key=lambda item: item[1], reverse=True)
    top_label, top_score = sorted_probs[0]

    # Evaluasi ambang batas keyakinan (confidence threshold)
    is_confident = top_score >= CONFIDENCE_THRESHOLD
    class_meta = CLASSES.get(top_label, {})
    category = class_meta.get("category", "B3")

    # Tentukan state semantik
    if not is_confident:
        status_state = "UNCERTAIN"
    elif category == "B3":
        status_state = "B3_HAZARDOUS"
    else:
        status_state = "NON_B3_SAFE"

    # Bentuk daftar distribusi probabilitas terurut
    distribution = [
        {
            "class_id": cid,
            "name": CLASSES.get(cid, {}).get("short_name", cid),
            "full_name": CLASSES.get(cid, {}).get("name", cid),
            "category": CLASSES.get(cid, {}).get("category", "Non-B3"),
            "confidence": round(prob * 100, 2),
            "ratio": prob,
        }
        for cid, prob in sorted_probs
    ]

    latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

    # Kembalikan payload lengkap yang sesuai dengan schema PredictionResponse
    return {
        "status": "success",
        "filename": filename,
        "label": top_label,
        "class_name": class_meta.get("name", top_label),
        "short_name": class_meta.get("short_name", top_label),
        "category": category,
        "hazard_level": class_meta.get("hazard_level", "Tinggi"),
        "score": round(float(top_score), 4),
        "confidence": round(float(top_score) * 100, 2),
        "is_confident": is_confident,
        "status_state": status_state,
        "model_version": MODEL_VERSION,
        "latency_ms": latency_ms,
        "probabilities": probabilities,
        "distribution": distribution,
        "description": class_meta.get("description", ""),
        "environmental_impact": class_meta.get("environmental_impact", ""),
        "sop_actions": class_meta.get("sop_actions", []),
        "prohibitions": class_meta.get("prohibitions", []),
    }
