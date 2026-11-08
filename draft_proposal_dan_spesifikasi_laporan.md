# Panduan Lengkap Proposal & Spesifikasi Teknis B3Vision
**Mata Kuliah: Kecerdasan Buatan (Universitas Bina Sarana Informatika - UBSI)**  
**Judul: Klasifikasi Jenis Limbah B3 Menggunakan Transfer Learning MobileNetV2**

---

> ### PETUNJUK PENGGUNAAN DOKUMEN INI UNTUK GOOGLE GEMINI:
> *Dokumen ini berisi seluruh spesifikasi program, metodologi AI, arsitektur perangkat lunak, serta naskah draf proposal Bab I s/d Bab V yang sudah diselaraskan 100% dengan aplikasi riil yang telah dibangun.*  
> **Instruksi untuk Gemini:** Gunakan dokumen ini sebagai acuan fakta mutlak (*single source of truth*) dalam menyusun proposal, makalah, maupun laporan tugas akhir. Jangan mengubah nama kelas, arsitektur model, metrik evaluasi, maupun nama framework yang telah didefinisikan di sini.

---

## 1. Identitas Proyek & Anggota Kelompok

| Komponen | Rincian Data Proyek |
| :--- | :--- |
| **Perguruan Tinggi** | Universitas Bina Sarana Informatika (UBSI) |
| **Fakultas / Program Studi** | Fakultas Teknik & Informatika / Informatika (S1) |
| **Mata Kuliah / Kelas** | Kecerdasan Buatan / 15.5A.05 (Kelompok 2) |
| **Tahun Akademik** | Semester 5 / 2026 |
| **Ketua Kelompok** | Muhammad Ichsan Fadillah (NIM: 15240420) |
| **Anggota 1** | Muhammad Athar Ramadhan (NIM: 15240414) |
| **Anggota 2** | Adhitya Esha Faruq Ramadhan (NIM: 15240018) |
| **Tautan Repositori GitHub** | https://github.com/atharramadan03/B3Vision.git |
| **Tautan Dataset Kaggle** | https://www.kaggle.com/datasets/mostafaabla/garbage-classification |

---

## 2. Spesifikasi Teknis Program & Sistem AI (Technical Specification)

Berikut adalah parameter teknis aplikasi yang telah dibangun agar laporan/proposal sesuai dengan kode aslinya:

### A. Tumpukan Teknologi (Technology Stack)
* **Bahasa Pemrograman**: Python 3.11.9
* **Framework Deep Learning**: TensorFlow 2.15+ / 2.21+ & Keras 3
* **Backend Framework**: FastAPI (ASGI Server via Uvicorn, RESTful API murni)
* **Validasi Skema Data**: Pydantic v2
* **Frontend Framework**: Streamlit (Web App responsif tanpa ketergantungan langsung ke TensorFlow)
* **Komponen Ikon UI**: Lucide Icons SVG resmi (bebas emoji/AI slop)
* **Format Bobot Model**: Keras v3 Native format (`models/mobilenetv2_limbah_b3.keras`, ukuran ~23,9 MB)
* **Format Pemetaan Label**: JSON (`models/class_names.json`)

### B. Karakteristik Dataset & Preprocessing
* **Nama Dataset**: *Garbage Classification (12 classes)* oleh Mostafa Abla.
* **Lisensi Dataset**: **Open Database License (ODbL) v1.0** (*Database: Open Database, Contents: © Original Authors*).
* **Volume Citra**: **15.515 citra** terverifikasi pada 12 direktori kelas.
* **Taksonomi 12 Kelas**:
  * **6 Kelas Limbah B3**: `battery` (Baterai), `brown-glass` (Kaca Cokelat Kimia/Obat), `green-glass` (Kaca Hijau Tajam), `metal` (Kaleng Aerosol), `trash` (Residu Medis Infeksius), `white-glass` (Bohlam/Neon Kaca Bening).
  * **6 Kelas Non-B3**: `biological` (Organik/Sisa Makanan), `cardboard` (Kardus Karton), `clothes` (Pakaian Tekstil), `paper` (Kertas HVS), `plastic` (Botol Plastik), `shoes` (Sepatu).
