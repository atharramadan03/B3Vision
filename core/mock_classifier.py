"""
Simulator Inferensi Deterministik (Mock Fallback Engine untuk 7 Kelas Dataset)
Memberikan simulasi prediksi yang realistis dan konsisten untuk 7 kelas limbah
sebelum model pelatihan .keras diekspor dari Google Colab.
"""

import hashlib
from config.settings import CONFIDENCE_THRESHOLD, CLASSES

CLASS_KEYS = ["battery", "brown-glass", "green-glass", "metal", "plastic", "trash", "white-glass"]

def predict_mock(display_image, filename=""):
    """
    Menghasilkan simulasi probabilitas klasifikasi deterministik untuk 7 kelas limbah.
    
    Args:
        display_image (PIL.Image): Objek gambar input
        filename (str): Nama berkas input
        
    Returns:
        dict: Hasil klasifikasi lengkap
    """
    fname = filename.lower()
    
    # 1. Deteksi spesifik berdasarkan nama sampel
    if "battery" in fname or "baterai" in fname:
        top_key = "battery"
        conf = 0.942
    elif "brown-glass" in fname or "kaca-cokelat" in fname:
        top_key = "brown-glass"
        conf = 0.915
    elif "green-glass" in fname or "kaca-hijau" in fname:
        top_key = "green-glass"
        conf = 0.898
    elif "metal" in fname or "kaleng" in fname:
        top_key = "metal"
        conf = 0.927
    elif "plastic" in fname or "plastik" in fname:
        top_key = "plastic"
        conf = 0.954
    elif "trash" in fname or "masker" in fname:
        top_key = "trash"
        conf = 0.908
    elif "white-glass" in fname or "lampu" in fname or "bohlam" in fname:
        top_key = "white-glass"
        conf = 0.931
    elif "blur" in fname or "uncertain" in fname:
        # Skenario Confidence Rendah (< 60%)
        top_key = "plastic"
        conf = 0.472
    else:
        # Citra acak: gunakan SHA-256 hash deterministik
        img_bytes = display_image.tobytes()
        digest = hashlib.sha256(img_bytes).hexdigest()
        hash_val = int(digest[:8], 16)
        
        top_idx = hash_val % len(CLASS_KEYS)
        top_key = CLASS_KEYS[top_idx]
        conf = round(0.78 + ((hash_val % 180) / 1000.0), 3)

    # Bangun distribusi probabilitas 7 kelas
    remaining = 1.0 - conf
    other_keys = [k for k in CLASS_KEYS if k != top_key]
    
    # Alokasikan sisa probabilitas ke kelas lainnya
    probabilities = {top_key: conf}
    weights = [0.35, 0.25, 0.15, 0.12, 0.08, 0.05]
    for idx, ok in enumerate(other_keys):
        probabilities[ok] = round(remaining * weights[idx], 4)
        
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
        "is_mock": True,
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
