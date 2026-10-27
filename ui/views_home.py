import streamlit as st
from config.settings import APP_TAGLINE


def _clean_html(raw: str) -> str:
    """Membersihkan whitespace dan indentasi agar HTML tidak dianggap code block oleh Markdown."""
    return "".join(line.strip() for line in raw.splitlines() if line.strip())


def render_home_view(on_navigate=None):
    parts = APP_TAGLINE.split(",")
    headline_main = parts[0].strip() if len(parts) > 0 else APP_TAGLINE
    headline_accent = parts[1].strip() if len(parts) > 1 else "Jaga Lingkungan"

    hero_html = f"""
    <div class="hero">
        <div class="hero-eyebrow">✨ Deep Learning • Transfer Learning MobileNetV2</div>
        <div class="hero-title">{headline_main},<br><span>{headline_accent}</span></div>
        <p>
            Unggah foto atau gunakan kamera secara langsung. <b>B3Vision</b> mengidentifikasi
            7 kategori limbah secara akurat, memisahkan <b>Limbah B3 (Berbahaya)</b> dari
            <b>Sampah Daur Ulang</b>, serta menyajikan panduan SOP penanganan sesuai regulasi K3.
        </p>
        <div class="hero-stats-grid">
            <div class="hero-stat-item">
                <div class="hero-stat-val">7 Kelas</div>
                <div class="hero-stat-lbl">6 B3 &amp; 1 Non-B3</div>
            </div>
            <div class="hero-stat-item">
                <div class="hero-stat-val">90,25%</div>
                <div class="hero-stat-lbl">Akurasi Pengujian</div>
            </div>
            <div class="hero-stat-item">
                <div class="hero-stat-val">5.287</div>
                <div class="hero-stat-lbl">Citra Terkurasi</div>
            </div>
            <div class="hero-stat-item">
                <div class="hero-stat-val">REST API</div>
                <div class="hero-stat-lbl">FastAPI + Keras</div>
            </div>
        </div>
    </div>
    """
    st.markdown(_clean_html(hero_html), unsafe_allow_html=True)

    st.write("")
    _, mid, _ = st.columns([1.2, 1.1, 1.2])
    with mid:
        if on_navigate:
            st.button(
                "🚀  Mulai Analisis Sekarang →",
                key="cta_home_to_predict",
                type="primary",
                use_container_width=True,
                on_click=on_navigate,
                args=("Analisis",),
            )
        else:
            if st.button("🚀  Mulai Analisis Sekarang →", type="primary", use_container_width=True):
                st.session_state["active_tab"] = "Analisis"
                st.rerun()

    # 4 Langkah Cara Kerja
    st.markdown('<div class="section-title anim-fade-1">Cara Kerja B3Vision</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub anim-fade-1">Empat tahapan otomatis dari tangkapan kamera hingga rekomendasi SOP</div>',
        unsafe_allow_html=True,
    )

    steps = [
        ("LANGKAH 01", "📸", "Unggah / Potret Citra",
         "Pilih berkas foto limbah (JPG, PNG, WEBP) dari perangkat atau ambil foto langsung melalui webcam/kamera."),
        ("LANGKAH 02", "⚡", "Kirim ke REST API",
         "Saat tombol Analisis ditekan, citra dikirim ke endpoint FastAPI dan dinormalisasi ke tensor 224×224 piksel."),
        ("LANGKAH 03", "🧠", "Inferensi MobileNetV2",
         "Model Transfer Learning MobileNetV2 mengekstraksi fitur visual dan menghitung probabilitas ke-7 kelas limbah."),
        ("LANGKAH 04", "🛡️", "Diagnosa & SOP Aman",
         "Sistem menampilkan status bahaya (B3 / Non-B3), skor keyakinan, dampak lingkungan, dan prosedur penanganan."),
    ]

    cards_html = "".join(
        _clean_html(f"""
        <div class="step-card">
            <div class="step-top-row">
                <span class="step-num">{num}</span>
                <span class="step-icon">{icon}</span>
            </div>
            <div class="step-title">{title}</div>
            <div class="step-desc">{desc}</div>
        </div>
        """)
        for num, icon, title, desc in steps
    )

    st.markdown(_clean_html(f'<div class="steps-grid anim-fade-2">{cards_html}</div>'), unsafe_allow_html=True)

    # Ringkasan Edukasi B3 vs Non-B3
    compare_html = """
    <div class="compare-grid anim-fade-3">
        <div class="compare-card b3-box">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                <span style="font-size:1.4rem;">☣️</span>
                <span style="font-weight:800;font-size:1.05rem;color:#991B1B;">6 Kategori Limbah B3 (Berbahaya)</span>
            </div>
            <p style="margin:0;color:#475569;font-size:0.9rem;line-height:1.6;">
                Mencakup <b>Baterai &amp; Akumulator</b>, <b>Kaleng Aerosol</b>, <b>Kaca Cokelat Farmasi</b>,
                <b>Pecahan Kaca Hijau</b>, <b>Lampu Bohlam/Vial</b>, serta <b>Residu Medis Infeksius</b>.
                Wajib dipisahkan agar tidak mencemari air tanah atau melukai petugas kebersihan.
            </p>
        </div>
        <div class="compare-card nonb3-box">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                <span style="font-size:1.4rem;">🌿</span>
                <span style="font-weight:800;font-size:1.05rem;color:#065F46;">1 Kategori Non-B3 (Kontrol Daur Ulang)</span>
            </div>
            <p style="margin:0;color:#475569;font-size:0.9rem;line-height:1.6;">
                Mencakup kemasan <b>Plastik Daur Ulang (PET/HDPE)</b> bersih sebagai pembanding negatif
                (<i>negative control</i>). Sampah pada kategori ini aman dikelola melalui jalur Bank Sampah
                atau daur ulang sirkular.
            </p>
        </div>
    </div>
    """
    st.markdown(_clean_html(compare_html), unsafe_allow_html=True)