* **Pembersihan Data (*Data Cleaning*)**: Pemindaian format `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp` serta eliminasi folder sampah sistem `__MACOSX` dan file tersembunyi `.*`.
* **Standardisasi Input**: Resize otomatis ke $224 \times 224$ piksel, 3-Kanal RGB, One-Hot Categorical Label, dan normalisasi linier piksel:
  $$x_{\text{norm}} = \frac{x}{127.5} - 1.0 \quad (\text{rentang } [-1.0, 1.0])$$
* **Data Augmentation (Layer GPU)**: `RandomFlip("horizontal_and_vertical")`, `RandomRotation(0.2)`, `RandomZoom(0.15)`, `RandomContrast(0.1)`.
* **Skema Split**: 80% Data Latih (12.412 citra), 10% Data Validasi (1.536 citra), 10% Data Uji Mandiri (1.567 citra), `seed=42`, `batch_size=32`.

### C. Arsitektur Model & Eksperimen 2-Tahap
* **Base Model**: MobileNetV2 pre-trained ImageNet (`include_top=False`, 154 layers).
* **Custom Classification Head**:
  $$\text{Input}(224,224,3) \rightarrow \text{Augmentasi} \rightarrow \text{Rescaling} \rightarrow \text{MobileNetV2} \rightarrow \text{GAP} \rightarrow \text{BatchNorm} \rightarrow \text{Dropout}(0.3) \rightarrow \text{Dense}(128, \text{ReLU}) \rightarrow \text{Dropout}(0.2) \rightarrow \text{Dense}(12, \text{Softmax})$$
* **Tahap 1 (Feature Extraction)**: Base model dibekukan (`trainable=False`), optimizer Adam (LR: 0.001), loss `categorical_crossentropy`, 15 epoch.
* **Tahap 2 (Fine-Tuning)**: Mencairkan 30 layer konvolusi teratas (`layers[:-30]`), optimizer Adam dengan LR diturunkan 10x lipat (LR: 0.0001), 10 epoch tambahan.
* **Hasil Evaluasi Data Uji Mandiri (1.567 Test Citra)**:
  * **Akurasi Pengujian (Test Accuracy)**: **96,17%**
  * **Macro Precision**: 94,46%
  * **Macro Recall**: 94,45%
  * **Macro F1-Score**: 94,35%
  * **Weighted Average F1**: 96,18%

### D. Arsitektur Komputasi Client-Server
* **Frontend (Streamlit)**: Berjalan di `http://localhost:8501`. Tidak memuat modul TensorFlow; bertindak sebagai presenter interaktif yang berkomunikasi murni via HTTP POST ke FastAPI.
* **Backend (FastAPI)**: Berjalan di `http://127.0.0.1:8000`. Menyediakan endpoint:
  * `GET /health`: Healthcheck status server dan konfirmasi model dimuat.
  * `POST /api/v1/predict`: Menerima biner gambar, inferensi model, kalkulasi latensi, dan pengikatan SOP K3 otomatis.
  * Middleware: Mengukur latensi inferensi dalam milidetik (`X-Process-Time-Ms`). Rata-rata latensi: 30–50 ms.

---

## 3. Draf Naskah Proposal Lengkap (Bab I s/d Bab V)

### RINGKASAN PROPOSAL
Limbah Bahan Berbahaya dan Beracun (B3) rumah tangga sering kali tercampur dengan sampah domestik umum karena rendahnya literasi pemilahan serta kemiripan karakteristik visual antar-material limbah. Penanganan yang keliru terhadap limbah B3 (seperti baterai bekas, kaleng aerosol bertekanan, beling tajam, dan limbah medis infeksius) berisiko memicu ledakan fisik, pelepasan uap beracun (merkuri, timbal), dan pencemaran ekosistem tanah serta air. Pengenalan manual oleh petugas kebersihan memiliki keterbatasan dalam hal kecepatan, konsistensi, dan keselamatan kerja.

