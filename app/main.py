"""
Entry point REST API FastAPI untuk inferensi klasifikasi limbah B3.
Menyediakan endpoint pengecekan status (/health) dan prediksi (/api/v1/predict).
"""

from time import perf_counter
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from config.settings import APP_TITLE, APP_VERSION, CLASSES
from .schemas import HealthResponse, PredictionResponse
from .model_service import predict_image_bytes, is_model_ready, MODEL_VERSION

# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title=f"{APP_TITLE} API",
    description="REST API Klasifikasi Jenis Limbah B3 Menggunakan Transfer Learning MobileNetV2",
    version=APP_VERSION,
)

# Konfigurasi CORS agar frontend Streamlit atau client lain dapat mengakses API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time(request: Request, call_next):
    """Middleware untuk mengukur latensi pemrosesan request dalam milidetik."""
    start = perf_counter()
    response = await call_next(request)
    elapsed_ms = (perf_counter() - start) * 1000
    # Sisipkan header durasi proses pada HTTP response
    response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.2f}"
    return response


@app.get("/health", response_model=HealthResponse)
def health():
    """Endpoint health check untuk memverifikasi kesiapan server dan model."""
    return HealthResponse(
        status="ok" if is_model_ready() else "model_missing",
        model_loaded=is_model_ready(),
        model_version=MODEL_VERSION,
        total_classes=len(CLASSES),
    )


@app.post("/api/v1/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    """Endpoint utama inferensi citra limbah menggunakan MobileNetV2."""
    # 1. Pastikan model deep learning sudah siap
    if not is_model_ready():
        raise HTTPException(
            status_code=503,
            detail="Model 'models/mobilenetv2_limbah_b3.keras' belum terpasang atau gagal dimuat di server.",
        )

    # 2. Validasi ekstensi berkas citra
    if not file.filename or not file.filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        raise HTTPException(
            status_code=400,
            detail="Format berkas harus JPG, JPEG, PNG, atau WEBP.",
        )

    # 3. Baca data biner berkas yang diunggah
    try:
        image_bytes = await file.read()
        if not image_bytes:
            raise ValueError("Berkas gambar kosong.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Gagal membaca citra: {str(e)}")

    # 4. Jalankan inferensi MobileNetV2 dan mapping SOP
    try:
        result = predict_image_bytes(image_bytes, filename=file.filename)
        return PredictionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kesalahan inferensi server: {str(e)}")
