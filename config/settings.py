"""
Konfigurasi Aplikasi B3Vision (7 Kelas Dataset)
Pengaturan kelas limbah, ambang batas confidence, dan panduan penanganan limbah.
"""

APP_TITLE = "B3Vision"
APP_TAGLINE = "Pilah Limbah B3, Jaga Lingkungan"
APP_VERSION = "v1.0 (7-Class MobileNetV2)"

# Ambang batas kepercayaan model (di bawah ini dianggap 'Tidak Yakin / Perlu Foto Ulang')
CONFIDENCE_THRESHOLD = 0.60

# Taksonomi dan Definisi 7 Kelas Dataset
CLASSES = {
    "battery": {
        "id": "battery",
        "name": "Baterai & Akumulator",
        "short_name": "Baterai (B3)",
        "category": "B3",
        "badge_color": "#DC2626",
        "icon": "🔋",
        "hazard_level": "Beracun & Korosif",
        "description": "Baterai sel kering (AA/AAA), aki basah/kering, baterai lithium ponsel, dan button cell jam.",
        "environmental_impact": "Mengandung logam berat Merkuri (Hg), Kadmium (Cd), dan Timbal (Pb) yang merusak ginjal, sistem saraf, dan mencemari rantai makanan.",
        "sop_actions": [
            "Tutup kedua kutub positif (+) dan negatif (-) menggunakan selotip kertas/isolasi listrik untuk mencegah arus pendek.",
            "Simpan baterai di wadah plastik tebal terisolasi dan kedap air.",
            "Jauhkan dari kontak langsung dengan sumber panas atau sinar matahari terik.",
            "Salurkan ke Dropbox E-Waste resmi di kantor pemerintahan atau bank sampah terdekat."
        ],
        "prohibitions": [
            "DILARANG membakar atau membongkar lapisan luar baterai.",
            "DILARANG membuang baterai ke tempat sampah basah domestik.",
            "DILARANG membasahi baterai bekas dengan air."
        ]
    },
    "metal": {
        "id": "metal",
        "name": "Kaleng Aerosol & Logam Terkontaminasi",
        "short_name": "Kaleng Aerosol (B3)",
        "category": "B3",
        "badge_color": "#DC2626",
        "icon": "🛢️",
        "hazard_level": "Mudah Meledak & Beracun",
        "description": "Kaleng semprot obat nyamuk, cat semprot (pilox), deodoran aerosol, dan kemasan logam residu kimia.",
        "environmental_impact": "Gas propelan bertekanan sisa dan senyawa organik volatil (VOC) dapat memicu ledakan serta mencemari lapisan ozon.",
        "sop_actions": [
            "Pastikan isi gas aerosol telah terbuang habis di area berventilasi terbuka sebelum disimpan.",
            "Simpan pada suhu ruang di tempat yang sejuk dan tidak berdekatan dengan instalasi listrik.",
            "Pisahkan dari sampah logam biasa yang tidak terkontaminasi bahan kimia.",
            "Serahkan ke fasilitas pengelolaan limbah B3 berizin."
        ],
        "prohibitions": [
            "DILARANG menusuk, melubangi, atau menggepengkan kaleng aerosol yang masih bertekanan.",
            "DILARANG membakar kaleng bekas di tempat pembuangan sampah terbuka."
        ]
    },
    "brown-glass": {
        "id": "brown-glass",
        "name": "Botol Kaca Cokelat (Kimia / Obat)",
        "short_name": "Kaca Cokelat (B3)",
        "category": "B3",
        "badge_color": "#DC2626",
        "icon": "🧴",
        "hazard_level": "Kontaminan Kimia & Benda Tajam",
        "description": "Botol sirup obat farmasi, botol reagen laboratorium, dan botol kaca amber penyimpan bahan peka cahaya.",
        "environmental_impact": "Residu senyawa aktif obat/kimia dapat membunuh mikroorganisme tanah dan mencemari sumber air bersih.",
        "sop_actions": [
            "Bilas bagian dalam botol jika zat kimia tidak reaktif dengan air, lalu tampung air bilasan sebagai residu terpisah.",
            "Bungkus botol dengan kertas koran tebal atau kardus kaku agar tidak pecah saat pengangkutan.",
            "Beri label peringatan 'Awas Residu Kimia / Kaca' pada kemasan luar.",
            "Serahkan ke drop point limbah farmasi atau fasilitas kesehatan terdekat."
        ],
        "prohibitions": [
            "DILARANG memecahkan botol kaca amber di sekitar pemukiman.",
            "DILARANG mencampur dengan botol kaca minuman biasa tanpa dekontaminasi."
        ]
    },
    "green-glass": {
        "id": "green-glass",
        "name": "Kaca Hijau & Pecahan Kaca",
        "short_name": "Kaca Hijau (B3)",
        "category": "B3",
        "badge_color": "#DC2626",
        "icon": "🍾",
        "hazard_level": "Bahaya Fisik Benda Tajam",
        "description": "Pecahan botol kaca hijau, kaca industri berpewarna, dan beling tajam berisiko fisik tinggi.",
        "environmental_impact": "Kaca tidak dapat terurai secara alami selama jutaan tahun dan berisiko fatal melukai petugas kebersihan serta hewan liar.",
        "sop_actions": [
            "Gunakan sarung tangan pelindung anti-sayat saat memungut pecahan kaca.",
            "Tempatkan pecahan kaca ke dalam kotak kardus tebal atau jeriken plastik bekas yang diberi lakban kuat.",
            "Tuliskan tanda peringatan 'AWAS PECAHAN KACA' dengan jelas.",
            "Salurkan ke penampungan khusus benda tajam (sharps waste)."
        ],
        "prohibitions": [
            "DILARANG membuang pecahan kaca ke dalam kantong plastik tipis yang mudah robek.",
            "DILARANG membiarkan beling berserakan di tanah terbuka."
        ]
    },
    "white-glass": {
        "id": "white-glass",
        "name": "Kaca Bening, Vial & Lampu Bohlam",
        "short_name": "Kaca Bening / Lampu (B3)",
        "category": "B3",
        "badge_color": "#DC2626",
        "icon": "💡",
        "hazard_level": "Uap Merkuri & Benda Tajam",
        "description": "Lampu neon tubular (TL), bohlam CFL/LED, vial kaca medis, dan botol kaca bening laboratorium.",
        "environmental_impact": "Lampu neon mengandung bubuk fosfor dan gas uap merkuri beracun yang menguap ke udara begitu tabung pecah.",
        "sop_actions": [
            "Kemas lampu neon atau tabung kaca panjang dalam selongsong kardus aslinya.",
            "Pastikan tabung kaca tidak tertekan atau tertindih benda berat lainnya.",
            "Jika lampu pecah di dalam ruangan, segera buka ventilasi jendela dan hindari menghirup udara di sekitarnya.",
            "Kirimkan ke TPS B3 atau Dropbox E-Waste terdaftar."
        ],
        "prohibitions": [
            "DILARANG sengaja memecahkan lampu neon untuk memperkecil volume sampah.",
            "DILARANG membakar kaca lampu bersama sampah rumah tangga."
        ]
    },
    "trash": {
        "id": "trash",
        "name": "Residu Medis & Masker Infeksius",
        "short_name": "Residu Medis (B3)",
        "category": "B3",
        "badge_color": "#DC2626",
        "icon": "🩹",
        "hazard_level": "Infeksius Domestik",
        "description": "Masker medis sekali pakai, perban luka, sarung tangan lateks, kapas bekas antiseptik, dan jarum tes gula darah.",
        "environmental_impact": "Dapat menularkan bakteri patogen, virus berbahaya, dan penyakit menular kepada masyarakat serta pemulung.",
        "sop_actions": [
            "Gunting tali masker atau potong masker bekas pakai untuk mencegah penyalahgunaan/daur ulang ilegal.",
            "Rendam dalam cairan disinfektan/klorin encer jika terkontaminasi cairan tubuh.",
            "Masukkan ke dalam kantong plastik khusus berwarna kuning atau kantong berlabel 'Limbah Medis'.",
            "Ikat rapat dan serahkan ke fasilitas pelayanan kesehatan atau pos pengumpulan B3 medis."
        ],
        "prohibitions": [
            "DILARANG membuang masker dan perban medis ke saluran pembuangan air atau toilet.",
            "DILARANG membuang jarum suntik tanpa pelindung jarum ke kantong sampah umum."
        ]
    },
    "plastic": {
        "id": "plastic",
        "name": "Plastik Daur Ulang (PET/HDPE)",
        "short_name": "Plastik (Non-B3)",
        "category": "Non-B3",
        "badge_color": "#16A34A",
        "icon": "♻️",
        "hazard_level": "Aman (Negative Control)",
        "description": "Botol minuman plastik (PET), botol detergen (HDPE), wadah makanan bersih, dan gelas plastik bening.",
        "environmental_impact": "Bukan limbah beracun B3 langsung, namun membutuhkan pengelolaan sirkular agar tidak menyumbat saluran air dan mencemari lautan.",
        "sop_actions": [
            "Kosongkan dan bilas bersih wadah dari sisa cairan manis atau minyak.",
            "Lepaskan label plastik dan pisahkan tutup botol jika diperlukan.",
            "Pipihkan / remas botol untuk menghemat ruang tampung tempat sampah.",
            "Kumpulkan dan setorkan ke Bank Sampah atau drop box daur ulang sirkular."
        ],
        "prohibitions": [
            "DILARANG membakar sampah plastik di pekarangan karena asapnya melepaskan senyawa karsinogenik.",
            "DILARANG membuang plastik ke aliran sungai atau selokan umum."
        ]
    }
}

# Endpoint API backend (dikonfigurasi di sini, tidak ditampilkan di UI).
# Bisa di-override lewat environment variable B3VISION_API_URL.
import os as _os
API_URL = _os.environ.get("B3VISION_API_URL", "http://127.0.0.1:8000/api/v1/predict")

# Catatan singkat di bawah hasil analisis
OFFICIAL_DISCLAIMER = (
    "Hasil analisis ini adalah prediksi otomatis berdasarkan gambar dan dapat keliru. "
    "Jika ragu, perlakukan limbah tersebut sebagai limbah B3."
)
