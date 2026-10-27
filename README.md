# B3Vision • Klasifikasi Limbah B3 Menggunakan MobileNetV2

Aplikasi cerdas berbasis arsitektur **Client-Server (FastAPI Backend + Streamlit Frontend)** untuk mengklasifikasikan citra limbah ke dalam **7 kelas spesifik** (*6 kelas Limbah B3 & 1 kelas Non-B3*) menggunakan model **Transfer Learning MobileNetV2**, lengkap dengan visualisasi tingkat keyakinan dan panduan SOP penanganan yang aman dan bertanggung jawab.

---

## 🚀 Fitur Utama
1. **Client-Server REST API Murni:**
   - ⚡ **Backend FastAPI Terdedikasi:** Menangani pemrosesan citra, inferensi MobileNetV2, dan pencatatan latensi middleware (`X-Process-Time-Ms`).
   - 🌐 **Frontend Streamlit Ringan:** Bebas dari dependensi TensorFlow, berkomunikasi murni via HTTP POST ke endpoint `POST /api/v1/predict`.
   - 🔒 **Tanpa Auto-Analisis:** Analisis hanya dijalankan saat tombol `🔍 Analisis` diklik oleh pengguna.
2. **Antarmuka Modern & Bersih:**
   - Navigasi atas berbasis *segmented pill tabs* (`🏠 Beranda`, `🔍 Analisis`, `ℹ️ About`) tanpa sidebar.
   - Desain responsif bertema *Emerald Green* modern.
   - Status badge indikator server backend real-time.
3. **Pilihan Input Fleksibel:**
   - 📁 **Unggah Citra:** Berkas JPG, JPEG, PNG, WEBP dari perangkat.
   - 📸 **Kamera Langsung:** Pemotretan langsung dari webcam atau kamera smartphone.
4. **Diagnosa & SOP Penanganan:**
   - Status semantik jelas (🔴 **Limbah B3 (Berbahaya)**, 🟢 **Non-B3**, 🟡 **Kurang Yakin / Perlu Foto Ulang**).
   - Indikator bar tingkat keyakinan (*Confidence Score*).
   - Rekomendasi tindakan yang dianjurkan (✓) dan dilarang keras (✕).

---

## 🛠️ Cara Menjalankan Aplikasi

Jalankan aplikasi dengan **dua terminal terpisah**:

### Terminal 1 — Backend FastAPI
```bash
uvicorn app.main:app --reload --port 8000
```
Server FastAPI akan aktif di `http://127.0.0.1:8000`. Dokumentasi interaktif Swagger API dapat diakses di `http://127.0.0.1:8000/docs`.

### Terminal 2 — Frontend Streamlit
```bash
streamlit run app.py
```
Aplikasi Streamlit akan terbuka pada alamat: `http://localhost:8501`.

---

## 📁 Struktur Direktori
```
Klasifikasi_limbahB3/
├── app.py                         # Entry point & controller navigasi Streamlit
├── requirements.txt               # Dependensi proyek (Streamlit, FastAPI, Uvicorn, dll.)
├── rancangan_aplikasi_b3vision.md # Dokumen spesifikasi sistem lengkap
│
├── app/                           # Backend REST API Package (FastAPI)
│   ├── __init__.py                # Package identifier
│   ├── main.py                    # Aplikasi FastAPI, CORS, middleware, & router
│   ├── schemas.py                 # Pydantic Schemas (HealthResponse & PredictionResponse)
│   └── model_service.py           # TensorFlow MobileNetV2 model loader & inference engine
│
├── .streamlit/                    # Konfigurasi Streamlit
│   └── config.toml                # Tema Emerald (#059669) & pengaturan antarmuka
│
├── config/                        # Konfigurasi kelas, ambang batas, & SOP
│   └── settings.py
│
├── core/                          # Komponen pendukung sistem
│   ├── api_client.py              # HTTP client REST API (check_api_health & predict_via_api)
│   └── preprocessor.py            # Pemrosesan citra (resize 224x224 px & tensor format)
│
├── ui/                            # Modul antarmuka Streamlit (Navbar atas tanpa sidebar)
│   ├── styles.py                  # Custom CSS (pills navbar, cards, badges semantik)
│   ├── views_home.py              # Halaman Beranda (hero tagline & 4 langkah cara kerja)
│   ├── views_predict.py           # Halaman Analisis (unggah berkas, live camera, & hasil SOP)
│   └── views_about.py             # Halaman About (deskripsi, taksonomi 7 kelas, info model)
│
├── dataset/                       # Folder dataset lokal (5.287 citra dalam 7 subfolder kelas)
└── models/                        # Tempat penyimpanan file bobot model (.keras)
    └── mobilenetv2_limbah_b3.keras
```
