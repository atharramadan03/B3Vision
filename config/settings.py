"""
Konfigurasi Aplikasi B3Vision (12 Kelas Dataset Penuh)
Pengaturan taksonomi 12 kelas (6 Limbah B3 & 6 Non-B3), ambang batas keyakinan, dan SOP penanganan.
"""

APP_TITLE = "B3Vision"
APP_TAGLINE = "Pilah Limbah B3, Jaga Lingkungan"
APP_VERSION = "v2.0 (12-Class MobileNetV2)"

# Ambang batas kepercayaan model (di bawah ini dianggap 'Kurang Yakin / Perlu Foto Ulang')
CONFIDENCE_THRESHOLD = 0.60

# Taksonomi dan Definisi Lengkap 12 Kelas Dataset
CLASSES = {
    # ==================== 6 KELAS LIMBAH B3 (BERBAHAYA & BERACUN) ====================
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

    # ==================== 6 KELAS NON-B3 (DAUR ULANG, ORGANIK, & TEKSTIL) ====================
    "biological": {
        "id": "biological",
        "name": "Sampah Organik & Sisa Makanan",
        "short_name": "Organik (Non-B3)",
        "category": "Non-B3",
        "badge_color": "#16A34A",
        "icon": "🍎",
        "hazard_level": "Aman (Dapat Dikomposkan)",
        "description": "Sisa sayuran, buah-buahan, sisa makanan dapur, daun kering, dan bahan organik mudah terurai hayati.",
        "environmental_impact": "Menghasilkan gas metana (CH4) jika tertumpuk di TPA tanpa oksigen, namun sangat bermanfaat jika diolah menjadi pupuk kompos atau pakan maggot.",
        "sop_actions": [
            "Pisahkan secara ketat dari sampah anorganik dan limbah B3 beracun.",
            "Tiriskan sisa air/kuah makanan sebelum dimasukkan ke dalam wadah pengomposan.",
            "Manfaatkan sebagai bahan baku pembuatan kompos organik atau pakan biokonversi maggot BSF.",
            "Gunakan wadah sampah bertutup rapat untuk mencegah bau dan perkembangbiakan lalat."
        ],
        "prohibitions": [
            "DILARANG mencampur sampah organik dengan baterai atau pecahan kaca.",
            "DILARANG membakar sampah organik basah karena menimbulkan asap pekat yang mencemari udara."
        ]
    },
    "cardboard": {
        "id": "cardboard",
        "name": "Kardus & Karton Kemasan",
        "short_name": "Kardus (Non-B3)",
        "category": "Non-B3",
        "badge_color": "#16A34A",
        "icon": "📦",
        "hazard_level": "Aman (Daur Ulang Tinggi)",
        "description": "Kardus cokelat bergelombang (corrugated box), karton duplex kemasan makanan kering, dan tabung karton gulungan.",
        "environmental_impact": "Dapat didaur ulang menjadi bubur kertas (pulp) berulang kali untuk mengurangi penebangan pohon dan deforestasi hutan.",
        "sop_actions": [
            "Bongkar lipatan dan pipihkan kardus untuk menghemat ruang tempat penyimpanan.",
            "Lepaskan selotip plastik, lakban, dan staples logam tebal yang masih menempel.",
            "Jaga kardus tetap kering dan terlindung dari cipratan air agar nilai daur ulangnya tinggi.",
            "Ikat tumpukan kardus dengan tali dan setorkan ke Bank Sampah atau mitra daur ulang."
        ],
        "prohibitions": [
            "DILARANG sengaja membasahi kardus untuk menambah bobot timbangan.",
            "DILARANG membakar tumpukan kardus karena berisiko memicu kebakaran lingkungan."
        ]
    },
    "clothes": {
        "id": "clothes",
        "name": "Pakaian & Limbah Tekstil",
        "short_name": "Pakaian / Tekstil (Non-B3)",
        "category": "Non-B3",
        "badge_color": "#16A34A",
        "icon": "👕",
        "hazard_level": "Aman (Guna Ulang / Daur Ulang)",
        "description": "Baju bekas, celana kain, jaket, kain perca penjahit, selimut, dan serat tekstil katun maupun sintetis.",
        "environmental_impact": "Serat sintetis (polyester/nylon) sulit terurai dan melepaskan mikroplastik ke lingkungan jika terbuang ke perairan terbuka.",
        "sop_actions": [
            "Cuci dan rapikan pakaian jika kondisinya masih layak pakai untuk didonasikan kembali.",
            "Pisahkan kancing logam atau resleting jika pakaian akan dicacah menjadi bahan isian daur ulang.",
            "Gunakan kain perca rusak sebagai lap pembersih (majun) serbaguna.",
            "Serahkan ke Dropbox daur ulang tekstil atau yayasan sosial terdekat."
        ],
        "prohibitions": [
            "DILARANG membakar pakaian bekas karena serat sintetis melepaskan gas beracun dioksin.",
            "DILARANG membuang limbah kain ke sungai atau selokan yang menyumbat saluran air."
        ]
    },
    "paper": {
        "id": "paper",
        "name": "Kertas & Dokumen Daur Ulang",
        "short_name": "Kertas (Non-B3)",
        "category": "Non-B3",
        "badge_color": "#16A34A",
        "icon": "📄",
        "hazard_level": "Aman (Daur Ulang)",
        "description": "Kertas HVS putih, koran bekas, majalah, buku tulis, amplop surat, dan selebaran kertas kering.",
        "environmental_impact": "Daur ulang 1 ton kertas menghemat 17 batang pohon dewasa, 7.000 galon air bersih, dan mengurangi emisi gas rumah kaca.",
        "sop_actions": [
            "Pisahkan penjepit kertas (paper clip), staples, dan binder plastik dari lembaran kertas.",
            "Hancurkan (shredding) dokumen sensitif atau rahasia pribadi sebelum disalurkan.",
            "Simpan kertas dalam keadaan bersih, kering, dan tidak terkontaminasi minyak makanan.",
            "Tumpuk rapi dan salurkan ke Bank Sampah atau pabrik daur ulang kertas terdekat."
        ],
        "prohibitions": [
            "DILARANG mencampur kertas bersih dengan sampah basah sisa makanan dapur.",
            "DILARANG membakar sampah kertas di pekarangan rumah."
        ]
    },
    "plastic": {
        "id": "plastic",
        "name": "Plastik Daur Ulang (PET/HDPE)",
        "short_name": "Plastik (Non-B3)",
        "category": "Non-B3",
        "badge_color": "#16A34A",
        "icon": "🥤",
        "hazard_level": "Aman (Daur Ulang)",
        "description": "Botol minuman plastik (PET), botol detergen (HDPE), wadah makanan bersih, dan gelas plastik bening.",
        "environmental_impact": "Bukan racun langsung B3, namun membutuhkan daur ulang sirkular agar tidak terpecah menjadi mikroplastik yang mencemari laut.",
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
    },
    "shoes": {
        "id": "shoes",
        "name": "Sepatu & Alas Kaki Bekas",
        "short_name": "Sepatu (Non-B3)",
        "category": "Non-B3",
        "badge_color": "#16A34A",
        "icon": "👟",
        "hazard_level": "Aman (Guna Ulang / Refurbish)",
        "description": "Sepatu kets (sneakers), sandal karet, sepatu olahraga, dan alas kaki kombinasi karet sol, busa EVA, dan kanvas.",
        "environmental_impact": "Sol karet dan perekat sintetis butuh ratusan tahun untuk terurai di alam; daur ulang karet sol dapat diolah menjadi matras lantai olahraga.",
        "sop_actions": [
            "Bersihkan kotoran tanah yang menempel pada sol luar sepatu.",
            "Ikat kedua pasang sepatu menjadi satu agar tidak terpisah saat pengumpulan.",
            "Jika sol terkelupas namun badan sepatu masih kokoh, lakukan perbaikan (sol sepatu ulang).",
            "Salurkan ke program donasi alas kaki atau drop point daur ulang khusus sepatu."
        ],
        "prohibitions": [
            "DILARANG membakar sol karet sepatu karena menghasilkan asap hitam pekat karsinogenik.",
            "DILARANG membuang sepatu bekas ke selokan, danau, atau aliran sungai."
        ]
    }
}

# Endpoint API backend
import os as _os
API_URL = _os.environ.get("B3VISION_API_URL", "http://127.0.0.1:8000/api/v1/predict")

# Catatan resmi di bawah hasil analisis
OFFICIAL_DISCLAIMER = (
    "Hasil analisis ini adalah prediksi otomatis deep learning dan dapat keliru. "
    "Jika ragu dengan jenis limbah berbahaya, selalu perlakukan objek tersebut dengan standar kehati-hatian limbah B3."
)