Untuk mengatasi permasalahan tersebut, project ini membangun **B3Vision**, sistem klasifikasi citra cerdas berbasis arsitektur *Client-Server* (FastAPI Backend dan Streamlit Frontend). Sistem menerapkan metode *Transfer Learning* dengan arsitektur *convolutional neural network* **MobileNetV2** yang dilatih secara bertahap (*Feature Extraction* dan *Fine-Tuning*) menggunakan 15.515 citra pada 12 kategori limbah (6 kelas Limbah B3 dan 6 kelas Non-B3/Daur Ulang). Sistem menerima masukan citra melalui unggah berkas atau kamera langsung, melakukan normalisasi tensor $224 \times 224$ piksel, dan menyajikan keluaran berupa diagnosa kategori limbah, skor keyakinan (*confidence score*), tingkat bahaya, serta rekomendasi panduan Standard Operating Procedure (SOP) K3 resmi yang wajib dilakukan dan larangan keras yang harus dihindari. Model yang dihasilkan mencapai akurasi pengujian mandiri (*Test Accuracy*) sebesar 96,17% dengan latensi inferensi di bawah 50 ms. Luaran project ini berupa prototype aplikasi web interaktif, REST API terdokumentasi Swagger UI, repositori sumber terbuka di GitHub, dan laporan evaluasi akademis.

* **Kata Kunci**: Limbah B3, MobileNetV2, Transfer Learning, FastAPI, Streamlit.
* **Luaran Utama**: Prototype Web B3Vision, REST API FastAPI, Repositori GitHub, Dokumentasi API Swagger, dan Laporan Pengujian.

---

### BAB I: PENDAHULUAN

#### 1.1 Latar Belakang
Limbah Bahan Berbahaya dan Beracun (B3) merupakan sisa suatu usaha atau kegiatan yang mengandung zat, energi, dan komponen berbahaya yang dapat mencemari lingkungan hidup serta membahayakan kesehatan manusia. Di lingkungan rumah tangga, limbah B3 sering kali dibuang sembarangan bersama sampah organik dan anorganik karena minimnya pemahaman masyarakat serta kemiripan fisik antar-objek (misalnya kaleng aerosol berbahan logam yang bercampur dengan kaleng minuman biasa, atau pecahan botol reagen kaca dengan botol sirup umum). 

Pengenalan jenis limbah secara manual memiliki kelemahan mendasar dalam kecepatan, kelelahan manusia, dan risiko paparan zat berbahaya bagi petugas pemilah. Seiring pesatnya perkembangan visi komputer (*Computer Vision*) dan *Deep Learning*, teknologi Convolutional Neural Network (CNN) terbukti sangat efektif dalam mengekstraksi pola visual citra. MobileNetV2 merupakan arsitektur CNN modern yang dirancang khusus untuk efisiensi komputasi tinggi menggunakan mekanisme *Depthwise Separable Convolution* dan *Inverted Residuals*, menjadikannya sangat ideal untuk komputasi cepat berbasis web.

Melalui pendekatan *Transfer Learning* dan *Fine-Tuning*, model MobileNetV2 yang telah dilatih pada basis data ImageNet diadaptasi untuk mengenali 12 kategori limbah rumah tangga. Dengan mengintegrasikan model ke dalam arsitektur Client-Server berbasis FastAPI dan Streamlit, sistem B3Vision hadir sebagai solusi praktis identifikasi awal limbah B3 yang dilengkapi panduan mitigasi keselamatan K3 secara real-time.

#### 1.2 Identifikasi dan Rumusan Masalah
##### 1.2.1 Identifikasi Masalah
1. Pemilahan limbah B3 domestik secara manual rentan mengalami kesalahan akibat kemiripan visual bentuk, warna, dan tekstur antar-material limbah.
2. Belum tersedianya sistem klasifikasi cerdas berbasis web yang memadukan deteksi citra limbah dengan rekomendasi SOP penanganan keselamatan K3 terpadu.
3. Kebutuhan arsitektur deep learning yang ringan dan berkecepatan tinggi agar dapat dioperasikan secara responsif tanpa membutuhkan perangkat keras berbiaya mahal.
4. Diperlukannya pengujian terukur untuk membuktikan kinerja model MobileNetV2 pada dataset citra limbah berskala besar (15.515 citra).

##### 1.2.2 Rumusan Masalah
1. Bagaimana mengimplementasikan metode Transfer Learning dan Fine-Tuning pada arsitektur MobileNetV2 untuk mengklasifikasikan 12 jenis limbah B3 dan Non-B3?
2. Bagaimana merancang arsitektur Client-Server berbasis REST API FastAPI dan antarmuka web Streamlit yang dapat menerima input berkas maupun kamera langsung?
3. Bagaimana kinerja akurasi, precision, recall, F1-score, serta latensi waktu komputasi model MobileNetV2 dalam mengidentifikasi limbah pada data uji mandiri?

