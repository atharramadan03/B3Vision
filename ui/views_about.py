import streamlit as st
from config.settings import APP_TITLE, CLASSES
from ui.icons import render_lucide_svg


def _clean_html(raw: str) -> str:
    """Membersihkan whitespace dan indentasi agar HTML tidak dianggap code block oleh Markdown."""
    return "".join(line.strip() for line in raw.splitlines() if line.strip())


# Definisi ringkas & padat agar seluruh kartu sejajar presisi
CLASS_CONCISE_INFO = {
    "battery": {
        "desc": "Baterai kering (AA/AAA), aki basah, baterai ponsel, dan baterai jam.",
        "impact": "Mengandung logam berat merkuri, timbal, dan kadmium beracun."
    },
    "brown-glass": {
        "desc": "Botol sirup obat farmasi, reagen kimia, dan botol kaca amber.",
        "impact": "Residu aktif kimiawi dapat mencemari air dan ekosistem tanah."
    },
    "green-glass": {
        "desc": "Pecahan botol kaca hijau dan pecahan beling tajam industri.",
        "impact": "Berbahaya secara fisik, melukai manusia serta hewan liar."
    },
    "metal": {
        "desc": "Kaleng obat nyamuk, cat semprot, deodoran, dan kemasan bertekanan.",
        "impact": "Gas propelan bertekanan sisa mudah memicu ledakan lingkungan."
    },
    "white-glass": {
        "desc": "Lampu neon tubular (TL), bohlam CFL/LED, dan botol vial medis.",
        "impact": "Mengandung gas uap merkuri beracun yang cepat menguap."
    },
    "trash": {
        "desc": "Masker medis, perban luka, sarung tangan, dan kapas antiseptik.",
        "impact": "Menyebarkan bakteri patogen, virus berbahaya, dan infeksi."
    },
    "biological": {
        "desc": "Sisa sayur, buah, sisa makanan dapur, dan dedaunan kering.",
        "impact": "Mudah terurai alami; ideal diolah menjadi kompos atau maggot."
    },
    "cardboard": {
        "desc": "Kardus boks cokelat, karton duplex, dan tabung karton gulung.",
        "impact": "Dapat didaur ulang menjadi bubur kertas pulp berulang kali."
    },
    "clothes": {
        "desc": "Baju bekas, celana kain, jaket, dan sisa serat tekstil majun.",
        "impact": "Serat sintetis lambat terurai; manfaatkan kembali atau donasikan."
    },
    "paper": {
        "desc": "Kertas HVS, koran, majalah, buku tulis, dan amplop surat kering.",
        "impact": "Daur ulang menghemat penebangan pohon kayu dan konsumsi air."
    },
    "plastic": {
        "desc": "Botol minum PET, wadah detergen HDPE, dan gelas plastik bersih.",
        "impact": "Butuh ratusan tahun terurai; pilah untuk daur ulang sirkular."
    },
    "shoes": {
        "desc": "Sepatu kets, sandal karet, dan alas kaki kombinasi sol kanvas.",
        "impact": "Sol karet sintetis tahan lama; dapat disol atau direparasi ulang."
    }
}


