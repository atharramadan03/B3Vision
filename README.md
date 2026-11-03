# B3Vision: Sistem Klasifikasi Limbah B3 Menggunakan MobileNetV2

B3Vision adalah sistem cerdas klasifikasi citra berbasis arsitektur **Client-Server (FastAPI Backend + Streamlit Frontend)** yang dirancang untuk mengidentifikasi kategori limbah ke dalam **12 kelas** (*6 kelas Limbah B3 dan 6 kelas Non-B3/Daur Ulang*). Sistem ini mengintegrasikan model deep learning **Transfer Learning & Fine-Tuning MobileNetV2** dengan sistem pakar berbasis regulasi K3 untuk memberikan rekomendasi Standard Operating Procedure (SOP) penanganan limbah secara real-time.

Proyek ini dikembangkan sebagai penelitian Tugas Akhir pada bidang Computer Vision dan Sistem Rekayasa Perangkat Lunak Berbasis Kecerdasan Buatan.

---

## 1. Informasi Dataset & Lisensi

Dataset yang digunakan dalam pelatihan model B3Vision bersumber dari repositori publik Kaggle yang disusun oleh Mostafa Abla:

* **Nama Dataset**: *Garbage Classification (12 classes)*
* **Penyusun / Kurator**: Mostafa Abla
* **Tautan Sumber Kaggle**: [https://www.kaggle.com/datasets/mostafaabla/garbage-classification](https://www.kaggle.com/datasets/mostafaabla/garbage-classification)
* **Lisensi Resmi**: **[Open Database License (ODbL) v1.0](http://opendatacommons.org/licenses/odbl/1.0/)**
  * *Ketentuan Lisensi*: `Database: Open Database, Contents: © Original Authors`.
  * *Pemanfaatan*: Diizinkan untuk dibagikan (*Share*), diadaptasi/dimodifikasi (*Create*), dan digunakan secara terbuka untuk tujuan penelitian (*Research & Academic Education*) non-profit dengan mencantumkan atribusi kepada pemilik/fotografer asli.
* **Volume Citra**:
  * Disebutkan pada deskripsi awal sekitar 15.150 citra, dan pada rilis dataset terverifikasi yang diekstrak pada lingkungan sistem ini terdapat **15.515 citra** berformat JPG/PNG/WEBP yang terbagi ke dalam 12 kelas seimbang.

### Sumber Perolehan Data (Acknowledgements):
Berdasarkan dokumentasi resmi penyusun dataset:
1. **Kategori Pakaian (`clothes`) & 22% Kategori Sepatu (`shoes`)**: Diperoleh dari dataset publik *Clothing Dataset Full* oleh Alexey Grigorev ([Kaggle Clothing Dataset](https://www.kaggle.com/agrigorev/clothing-dataset-full)).
2. **Sekitar 29% dari 9 Kategori Lainnya**: Diambil dari *Garbage Classification Dataset* dasar oleh Gary Thung & Mindy Yang ([Kaggle Garbage Classification](https://www.kaggle.com/asdasdasasdas/garbage-classification)).
3. **Sisa Citra Lainnya**: Dikumpulkan melalui teknik *Web Scraping* terarah untuk mengumpulkan foto limbah dunia nyata (misal: sayuran busuk dan sisa makanan untuk kategori `biological`, botol kaca dan kaleng aerosol untuk kategori limbah lainnya). Seluruh hak cipta foto dimiliki oleh masing-masing fotografer/pemilik asli dan digunakan khusus untuk pengembangan riset kecerdasan buatan lingkungan.

### Taksonomi 12 Kelas Limbah:

| Kategori Lingkungan | Kelas Dataset | Label Bahasa Indonesia | Karakteristik Risiko Utama |
| :--- | :--- | :--- | :--- |
| **Limbah B3 (Berbahaya & Beracun)** | `battery` | Baterai & Akumulator | Korosif, beracun, pencemaran logam berat (Hg, Pb, Cd). |
| **Limbah B3 (Berbahaya & Beracun)** | `brown-glass` | Botol Kaca Cokelat (Kimia/Obat) | Kontaminan residu aktif farmasi & bahaya pecahan tajam. |
| **Limbah B3 (Berbahaya & Beracun)** | `green-glass` | Kaca Hijau & Pecahan Kaca | Bahaya fisik luka tusuk & pecahan beling beracun industri. |
| **Limbah B3 (Berbahaya & Beracun)** | `metal` | Kaleng Logam Aerosol Bertekanan | Mudah meledak karena gas propelan sisa dan residu kimia VOC. |
| **Limbah B3 (Berbahaya & Beracun)** | `white-glass` | Kaca Bening, Vial & Lampu Bohlam | Uap merkuri beracun dari lampu neon/TL dan botol obat. |
| **Limbah B3 (Berbahaya & Beracun)** | `trash` | Residu Medis & Masker Infeksius | Biohazard, penularan mikroorganisme patogen dan virus. |
| **Non-B3 / Daur Ulang / Organik** | `biological` | Sampah Organik & Sisa Makanan | Mudah terurai alami, dapat diolah menjadi kompos. |
| **Non-B3 / Daur Ulang / Organik** | `cardboard` | Kardus & Karton Duplex | Serat pulp mudah didaur ulang menjadi produk kertas baru. |
| **Non-B3 / Daur Ulang / Organik** | `clothes` | Pakaian & Serat Tekstil | Bahan dapat didonorkan atau didaur ulang serat majun. |
| **Non-B3 / Daur Ulang / Organik** | `paper` | Kertas HVS, Koran & Dokumen | Daur ulang bubur kertas kering bernilai ekonomis. |
| **Non-B3 / Daur Ulang / Organik** | `plastic` | Wadah Plastik Kemasan (PET/HDPE) | Polimer termoplastik untuk daur ulang pelet plastik. |
| **Non-B3 / Daur Ulang / Organik** | `shoes` | Sepatu & Alas Kaki Bekas | Karet sol dan sintetis untuk pemulihan material sekunder. |

### Pembagian Data & Evaluasi Model:
* **Skema Split**: 80% Data Latih (12.412 citra), 10% Data Validasi (1.536 citra), 10% Data Uji (1.567 citra).
* **Hasil Evaluasi Data Uji (Test Set)**:
  * **Akurasi Pengujian (Test Accuracy)**: **96,17%**
  * **Macro Precision**: 94,46%
  * **Macro Recall**: 94,45%
  * **Macro F1-Score**: 94,35%

---

## 2. Arsitektur Sistem (Client-Server)

Sistem memisahkan secara ketat antara lapisan presentasi (*Frontend UI*) dan lapisan komputasi kecerdasan buatan (*Backend Engine*):

```
┌─────────────────────────────────────────────────────────────┐
│                    LAPISAN PENGGUNA (FRONTEND)              │
│       Streamlit Web App (Port 8501) • Python 3.11           │
│   [Unggah Berkas / Kamera] -> [Pramodel UI & Validasi]      │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP POST /api/v1/predict
                               │ (Multipart Form-Data: Image)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    LAPISAN SERVER (BACKEND REST API)        │
│       FastAPI Web Server (Port 8000) • Uvicorn Worker       │
│                                                             │
│   1. Endpoint Handler (/api/v1/predict)                     │
│   2. Image Preprocessing (Pillow & NumPy)                   │
│   3. Tensor Rescaling & Dimension Formatting                │
│   4. MobileNetV2 Deep Learning Inference Engine             │
│   5. Knowledge-Base SOP & K3 Rule Engine                    │
│   6. Response Serialization (Pydantic Schema)               │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
               models/mobilenetv2_limbah_b3.keras
               models/class_names.json
```

---

## 3. Cara Kerja Aplikasi (Tampak Depan / Frontend Flow)

Dari perspektif pengguna, alur kerja aplikasi dirancang intuitif, responsif, dan bebas dari eksekusi inferensi yang tidak disengaja:

1. **Pemilihan Sumber Citra**:
   * Pengguna dapat memilih antara dua mode:
     * **Unggah Berkas**: Memilih file foto (`.jpg`, `.jpeg`, `.png`, `.webp`) dari penyimpanan komputer/ponsel.
     * **Kamera Langsung**: Mengambil foto secara real-time langsung melalui sensor webcam atau kamera smartphone.
2. **Pratinjau & Kontrol Manual**:
   * Citra yang dipilih akan ditampilkan sebagai pratinjau beserta informasi nama berkas dan ukuran file.
   * Tombol **"Analisis Gambar Sekarang"** hanya aktif apabila berkas citra telah siap. Ini mencegah pemborosan panggilan API kosong (*safe-trigger*).
3. **Penyajian Hasil Analisis (2 Baris Sejajar)**:
   * **Baris 1 (Visual & Diagnosa)**:
     * Sisi Kiri: Foto limbah yang diuji.
     * Sisi Kanan: Kartu status bahaya limbah (apakah termasuk **Limbah B3** atau **Non-B3**), tingkat keyakinan (*confidence score* dalam persentase), waktu latensi komputasi server (ms), dan diagram batang distribusi probabilitas 12 kelas.
   * **Baris 2 (Panduan K3)**:
     * Sisi Kiri: **Prosedur Penanganan Aman (SOP)** yang dianjurkan (misal: penggunaan APD, pemisahan wadah berlabel).
     * Sisi Kanan: **Larangan Keras (Hindari)** yang tidak boleh dilakukan (misal: dilarang membakar, dilarang mencampur dengan sampah umum).

---

## 4. Cara Kerja di Balik Layar (Backend & Inference Pipeline)

Saat tombol **Analisis Gambar Sekarang** ditekan, server backend FastAPI mengeksekusi pipeline komputasi terstruktur berikut:

```
[Citra Mentah (Byte Stream)]
           │
           ▼
[1. Pembacaan Buffer & Validasi Format PIL]
           │
           ▼
[2. Konversi Ruang Warna ke 3-Channel RGB]
           │
           ▼
[3. Bilinear Interpolation Resize ke (224, 224)]
           │
           ▼
[4. Konversi ke Matriks Tensor NumPy float32]
           │
           ▼
[5. Normalisasi Nilai Piksel [-1.0, 1.0]]
           │
           ▼
[6. Forward Pass Konvolusi MobileNetV2 Base]
           │
           ▼
[7. Global Average Pooling & Dense Head]
           │
           ▼
[8. Aktivasi Softmax (Distribusi 12 Probabilitas)]
           │
           ▼
[9. Ekstraksi Argmax & Knowledge-Base Binding SOP]
           │
           ▼
[10. Serialisasi JSON Response ke Frontend]
```

### Rincian Teknis Tiap Tahapan:

1. **Penerimaan Byte Stream**:
   FastAPI menerima berkas melalui parameter `UploadFile = File(...)`. Nama berkas **dieliminasi dari proses inferensi** untuk memastikan model hanya membaca visual piksel murni.
2. **Standardisasi Ruang Warna (Color Space)**:
   Pustaka `PIL.Image.open()` membedah berkas biner. Citra dipaksa dikonversi dengan metode `.convert("RGB")`. Hal ini secara otomatis menormalkan citra RGBA (4 channel transparan) dan Grayscale (1 channel hitam-putih) menjadi format baku 3 channel warna.
3. **Penyelarasan Spasial**:
   Citra di-*resize* menjadi resolusi $224 \times 224$ piksel menggunakan algoritma interpolasi bilinear agar cocok dengan input layer MobileNetV2.
4. **Formulasi Tensor Input**:
   Array piksel dikonversi menjadi tipe data `float32` dan ditambahkan dimensi batch sehingga berdimensi matriks:
   $$\text{Shape} = (1, 224, 224, 3)$$
5. **Normalisasi Nilai Piksel**:
   Nilai intensitas warna dari rentang $[0, 255]$ dinormalisasi ke rentang $[-1.0, 1.0]$ menggunakan formula linier bawaan MobileNetV2:
   $$x_{\text{norm}} = \frac{x}{127.5} - 1.0$$
6. **Ekstraksi Fitur Konvolusional (Base Model)**:
   Tensor dialirkan melalui lapisan *Inverted Residual Blocks* dan *Depthwise Separable Convolutions* MobileNetV2 berbobot ImageNet untuk mengekstraksi representasi fitur hierarkis (garis, tekstur material kaleng/kaca/kardus, hingga bentuk fisik objek).
7. **Dense Classification Head**:
   Fitur spasial dikompresi melalui lapisan:
   * `GlobalAveragePooling2D`: Mengurangi dimensi tensor menjadi vektor fitur 1 dimensi.
   * `BatchNormalization`: Menstabilkan distribusi aktivasi.
   * `Dropout(0.3)` & `Dense(128, ReLU)` & `Dropout(0.2)`: Lapisan representasi non-linear untuk mengklasifikasikan pola khusus limbah B3.
   * `Dense(12, Softmax)`: Menghasilkan 12 nilai peluang.
8. **Kalkulasi Probabilitas Softmax**:
   Probabilitas kelas ke-$c$ dihitung dengan rumus:
   $$P(y = c \mid x) = \frac{e^{z_c}}{\sum_{j=1}^{12} e^{z_j}}$$
   di mana total seluruh $\sum_{j=1}^{12} P_j = 1.0$ ($100\%$).
9. **Penentuan Label & Pengikatan SOP**:
   Indeks dengan nilai probabilitas tertinggi diekstrak via $\text{argmax}(P)$. Indeks tersebut dipetakan ke berkas `models/class_names.json`. Backend kemudian menghubungkannya dengan konfigurasi aturan domain di `config/settings.py` untuk menarik deskripsi bahaya, status B3/Non-B3, serta daftar tindakan SOP dan larangan.
10. **Serialisasi Output JSON**:
    Hasil dikemas ke dalam skema Pydantic (`schemas.PredictionResponse`) dan dikembalikan ke klien dengan payload terstruktur:
    ```json
    {
      "predicted_class": "metal",
      "display_name": "Kaleng Aerosol & Logam Terkontaminasi",
      "confidence": 0.9842,
      "is_b3": true,
      "hazard_level": "BAHAYA TINGGI",
      "probabilities": { ... },
      "sop_actions": [ ... ],
      "prohibitions": [ ... ],
      "latency_ms": 42.15
    }
    ```

---

## 5. Struktur Direktori Proyek

```
Klasifikasi_limbahB3/
├── app.py                         # Entry point & controller navigasi Streamlit
├── requirements.txt               # Daftar pustaka & dependensi sistem
├── README.md                      # Dokumentasi teknis proyek
│
├── app/                           # Backend REST API Package (FastAPI)
│   ├── __init__.py                # Package initializer
│   ├── main.py                    # Aplikasi FastAPI, middleware CORS & router inferensi
│   ├── schemas.py                 # Pydantic schemas (validasi request & response JSON)
│   └── model_service.py           # Engine inferensi Keras & loader MobileNetV2
│
├── config/                        # Konfigurasi sistem & basis pengetahuan
│   └── settings.py                # Konfigurasi taksonomi 12 kelas, tingkat bahaya, & SOP
│
├── core/                          # Komponen utilitas & HTTP client
│   ├── api_client.py              # Klien HTTP penghubung Streamlit ke FastAPI
│   └── preprocessor.py            # Modul pra-pemrosesan citra mandiri
│
├── ui/                            # Modul antarmuka pengguna Streamlit (Clean Vector UI)
│   ├── icons.py                   # Kamus vektor resmi Lucide SVG (tanpa emoji/AI slop)
│   ├── styles.py                  # Custom styling CSS (responsive layout, soft animations)
│   ├── views_home.py              # Tampilan Beranda (hero section & 4 tahapan kerja)
│   ├── views_predict.py           # Tampilan Analisis (input citra, diagnosa, & grid SOP)
│   └── views_about.py             # Tampilan Tentang (katalog 12 kelas & pipeline training)
│
├── dataset/                       # Direktori dataset citra lokal (12 folder kelas)
│
└── models/                        # Bobot model terlatih & kamus label
    ├── mobilenetv2_limbah_b3.keras # Model Keras hasil training Google Colab (96,17% akurasi)
    └── class_names.json           # Kamus pemetaan 12 nama kelas resmi
```

---

## 6. Panduan Menjalankan Aplikasi

Aplikasi dijalankan menggunakan **dua terminal terpisah**:

### Terminal 1 — Menjalankan Server Backend (FastAPI)
```bash
# Pastikan berada di direktori utama proyek
uvicorn app.main:app --reload --port 8000
```
* Layanan REST API aktif di: `http://127.0.0.1:8000`
* Dokumentasi interaktif Swagger UI: `http://127.0.0.1:8000/docs`
* Endpoint diagnostik server: `http://127.0.0.1:8000/health`

### Terminal 2 — Menjalankan Antarmuka Pengguna (Streamlit)
```bash
# Jalankan di jendela terminal baru
streamlit run app.py
```
* Antarmuka aplikasi web akan otomatis terbuka pada peramban di alamat: `http://localhost:8501`

---

## 7. Persyaratan Lingkungan Pengembangan

* **Bahasa Pemrograman**: Python 3.10 atau 3.11
* **Framework Deep Learning**: TensorFlow 2.15+ / 2.16+ / 2.21+ & Keras
* **Framework Backend**: FastAPI 0.110+, Uvicorn, Pydantic v2
* **Framework Frontend**: Streamlit 1.32+
* **Pustaka Pemrosesan Citra & Matriks**: Pillow, NumPy, Scikit-learn, Matplotlib, Seaborn