#### 1.3 Tujuan Project
1. Menerapkan metode Transfer Learning dan Fine-Tuning MobileNetV2 untuk menghasilkan model klasifikasi citra 12 kelas limbah dengan akurasi pengujian $> 90\%$.
2. Mengembangkan prototype sistem cerdas B3Vision dengan pemisahan lapisan backend (FastAPI) dan frontend (Streamlit) yang responsif dan interaktif.
3. Mengevaluasi performa model menggunakan metrik Confusion Matrix, Classification Report, kurva konvergensi (Accuracy & Loss), serta latensi waktu inferensi.
4. Memberikan luaran sistem pakar SOP keselamatan K3 yang memuat tindakan aman dan larangan penanganan limbah secara otomatis.

#### 1.4 Manfaat Project
1. **Bagi Masyarakat & Pengguna**: Mempermudah identifikasi limbah B3 sejak dari sumber rumah tangga dan memberikan edukasi SOP pembuangan yang aman.
2. **Bagi Petugas Kebersihan & Bank Sampah**: Mengurangi risiko kecelakaan kerja akibat terkena pecahan beling atau ledakan gas kaleng semprot.
3. **Bagi Akademisi & Pengembangan AI**: Memberikan bukti empiris efektivitas arsitektur MobileNetV2 pada klasifikasi limbah citra berskala besar (>15.000 citra) dengan latensi rendah.

#### 1.5 Ruang Lingkup dan Batasan
1. Masukan citra merupakan citra tunggal (*single-image classification*) dengan objek limbah berada di area fokus bingkai kamera.
2. Sistem mengklasifikasikan limbah ke dalam **12 kelas tetap**: 6 kelas B3 (`battery`, `brown-glass`, `green-glass`, `metal`, `trash`, `white-glass`) dan 6 kelas Non-B3 (`biological`, `cardboard`, `clothes`, `paper`, `plastic`, `shoes`).
3. Dataset bersumber dari dataset sekunder publik Kaggle *Garbage Classification (12 classes)* berlisensi ODbL v1.0.
4. Layanan inferensi disediakan melalui REST API FastAPI (`POST /api/v1/predict` dan `GET /health`) dan antarmuka web Streamlit.
5. Sistem berfungsi sebagai alat bantu identifikasi awal dan tidak menggantikan uji laboratorium kimia resmi terkait karakteristik limbah B3.

---

### BAB II: ANALISIS KEBUTUHAN DAN LANDASAN SOLUSI

#### 2.1 Profil Pengguna dan Skenario Penggunaan
Pengguna sistem meliputi masyarakat umum, pengelola bank sampah, dan staf operasional K3. Skenario operasional:
1. Pengguna membuka peramban web pada alamat aplikasi B3Vision.
2. Pengguna memilih sumber masukan: mengunggah berkas foto (`.jpg`, `.png`, `.webp`) atau mengambil gambar langsung menggunakan webcam.
3. Sistem menampilkan pratinjau gambar dan mengaktifkan tombol analisis manual.
4. Pengguna menekan tombol "Analisis Gambar Sekarang".
5. Backend FastAPI menerima biner citra, melakukan pra-pemrosesan tensor, dan mengeksekusi inferensi model MobileNetV2.
6. Antarmuka web menampilkan kartu hasil diagnosa tingkat bahaya, skor keyakinan, distribusi probabilitas, serta grid rekomendasi SOP dan larangan penanganan.

#### 2.2 Kebutuhan Fungsional (Functional Requirements)

| ID | Kebutuhan Fungsional | Prioritas | Kriteria Penerimaan |
| :--- | :--- | :---: | :--- |
| **FR-01** | Pengguna dapat memilih sumber citra (Unggah / Kamera). | Must | Menerima format `.jpg`, `.jpeg`, `.png`, `.webp` (maks 10 MB) dan stream webcam. |
| **FR-02** | Pengguna memicu inferensi secara manual melalui tombol aksi. | Must | Tombol analisis hanya aktif jika citra valid telah tersedia. |
| **FR-03** | Backend memproses inferensi citra via REST API. | Must | Endpoint `POST /api/v1/predict` memproses tensor dan merespons payload JSON. |
| **FR-04** | Sistem menyajikan visualisasi diagnosa dan probabilitas. | Must | Menampilkan label, status B3, tingkat bahaya, persentase keyakinan, dan 12 bar kelas. |
| **FR-05** | Sistem menyajikan rekomendasi SOP K3 dan larangan keras. | Should | Grid 2 kolom yang memuat tindakan aman dan tindakan terlarang. |
| **FR-06** | Sistem memantau status kesiapan server dan model. | Could | Endpoint `GET /health` merespons status `ok` dan ketersediaan file `.keras`. |