def render_about_view(on_navigate=None):
    page_head_html = """
    <div class="page-head">
        <div>
            <div class="page-head-title">Tentang B3Vision</div>
            <p>Sistem klasifikasi citra 12 kelas limbah B3 dan Non-B3 berbasis Transfer Learning MobileNetV2 &amp; FastAPI.</p>
        </div>
    </div>
    """
    st.markdown(_clean_html(page_head_html), unsafe_allow_html=True)

    # 1. Ringkasan Aplikasi & Performa Model
    icon_shield = render_lucide_svg("shield-check", size=18, stroke_width=2.2, color="#059669")
    summary_card_html = f"""
    <div class="card anim-fade-1">
        <div style="font-size:1.05rem;font-weight:800;color:var(--ink);margin:0 0 8px;display:flex;align-items:center;gap:8px;">
            <span style="display:inline-flex;align-items:center;">{icon_shield}</span>
            <span>Mengenal {APP_TITLE} (12 Kategori Limbah)</span>
        </div>
        <p style="color:#475569;line-height:1.65;font-size:0.91rem;margin:0;">
            <strong>B3Vision</strong> adalah sistem cerdas klasifikasi citra berbasis deep learning yang dirancang
            untuk membantu masyarakat dan petugas kebersihan mengidentifikasi <strong>Limbah B3 (Bahan Berbahaya dan Beracun)</strong>
            serta membedakannya secara akurat dari <strong>Sampah Non-B3 (Daur Ulang, Organik, dan Tekstil)</strong>.
            Sistem ini memadukan frontend responsif <strong>Streamlit</strong> dengan backend
            <strong>FastAPI REST API</strong> yang menjalankan model <em>Transfer Learning MobileNetV2</em>.
        </p>
        <div class="hero-stats-grid" style="max-width:100%;margin-top:18px;">
            <div class="hero-stat-item">
                <div class="hero-stat-val">96,17%</div>
                <div class="hero-stat-lbl">Test Accuracy (1.567 Uji)</div>
            </div>
            <div class="hero-stat-item">
                <div class="hero-stat-val">94,46%</div>
                <div class="hero-stat-lbl">Macro Precision</div>
            </div>
            <div class="hero-stat-item">
                <div class="hero-stat-val">94,45%</div>
                <div class="hero-stat-lbl">Macro Recall</div>
            </div>
            <div class="hero-stat-item">
                <div class="hero-stat-val">94,35%</div>
                <div class="hero-stat-lbl">Macro F1-Score</div>
            </div>
        </div>
    </div>
    """
    st.markdown(_clean_html(summary_card_html), unsafe_allow_html=True)

    # 2. Katalog 12 Kategori Limbah (Tabbed & Grid 3-Kolom Sejajar Presisi)
    st.markdown(
        '<div class="section-title anim-fade-2" style="text-align:left; margin: 26px 0 4px;">Katalog 12 Kategori Limbah</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-sub anim-fade-2" style="text-align:left; margin-bottom: 14px;">Taksonomi 6 kelas Limbah B3 dan 6 kelas Non-B3 beserta karakteristik bahaya dan pengelolaannya:</div>',
        unsafe_allow_html=True,
    )

    tab_b3, tab_nonb3 = st.tabs(["Limbah B3 (6 Kategori)", "Non-B3 / Daur Ulang (6 Kategori)"])

    # Tab 1: 6 Kategori Limbah B3 (3 Kolom x 2 Baris)
    with tab_b3:
        b3_classes = [c for c in CLASSES.values() if c["category"] == "B3"]
        col1, col2, col3 = st.columns(3, gap="small")

        for idx, meta in enumerate(b3_classes):
            target_col = col1 if idx % 3 == 0 else (col2 if idx % 3 == 1 else col3)
            with target_col:
                cid = meta["id"]
                svg_icon = render_lucide_svg(cid, size=17, stroke_width=2.0, color="#DC2626")
                c_info = CLASS_CONCISE_INFO.get(cid, {"desc": meta['description'], "impact": meta.get('environmental_impact', '')})
                card_html = f"""
                <div class="compact-class-card" style="border-left: 3px solid #DC2626;">
                    <div>
                        <div class="compact-card-header">
                            <div class="compact-icon-box b3">{svg_icon}</div>
                            <div style="flex:1;min-width:0;">
                                <div class="compact-card-title">{meta['name']}</div>
                                <span class="compact-badge b3">Limbah B3</span>
                            </div>
                        </div>
                        <div class="compact-hazard">Sifat: <b>{meta.get('hazard_level', 'Tinggi')}</b></div>
                        <div class="compact-desc">{c_info['desc']}</div>
                    </div>
                    <div class="compact-impact"><b>Dampak:</b> {c_info['impact']}</div>
                </div>
                """
                st.markdown(_clean_html(card_html), unsafe_allow_html=True)

    # Tab 2: 6 Kategori Non-B3 (3 Kolom x 2 Baris)
    with tab_nonb3:
        nonb3_classes = [c for c in CLASSES.values() if c["category"] == "Non-B3"]
        col_nb1, col_nb2, col_nb3 = st.columns(3, gap="small")

        for idx, meta in enumerate(nonb3_classes):
            target_col = col_nb1 if idx % 3 == 0 else (col_nb2 if idx % 3 == 1 else col_nb3)
            with target_col:
                cid = meta["id"]
                svg_icon = render_lucide_svg(cid, size=17, stroke_width=2.0, color="#059669")
                c_info = CLASS_CONCISE_INFO.get(cid, {"desc": meta['description'], "impact": meta.get('environmental_impact', '')})
                card_html = f"""
                <div class="compact-class-card" style="border-left: 3px solid #059669;">
                    <div>
                        <div class="compact-card-header">
                            <div class="compact-icon-box nonb3">{svg_icon}</div>
                            <div style="flex:1;min-width:0;">
                                <div class="compact-card-title">{meta['name']}</div>
                                <span class="compact-badge nonb3">Non-B3</span>
                            </div>
                        </div>
                        <div class="compact-hazard" style="color:#047857;">Sifat: <b>{meta.get('hazard_level', 'Aman')}</b></div>
                        <div class="compact-desc">{c_info['desc']}</div>
                    </div>
                    <div class="compact-impact"><b>Pengelolaan:</b> {c_info['impact']}</div>
                </div>
                """
                st.markdown(_clean_html(card_html), unsafe_allow_html=True)

    # 3. Tahapan Pelatihan Model (Transfer Learning & Fine-Tuning)
    icon_pipeline = render_lucide_svg("cpu", size=18, stroke_width=2.0, color="#0F172A")
    training_pipeline_html = f"""
    <div class="training-pipeline-card anim-fade-3">
        <div style="font-size:1.02rem;font-weight:800;color:var(--ink);margin:0 0 4px;display:flex;align-items:center;gap:8px;">
            <span style="display:inline-flex;align-items:center;">{icon_pipeline}</span>
            <span>Tahapan Pelatihan Model (Transfer Learning &amp; Fine-Tuning)</span>
        </div>
        <p style="color:#64748B;font-size:0.85rem;margin:0 0 14px;">
            Pelatihan dijalankan secara bertahap pada 15.515 citra dataset untuk mencapai akurasi optimal 96,17%:
        </p>
        <div class="training-grid">
            <div class="stage-box">
                <div>
                    <span class="stage-badge p1">Tahap 1 • Feature Extraction</span>
                    <div class="stage-name">Pembekuan Base Model MobileNetV2</div>
                    <div class="stage-desc">
                        Lapisan dasar MobileNetV2 (ImageNet) dibekukan (<code>trainable=False</code>). Hanya dense head klasifikasi baru yang dilatih untuk mempelajari pola visual 12 kelas limbah tanpa merusak fitur dasar.
                    </div>
                </div>
                <div class="stage-specs">
                    <span class="stage-spec-tag">Optimizer: Adam</span>
                    <span class="stage-spec-tag">LR: 0.001</span>
                    <span class="stage-spec-tag">Epoch: 15</span>
                    <span class="stage-spec-tag">Dropout: 0.3 + 0.2</span>
                </div>
            </div>
            <div class="stage-box">
                <div>
                    <span class="stage-badge p2">Tahap 2 • Fine-Tuning</span>
                    <div class="stage-name">Pencairan 30 Layer Konvolusi Teratas</div>
                    <div class="stage-desc">
                        Membuka 30 lapisan konvolusi teratas MobileNetV2 dengan learning rate rendah (1e-4) untuk adaptasi mendalam pada tekstur spesifik limbah, mencapai akurasi pengujian puncak 96,17%.
                    </div>
                </div>
                <div class="stage-specs">
                    <span class="stage-spec-tag">Optimizer: Adam</span>
                    <span class="stage-spec-tag">LR: 0.0001</span>
                    <span class="stage-spec-tag">Epoch: 10</span>
                    <span class="stage-spec-tag">Akurasi: 96,17%</span>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(_clean_html(training_pipeline_html), unsafe_allow_html=True)

    # 4. Spesifikasi Arsitektur
    icon_arch = render_lucide_svg("cpu", size=18, stroke_width=2.0, color="#0F172A")
    arch_card_html = f"""
    <div class="card anim-fade-3" style="margin-top: 18px;">
        <div style="font-size:1.02rem;font-weight:800;color:var(--ink);margin:0 0 8px;display:flex;align-items:center;gap:8px;">
            <span style="display:inline-flex;align-items:center;">{icon_arch}</span>
            <span>Arsitektur Model &amp; REST API</span>
        </div>
        <p style="color:#475569;line-height:1.62;font-size:0.89rem;margin:0;">
            Model dibangun menggunakan arsitektur <b>MobileNetV2</b> (<i>ImageNet pre-trained weights</i>)
            dengan normalisasi <code>Rescaling(1./127.5, offset=-1.0)</code> dan custom head
            (<code>GlobalAveragePooling2D</code> → <code>BatchNormalization</code> → <code>Dropout(0.3)</code> →
            <code>Dense(128, ReLU)</code> → <code>Dropout(0.2)</code> → <code>Dense(12, Softmax)</code>).
            Inferensi dilayani secara terpisah oleh server <b>FastAPI</b> melalui endpoint
            <code>POST /api/v1/predict</code> dan monitoring status di <code>GET /health</code>.
        </p>
    </div>
    """
    st.markdown(_clean_html(arch_card_html), unsafe_allow_html=True)

    _, mid, _ = st.columns([1.2, 1.1, 1.2])
    with mid:
        if on_navigate:
            st.button(
                "Mulai Analisis Citra Sekarang →",
                key="cta_about_to_predict",
                type="primary",
                use_container_width=True,
                on_click=on_navigate,
                args=("Analisis",),
            )
