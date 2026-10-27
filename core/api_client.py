"""
Client HTTP untuk menghubungkan Streamlit Frontend ke FastAPI Backend.
Menangani request multipart, cek status server, dan parsing respons JSON.
"""

import time
from urllib.parse import urlparse
import requests

DEFAULT_API_URL = "http://127.0.0.1:8000/api/v1/predict"
DEFAULT_TIMEOUT = 10


def check_api_health(api_url: str = DEFAULT_API_URL):
    """Cek apakah backend FastAPI aktif dan model sudah siap dimuat."""
    if not api_url:
        return False, "URL API kosong."

    # Ambil base URL (misal: http://127.0.0.1:8000) lalu arahkan ke /health
    parsed = urlparse(api_url)
    health_url = f"{parsed.scheme}://{parsed.netloc}/health"

    try:
        resp = requests.get(health_url, timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            # Pastikan model_loaded bernilai True pada respon /health
            if data.get("model_loaded") is True:
                return True, "FastAPI & Model MobileNetV2 Siap"
            return False, "Server aktif, tetapi file model .keras belum dipasang"
        return False, f"Server aktif namun merespons kode status {resp.status_code}"
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        # Terjadi saat server FastAPI belum dijalankan
        return False, "Server FastAPI belum dijalankan (Offline)"
    except Exception as e:
        return False, f"Gagal menghubungi server: {str(e)}"


def predict_via_api(image_bytes: bytes, filename: str = "image.jpg", api_url: str = DEFAULT_API_URL, timeout: int = DEFAULT_TIMEOUT) -> dict:
    """Kirim gambar via HTTP POST multipart ke endpoint /api/v1/predict."""
    start_time = time.perf_counter()

    # Bungkus byte gambar ke format multipart/form-data
    files = {
        "file": (filename, image_bytes, "image/jpeg")
    }

    try:
        # Kirim request POST ke endpoint FastAPI
        resp = requests.post(api_url, files=files, timeout=timeout)
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "error_type": "TIMEOUT",
            "message": f"Server API ({api_url}) tidak merespons dalam {timeout} detik.",
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 1)
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "error_type": "CONNECTION_REFUSED",
            "message": f"Koneksi ditolak ke {api_url}. Pastikan server backend FastAPI sudah dijalankan.",
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 1)
        }
    except Exception as e:
        return {
            "status": "error",
            "error_type": "REQUEST_FAILED",
            "message": f"Gagal menghubungi API: {str(e)}",
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 1)
        }

    latency_ms = round((time.perf_counter() - start_time) * 1000, 1)

    # Tangani kode status HTTP error (seperti 400, 500, 503)
    if resp.status_code != 200:
        try:
            err_data = resp.json()
            detail = err_data.get("detail", resp.text)
        except Exception:
            detail = resp.text[:200]
        return {
            "status": "error",
            "error_type": f"HTTP_{resp.status_code}",
            "message": f"Server mengembalikan kesalahan (HTTP {resp.status_code}): {detail}",
            "latency_ms": latency_ms,
            "raw_api_response": resp.text
        }

    # Parsing respon JSON dari backend
    try:
        data = resp.json()
    except Exception:
        return {
            "status": "error",
            "error_type": "INVALID_JSON",
            "message": "Respons server bukan format JSON yang valid.",
            "latency_ms": latency_ms,
            "raw_api_response": resp.text
        }

    # Sinkronisasi properti 'top_class_id' agar kompatibel dengan render UI
    data["top_class_id"] = data.get("label", data.get("top_class_id", ""))
    return data