#### 2.3 Kebutuhan Nonfungsional (Non-Functional Requirements)

| ID | Aspek | Target / Kriteria Terukur |
| :--- | :--- | :--- |
| **NFR-01** | Kinerja & Latensi | Waktu inferensi pada server memiliki nilai $p95 < 100\text{ ms}$ (rata-rata 30–50 ms). |
| **NFR-02** | Akurasi & Keandalan | Akurasi pengujian model pada Test Set $> 90\%$ (tercapai **96,17%**). |
| **NFR-03** | Keamanan Data | Citra diproses secara *in-memory* tanpa disimpan permanen di basis data publik. |
| **NFR-04** | Usability & Antarmuka | Menggunakan vektor resmi Lucide SVG (tanpa emoji), tata letak kontainer 1260px responsif. |

#### 2.4 Data, Input, dan Output
* **Sumber Data**: Kaggle *Garbage Classification (12 classes)* oleh Mostafa Abla (Lisensi ODbL v1.0).
* **Komposisi Data**: 15.515 citra (80% Train / 10% Validation / 10% Test).
* **Format Input**: Citra RGB berekstensi JPG/PNG yang dinormalisasi ke resolusi $224 \times 224$ piksel.
* **Format Output**: Skema JSON (`PredictionResponse`) yang divisualisasikan menjadi kartu diagnosa, bar probabilitas, serta panduan SOP K3.

#### 2.5 Pemilihan Model, Algoritma, dan Framework
1. **Model AI (MobileNetV2)**: Menggunakan *Depthwise Separable Convolution* dengan parameter ringkas (~3,5 juta parameter vs 138 juta pada VGG16), menghasilkan ukuran model kecil (~24 MB) dan waktu inferensi cepat (~40 ms).
2. **Backend (FastAPI)**: Framework modern berbasis async/await dengan validasi otomatis Pydantic dan dokumentasi otomatis Swagger UI di `/docs`.
3. **Frontend (Streamlit)**: Memungkinkan pembuatan antarmuka data web yang bersih tanpa perlu memuat TensorFlow di sisi frontend (*decoupled architecture*).
4. **Serialisasi**: Menggunakan format native Keras 3 (`.keras`) yang menyimpan konfigurasi dan bobot secara terkompresi.

#### 2.6 Risiko dan Etika AI
* **Mitigasi Kesalahan Prediksi**: Sistem menampilkan diagram probabilitas lengkap dan *disclaimer* keselamatan resmi agar pengguna tetap berhati-hati.
* **Privasi**: Tidak ada foto pengguna yang disimpan permanen di server.

---

### BAB III: RANCANGAN ARSITEKTUR DAN API

#### 3.1 Diagram Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────────┐
│                 CLIENT LAYER (STREAMLIT WEB)                │
│                 Port: 8501 • Python 3.11                    │
│   - Input: Unggah Berkas & Kamera Langsung                  │
│   - UI: Lucide SVG Icons, Container 1260px Responsive       │
│   - Output: Diagnosa Status B3, Bar Probabilitas, SOP K3    │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP POST /api/v1/predict
                               │ (Multipart/form-data: image)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 SERVER LAYER (FASTAPI REST API)             │
│                 Port: 8000 • Uvicorn ASGI                   │
│   - Middleware: CORS & X-Process-Time-Ms                    │
│   - Image Preprocessing: PIL RGB -> Resize (224, 224)       │
│   - Normalisasi: Rescaling(1/127.5, offset=-1.0)            │
│   - Inference: MobileNetV2 (12-Class Softmax)               │
│   - Knowledge Base Rule Engine: config/settings.py          │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
               models/mobilenetv2_limbah_b3.keras
               models/class_names.json
