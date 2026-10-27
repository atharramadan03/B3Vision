import streamlit as st
from config.settings import APP_TITLE, CLASSES


def _clean_html(raw: str) -> str:
    """Membersihkan whitespace dan indentasi agar HTML tidak dianggap code block oleh Markdown."""
    return "".join(line.strip() for line in raw.splitlines() if line.strip())


def render_about_view(on_navigate=None):
    page_head_html = """
    <div class="page-head">
        <div>
            <div class="page-head-title">Tentang B3Vision</div>
            <p>Sistem klasifikasi citra limbah B3 dan Non-B3 berbasis Transfer Learning MobileNetV2 &amp; FastAPI.</p>
        </div>
    </div>
    """
    st.markdown(_clean_html(page_head_html), unsafe_allow_html=True)

    # 1. Ringkasan Aplikasi & Performa Model
    summary_card_html = f"""
    <div class="card anim-fade-1">
        <div style="font-size:1.15rem;font-weight:800;color:var(--ink);margin:0 0 10px;">🌿 Mengenal {APP_TITLE}</div>
        <p style="color:#475569;line-height:1.68;font-size:0.95rem;margin:0;">
            <strong>B3Vision</strong> adalah aplikasi web pemilah limbah berbasis kecerdasan buatan yang dirancang
            untuk membantu masyarakat dan petugas pengelola sampah mengidentifikasi <strong>Limbah Bahan Berbahaya dan Beracun (B3)</strong>
            secara cepat dan akurat. Sistem ini memadukan antarmuka interaktif <strong>Streamlit</strong> dengan layanan
            backend <strong>FastAPI REST API</strong> yang menjalankan model <em>Transfer Learning MobileNetV2</em>.
        </p>
        <div class="hero-stats-grid" style="max-width:100%;margin-top:20px;">
            <div class="hero-stat-item">
                <div class="hero-stat-val">90,25%</div>
                <div class="hero-stat-lbl">Test Accuracy (513 Uji)</div>
            </div>
            <div class="hero-stat-item">
                <div class="hero-stat-val">91,32%</div>
                <div class="hero-stat-lbl">Macro Precision</div>
            </div>
            <div class="hero-stat-item">
                <div class="hero-stat-val">90,93%</div>
                <div class="hero-stat-lbl">Macro Recall</div>
            </div>
            <div class="hero-stat-item">
                <div class="hero-stat-val">90,84%</div>
                <div class="hero-stat-lbl">Macro F1-Score</div>
            </div>
        </div>
    </div>
    """
    st.markdown(_clean_html(summary_card_html), unsafe_allow_html=True)

    # 2. Katalog 7 Jenis Limbah
    st.markdown(
        '<div class="section-title anim-fade-2" style="text-align:left; margin: 32px 0 4px;">Katalog 7 Kategori Limbah</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-sub anim-fade-2" style="text-align:left; margin-bottom: 18px;">Rincian taksonomi 6 kelas Limbah B3 dan 1 kelas Non-B3 beserta karakteristik bahayanya:</div>',
        unsafe_allow_html=True,
    )

    # A. 6 Kategori Limbah B3
    st.markdown('<div class="category-subhead">🔴 6 Kategori Limbah B3 (Bahan Berbahaya &amp; Beracun)</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="medium")
    b3_classes = [c for c in CLASSES.values() if c["category"] == "B3"]

    for idx, meta in enumerate(b3_classes):
        target_col = col1 if idx < 3 else col2
        with target_col:
            chip_html = f"""
            <div class="class-chip">
                <div class="ico">{meta['icon']}</div>
                <div style="flex:1;">
                    <div class="t">
                        {meta['name']}
                        <span class="tag b3">Limbah B3</span>
                    </div>
                    <div style="font-size:0.75rem;font-weight:700;color:#DC2626;margin-top:3px;">
                        ⚡ Bahaya: {meta.get('hazard_level', 'Tinggi')}
                    </div>
                    <div class="d">{meta['description']}</div>
                    <div class="impact-mini"><b>Dampak:</b> {meta.get('environmental_impact', '')}</div>
                </div>
            </div>
            """
            st.markdown(_clean_html(chip_html), unsafe_allow_html=True)

    # B. 1 Kategori Non-B3
    st.markdown('<div class="category-subhead" style="color:#047857;">🟢 1 Kategori Non-B3 (Daur Ulang / Kontrol Negatif)</div>', unsafe_allow_html=True)
    non_b3_meta = CLASSES.get("plastic", {})
    non_b3_chip_html = f"""
    <div class="class-chip" style="border-left: 4px solid var(--primary);">
        <div class="ico">{non_b3_meta.get('icon', '♻️')}</div>
        <div style="flex:1;">
            <div class="t">
                {non_b3_meta.get('name', 'Plastik Daur Ulang')}
                <span class="tag nonb3">Non-B3</span>
            </div>
            <div style="font-size:0.75rem;font-weight:700;color:#059669;margin-top:3px;">
                ✓ Status: {non_b3_meta.get('hazard_level', 'Aman')}
            </div>
            <div class="d">{non_b3_meta.get('description', '')}</div>
            <div class="impact-mini"><b>Pengelolaan:</b> {non_b3_meta.get('environmental_impact', '')}</div>
        </div>
    </div>
    """
    st.markdown(_clean_html(non_b3_chip_html), unsafe_allow_html=True)

    # 3. Spesifikasi Arsitektur
    arch_card_html = """
    <div class="card anim-fade-3" style="margin-top: 22px;">
        <div style="font-size:1.1rem;font-weight:800;color:var(--ink);margin:0 0 10px;">⚙️ Arsitektur Model &amp; REST API</div>
        <p style="color:#475569;line-height:1.65;font-size:0.93rem;margin:0;">
            Model visi komputer dibangun menggunakan <b>MobileNetV2</b> (<i>ImageNet pre-trained weights</i>)
            dengan lapisan normalisasi internal <code>Rescaling(1./127.5, offset=-1.0)</code> dan <i>custom classification head</i>
            (<code>GlobalAveragePooling2D</code> → <code>BatchNormalization</code> → <code>Dropout(0.3)</code> →
            <code>Dense(128, ReLU)</code> → <code>Dropout(0.2)</code> → <code>Dense(7, Softmax)</code>).
            Berkas model <code>mobilenetv2_limbah_b3.keras</code> disajikan melalui endpoint
            <code>POST /api/v1/predict</code> dan <code>GET /health</code> pada server FastAPI.
        </p>
    </div>
    """
    st.markdown(_clean_html(arch_card_html), unsafe_allow_html=True)

    _, mid, _ = st.columns([1.2, 1.1, 1.2])
    with mid:
        if on_navigate:
            st.button(
                "🔍  Coba Analisis Gambar Sekarang →",
                key="cta_about_to_predict",
                type="primary",
                use_container_width=True,
                on_click=on_navigate,
                args=("Analisis",),
            )