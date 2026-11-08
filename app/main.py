# REST API FastAPI untuk inferensi klasifikasi limbah

from time import perf_counter
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from config.settings import APP_TITLE, APP_VERSION, CLASSES
from .schemas import HealthResponse, PredictionResponse
from .model_service import predict_image_bytes, is_model_ready, MODEL_VERSION

app = FastAPI(
    title=f"{APP_TITLE} API",
    description="REST API Klasifikasi Jenis Limbah B3 Menggunakan Transfer Learning MobileNetV2",
    version=APP_VERSION,
)

# Konfigurasi CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time(request: Request, call_next):
    # Hitung waktu pemrosesan request
    start = perf_counter()
    response = await call_next(request)
    elapsed_ms = (perf_counter() - start) * 1000
    response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.2f}"
    return response


@app.get("/health", response_model=HealthResponse)
def health():
    # Pengecekan status server dan kesiapan model
    return HealthResponse(
        status="ok" if is_model_ready() else "model_missing",
        model_loaded=is_model_ready(),
        model_version=MODEL_VERSION,
        total_classes=len(CLASSES),
    )


@app.post("/api/v1/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    # Validasi kesiapan model
    if not is_model_ready():
        raise HTTPException(
            status_code=503,
            detail="Model 'models/mobilenetv2_limbah_b3.keras' belum terpasang atau gagal dimuat di server.",
        )

    # Validasi ekstensi berkas
    if not file.filename or not file.filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        raise HTTPException(
            status_code=400,
            detail="Format berkas harus JPG, JPEG, PNG, atau WEBP.",
        )

    # Baca byte data gambar
    try:
        image_bytes = await file.read()
        if not image_bytes:
            raise ValueError("Berkas gambar kosong.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Gagal membaca citra: {str(e)}")

    # Jalankan inferensi model
    try:
        result = predict_image_bytes(image_bytes, filename=file.filename)
        return PredictionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kesalahan inferensi server: {str(e)}")