```

#### 3.3 Rancangan Endpoint API

| Method | Endpoint | Request Body | Response Body | Status Code |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/health` | None | `HealthResponse` (status, model_loaded, model_version, total_classes) | `200 OK` / `503 Unavailable` |
| **POST** | `/api/v1/predict` | `multipart/form-data` (file) | `PredictionResponse` (label, score, is_b3, probabilities, sop_actions, prohibitions, latency_ms) | `200 OK` / `400 Bad Request` / `503 Unavailable` |

#### 3.4 Contoh Struktur JSON Respons (`POST /api/v1/predict`)
```json
{
  "status": "success",
  "filename": "sampel_kaleng.jpg",
  "label": "metal",
  "class_name": "Kaleng Aerosol & Logam Terkontaminasi",
  "short_name": "Kaleng Aerosol (B3)",
  "category": "B3",
  "hazard_level": "Mudah Meledak & Beracun",
  "score": 0.9842,
  "confidence": 0.9842,
  "is_confident": true,
  "status_state": "B3_DANGER",
  "model_version": "v2.0-mobilenetv2-12class",
  "latency_ms": 42.15,
  "probabilities": {
    "battery": 0.0012,
    "metal": 0.9842,
    "plastic": 0.0098
  },
  "sop_actions": [
    "Pastikan isi gas aerosol telah terbuang habis di area berventilasi terbuka sebelum disimpan.",
    "Simpan pada suhu ruang di tempat yang sejuk dan tidak berdekatan dengan instalasi listrik."
  ],
  "prohibitions": [
    "DILARANG menusuk, melubangi, atau menggepengkan kaleng aerosol yang masih bertekanan.",
    "DILARANG membakar kaleng bekas di tempat pembuangan sampah terbuka."
  ]
}
```

---

### BAB IV: RENCANA IMPLEMENTASI DAN PENGUJIAN

#### 4.2 Struktur Repository

```
Klasifikasi_limbahB3/
├── app.py                         # Controller antarmuka web Streamlit
├── requirements.txt               # Daftar pustaka dependensi sistem
├── README.md                      # Dokumentasi teknis proyek di GitHub
├── penjelasan_eksperimen_model.md # Naskah komprehensif eksperimen skripsi
│
├── app/                           # Backend REST API Package (FastAPI)
│   ├── main.py                    # Endpoint API, CORS, & middleware latensi
│   ├── schemas.py                 # Skema Pydantic validasi I/O
│   └── model_service.py           # Loader Keras & engine inferensi
│
├── config/                        # Basis Pengetahuan & Konfigurasi
│   └── settings.py                # Taksonomi 12 kelas, tingkat bahaya, & aturan SOP
│
├── core/                          # Komponen Utilitas
│   ├── api_client.py              # Klien HTTP requests penghubung UI ke API
│   └── preprocessor.py            # Modul normalisasi citra
│
├── ui/                            # Modul Antarmuka Pengguna
│   ├── icons.py                   # Vektor SVG resmi Lucide Icons
│   ├── styles.py                  # Styling CSS layout 1260px & animasi lembut
│   ├── views_home.py              # View Halaman Beranda
│   ├── views_predict.py           # View Halaman Analisis & Grid SOP
│   └── views_about.py             # View Halaman Tentang & Pipeline Training
│
└── models/                        # Artifak Model AI
    ├── mobilenetv2_limbah_b3.keras # Model bobot terlatih (96,17% akurasi)
    └── class_names.json           # Kamus indeks 12 kelas
```

#### 4.3 Rencana dan Hasil Pengujian

| ID | Jenis Pengujian | Skenario Uji | Hasil yang Diharapkan | Status |
| :--- | :--- | :--- | :--- | :---: |
| **T-01** | *Integration Test* | Unggah foto kaleng aerosol valid via Streamlit. | Status 200, label `metal` terdeteksi, SOP muncul di UI. | **Lolos** |
| **T-02** | *Negative Test* | Kirim berkas non-citra (`.txt`) ke API. | Status 400 Bad Request, pesan error format tidak valid. | **Lolos** |
| **T-03** | *Performance Test* | Komputasi inferensi tensor $224 \times 224$ px. | Latensi server $p95 < 100\text{ ms}$ (tercapai 30–50 ms). | **Lolos** |
| **T-04** | *Model Evaluation* | Uji mandiri pada 1.567 data uji di Colab. | Akurasi $> 90\%$ (Tercapai: **96,17%**, F1: **94,35%**). | **Lolos** |

---

### BAB V: MANAJEMEN PROJECT

