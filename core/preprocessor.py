"""
Modul Preprocessing Citra untuk MobileNetV2
Mengubah citra input menjadi format tensor 224x224 RGB terstandarisasi.
"""

from PIL import Image
import numpy as np

TARGET_SIZE = (224, 224)

def load_and_preprocess_image(image_input):
    """
    Memuat dan melakukan normalisasi citra untuk inferensi MobileNetV2.
    
    Args:
        image_input: Dapat berupa file-like object (BytesIO), path file, atau objek PIL.Image
        
    Returns:
        tuple: (pil_display_image, preprocessed_numpy_array)
    """
    if isinstance(image_input, Image.Image):
        img = image_input.copy()
    else:
        img = Image.open(image_input)
    
    # Konversi ke mode RGB (menghilangkan channel alpha jika PNG)
    if img.mode != "RGB":
        img = img.convert("RGB")
    
    # Buat salinan untuk display pratinjau UI
    display_image = img.copy()
    
    # Resize citra ke resolusi target 224x224 dengan resampling beresolusi tinggi
    resized_img = img.resize(TARGET_SIZE, Image.Resampling.BILINEAR)
    
    # Konversi ke NumPy array bertipe float32 (rentang piksel mentah 0–255).
    # Catatan: model hasil training sudah memuat layer resmi
    # layers.Rescaling(1./127.5, offset=-1.0, name="mobilenetv2_rescaling") di dalam arsitekturnya,
    # sehingga array tetap dibiarkan pada rentang [0, 255] agar tidak terjadi normalisasi ganda.
    img_array = np.array(resized_img, dtype=np.float32)
    
    # Tambahkan dimensi batch: (1, 224, 224, 3)
    batch_array = np.expand_dims(img_array, axis=0)
    
    return display_image, batch_array
