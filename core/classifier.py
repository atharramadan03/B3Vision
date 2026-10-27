"""
Engine Utama Klasifikasi Visi Komputer (Multi-Source Inference)
Mendukung 3 sumber inferensi:
1. REST API Server (FastAPI / Flask / Colab Ngrok / Cloud Endpoint)
2. Model Fisik Lokal TensorFlow/Keras (@st.cache_resource)
3. Smart Mock Fallback Engine (Simulasi Deterministik)
"""

import os
import io
import time
import streamlit as st
import numpy as np
from config.settings import CONFIDENCE_THRESHOLD, CLASSES
from core.mock_classifier import predict_mock
from core.api_client import predict_via_api, check_api_health

MODEL_PATH = os.path.join("models", "mobilenetv2_limbah_b3.keras")
CLASS_KEYS = ["battery", "brown-glass", "green-glass", "metal", "plastic", "trash", "white-glass"]

@st.cache_resource(show_spinner=False)
def get_model():
    """
    Memuat model TensorFlow/Keras dari disk lokal dan menyimpannya di memori via Streamlit cache.
    Mengembalikan None jika file bobot model belum ditemukan.
    """
    if not os.path.exists(MODEL_PATH):
        return None
    
    try:
        import tensorflow as tf
        model = tf.keras.models.load_model(MODEL_PATH)
        return model
    except Exception as e:
        print(f"Peringatan: Gagal memuat model fisik ({e}), beralih ke Mock Engine.")
        return None

def is_real_model_available():
    """Memeriksa apakah model deep learning fisik lokal siap digunakan."""
    return get_model() is not None

def predict_waste(display_image, preprocessed_batch, filename="image.jpg", 
                  engine_mode="AUTO", api_url="http://localhost:8000/predict"):
    """
    Menjalankan inferensi pada citra limbah dengan rute multi-engine.
    
    Args:
        display_image (PIL.Image): Citra PIL asli
        preprocessed_batch (np.ndarray): Tensor batch (1, 224, 224, 3)
        filename (str): Nama file citra input
        engine_mode (str): 'AUTO', 'API', 'LOCAL', atau 'MOCK'
        api_url (str): URL endpoint API REST
        
    Returns:
        dict: Hasil klasifikasi terstruktur lengkap
    """
    start_time = time.perf_counter()

    # Siapkan byte gambar untuk pengiriman API jika diperlukan
    img_byte_arr = io.BytesIO()
    display_image.save(img_byte_arr, format='JPEG')
    image_bytes = img_byte_arr.getvalue()

    # 1. Jalur API Server
    if engine_mode in ["API", "AUTO"] and api_url:
        api_res = predict_via_api(image_bytes, filename=filename, api_url=api_url,
                                  timeout=10 if engine_mode == "API" else 5)
        if api_res.get("status") == "success":
            api_res["source"] = "API_SERVER"
            return api_res
        elif engine_mode == "API":
            return api_res

    # 2. Jalur Model Fisik Lokal (.keras)
    model = get_model()
    if model is not None and engine_mode in ["LOCAL", "AUTO"]:
        try:
            preds = model.predict(preprocessed_batch, verbose=0)[0]
            latency_ms = round((time.perf_counter() - start_time) * 1000, 1)

            probabilities = {}
            for idx, key in enumerate(CLASS_KEYS):
                probabilities[key] = float(preds[idx]) if idx < len(preds) else 0.0

            sorted_probs = sorted(probabilities.items(), key=lambda item: item[1], reverse=True)
            top_class_id, top_confidence = sorted_probs[0]

            is_confident = top_confidence >= CONFIDENCE_THRESHOLD
            class_meta = CLASSES.get(top_class_id, {})
            category = class_meta.get("category", "B3")

            if not is_confident:
                status_state = "UNCERTAIN"
            elif category == "B3":
                status_state = "B3_HAZARDOUS"
            else:
                status_state = "NON_B3_SAFE"

            distribution_results = [
                {
                    "class_id": cid,
                    "name": CLASSES[cid]["short_name"],
                    "full_name": CLASSES[cid]["name"],
                    "category": CLASSES[cid]["category"],
                    "confidence": round(prob * 100, 2),
                    "ratio": prob
                }
                for cid, prob in sorted_probs
            ]

            return {
                "status": "success",
                "source": "LOCAL_MODEL",
                "latency_ms": latency_ms,
                "is_mock": False,
                "status_state": status_state,
                "is_confident": is_confident,
                "top_class_id": top_class_id,
                "class_name": class_meta.get("name", "Tidak Dikenal"),
                "short_name": class_meta.get("short_name", "Tidak Dikenal"),
                "category": category,
                "confidence": round(top_confidence * 100, 2),
                "confidence_ratio": top_confidence,
                "hazard_level": class_meta.get("hazard_level", "Sedang"),
                "top_3": distribution_results[:3],
                "distribution": distribution_results,
                "sop_actions": class_meta.get("sop_actions", []),
                "prohibitions": class_meta.get("prohibitions", []),
                "description": class_meta.get("description", ""),
                "environmental_impact": class_meta.get("environmental_impact", "")
            }
        except Exception as e:
            print(f"Error inferensi model lokal: {e}. Menggunakan fallback.")

    # 3. Jalur Fallback: Smart Mock Engine
    mock_res = predict_mock(display_image, filename=filename)
    mock_res["source"] = "SMART_MOCK"
    mock_res["latency_ms"] = round((time.perf_counter() - start_time) * 1000, 1)
    return mock_res