#### 5.1 Pembagian Peran dan Tanggung Jawab

| Nama / NIM | Peran | Tanggung Jawab Utama | Bukti Kontribusi |
| :--- | :--- | :--- | :--- |
| **Muhammad Ichsan Fadillah**<br>NIM: 15240420 | **Project Lead & Backend Engineer** | 1. Mengkoordinasikan timeline project dan penyusunan proposal.<br>2. Membangun REST API FastAPI (`app/main.py`, `app/schemas.py`).<br>3. Integrasi middleware latensi dan endpoint `/health`. | Dokumen Proposal, kode `main.py`, pengujian Swagger. |
| **Muhammad Athar Ramadhan**<br>NIM: 15240414 | **AI & Machine Learning Engineer** | 1. Pengadaan dataset 15.515 citra dan pembersihan data di Colab.<br>2. Melatih model MobileNetV2 (Feature Extraction & Fine-Tuning).<br>3. Evaluasi akurasi 96,17%, confusion matrix, dan repositori GitHub. | Script Colab, file `.keras`, commit `atharramadan03/B3Vision`. |
| **Adhitya Esha Faruq Ramadhan**<br>NIM: 15240018 | **Frontend UI/UX & QA Engineer** | 1. Membangun antarmuka Streamlit dengan komponen Lucide SVG.<br>2. Merancang tata letak seimbang 2 baris (Diagnosa dan Grid SOP K3).<br>3. Pengujian sistem (*black-box testing*) input file dan kamera. | File `views_predict.py`, `styles.py`, laporan uji. |

#### 5.2 Jadwal Pelaksanaan

| Minggu | Target Capaian | PIC | Luaran / Bukti |
| :---: | :--- | :---: | :--- |
| **1** | Analisis kebutuhan, studi regulasi B3, perolehan dataset 15.515 citra. | Tim Kelompok | Bab 1 & 2 Proposal, dataset Kaggle. |
| **2** | *Data cleaning*, perancangan MobileNetV2, dan pelatihan di Colab. | M. Athar R. | Model `mobilenetv2_limbah_b3.keras`, grafik loss. |
| **3** | Pembuatan REST API FastAPI dan skema data Pydantic. | M. Ichsan F. | Backend API aktif, Swagger UI `/docs`. |
| **4** | Pembuatan UI Streamlit, integrasi API, perancangan grid SOP K3. | Adhitya Esha | Aplikasi Web berjalan di `localhost:8501`. |
| **5** | Pengujian menyeluruh, finalisasi proposal, persiapan presentasi. | Tim Kelompok | Dokumen Proposal Final & Repositori bersih. |

#### 5.3 Risiko Project dan Mitigasi

| Risiko | Dampak | Probabilitas | Rencana Mitigasi | PIC |
| :--- | :---: | :---: | :--- | :---: |
| Keterbatasan RAM Colab saat training 15.000 citra | Tinggi | Tinggi | Menghapus pemanggilan `.cache()` dan menggunakan generator *prefetch* batch 32 citra. | M. Athar R. |
| Overfitting akibat kemiripan latar belakang citra | Sedang | Sedang | Menggunakan 4 layer augmentasi acak (flip, rotasi, zoom, kontras) dan Dropout (0.3 + 0.2). | M. Athar R. |
| Ketidakcocokan koneksi UI Streamlit ke backend | Tinggi | Rendah | Mengimplementasikan fungsi *health check* otomatis pada UI sebelum inferensi. | M. Ichsan F. |
| Kesalahan prediksi pada objek visual serupa | Sedang | Sedang | Menyajikan diagram sebaran 12 probabilitas Softmax dan penafian (*disclaimer*) K3. | Adhitya Esha |

---

## 4. Panduan Penyisipan Tangkapan Layar (Screenshots) pada Dokumen Laporan

Saat menyusun laporan atau proposal final di Microsoft Word, sisipkan tangkapan layar (*screenshot*) pada posisi-posisi berikut:

1. **[SISIPKAN GAMBAR 1: Diagram Arsitektur Sistem Client-Server B3Vision]**  
   *Letak*: Pada **Bab III Sub-bab 3.1**.  
   *Deskripsi*: Diagram alur data yang menghubungkan Frontend Streamlit, HTTP POST Multipart, Backend FastAPI, dan model Keras.

2. **[SISIPKAN GAMBAR 2: Dokumentasi Interaktif Swagger UI FastAPI]**  
   *Letak*: Pada **Bab III Sub-bab 3.3** atau Lampiran.  
   *Deskripsi*: Buka peramban ke `http://127.0.0.1:8000/docs`, ambil tangkapan layar endpoint `POST /api/v1/predict` dan `GET /health`.

3. **[SISIPKAN GAMBAR 3: Tampilan Antarmuka Halaman Beranda (Home View)]**  
   *Letak*: Pada **Bab III Sub-bab 3.6**.  
   *Deskripsi*: Tangkapan layar halaman Beranda B3Vision yang memperlihatkan judul "Klasifikasi Limbah B3 Menggunakan MobileNetV2", statistik 12 kelas, dan 4 tahapan cara kerja.

4. **[SISIPKAN GAMBAR 4: Tampilan Halaman Analisis (Input Berkas & Kamera Langsung)]**  
   *Letak*: Pada **Bab III Sub-bab 3.6** atau Bab IV.  
   *Deskripsi*: Tangkapan layar panel kiri halaman Analisis saat pengguna memilih file foto limbah dan saat pratinjau citra muncul.

5. **[SISIPKAN GAMBAR 5: Tampilan Hasil Diagnosa & Grid SOP Penanganan K3]**  
   *Letak*: Pada **Bab IV Sub-bab 4.3** (Hasil Pengujian Fungsional).  
   *Deskripsi*: Tangkapan layar hasil prediksi (misal sampel kaleng aerosol): memperlihatkan Kartu Diagnosa Tingkat Bahaya di atas, dan Grid 2 Kolom "Prosedur Penanganan Aman (SOP)" di kiri serta "Larangan Keras (Hindari)" di kanan.

6. **[SISIPKAN GAMBAR 6: Grafik Konvergensi Pelatihan (Accuracy & Loss Curve)]**  
   *Letak*: Pada **Bab IV Sub-bab 4.1**.  
   *Deskripsi*: Sisipkan berkas gambar `grafik_training_mobilenetv2.png` yang memperlihatkan kurva pelatihan dan garis putus-putus transisi Fine-Tuning.

7. **[SISIPKAN GAMBAR 7: Matriks Konfusi (Confusion Matrix Heatmap)]**  
   *Letak*: Pada **Bab IV Sub-bab 4.1**.  
   *Deskripsi*: Sisipkan berkas gambar `confusion_matrix_b3.png` yang memperlihatkan matriks sebaran prediksi $12 \times 12$ dengan akurasi 96,17%.

---

## 5. Solusi Mengapa Ukuran ZIP Mencapai 305 MB & Cara Mengatasinya

### Mengapa Ukuran ZIP Folder Mencapai ~305 MB?
Berdasarkan audit ukuran berkas pada repositori:
* Folder tersembunyi `.git/`: **~278 MB** (menyimpan riwayat kompresi git dari ribuan gambar yang sempat ter-commit sebelumnya).
* Berkas model `models/mobilenetv2_limbah_b3.keras`: **~23,9 MB**.
* Seluruh kode program aplikasi (`app/`, `ui/`, `core/`, `config/`, `app.py`): **Hanya ~0,3 MB (< 1 MB)**!

### Cara Mengompresi / Mengirim ke Gemini dengan Ringan:
1. **Jika ingin mengunggah ke Gemini untuk membuat laporan:**  
   Gemini **hanya memerlukan berkas kode teks dan dokumen markdown**, tidak memerlukan berkas biner `.keras` atau folder `.git`!  
   *Cukup pilih file berikut untuk di-zip:*
   * `app/`, `config/`, `core/`, `ui/`
   * `app.py`, `requirements.txt`, `README.md`
   * `penjelasan_eksperimen_model.md`
   * `draft_proposal_dan_spesifikasi_laporan.md`  
   *Ukuran total ZIP ini **kurang dari 1 MB (hanya ~300 KB)** dan dapat diunggah ke Gemini secara instan!*

2. **Jika ingin membuat ZIP untuk pengumpulan tugas akhir:**  
   Cukup kecualikan (*exclude*) folder tersembunyi `.git/`. Ukuran ZIP aplikasi utuh beserta modelnya hanya menjadi **sekitar ~23 MB** (jauh di bawah batas 305 MB).
