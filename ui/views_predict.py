import hashlib
import streamlit as st

from core.api_client import predict_via_api, check_api_health
from config.settings import OFFICIAL_DISCLAIMER, API_URL, CLASSES


def _clean_html(raw: str) -> str:
    """Membersihkan whitespace dan indentasi agar HTML tidak dianggap code block oleh Markdown."""
    return "".join(line.strip() for line in raw.splitlines() if line.strip())


def _set_source(src: str):
    st.session_state["active_src"] = src


def _bar(pct: float, color: str) -> str:
    width_val = max(min(float(pct), 100.0), 1.0)
    return f'<div class="bar"><div style="width:{width_val:.1f}%;background:{color};"></div></div>'


def _render_result(result: dict):
    state = result.get("status_state", "UNCERTAIN")
    conf = float(result.get("confidence", 0.0))
    top_id = result.get("top_class_id", result.get("label", ""))
    class_meta = CLASSES.get(top_id, {})

    icon = class_meta.get("icon", "♻️")
    hazard_level = result.get("hazard_level") or class_meta.get("hazard_level", "Perlu Perhatian")
    env_impact = result.get("environmental_impact") or class_meta.get("environmental_impact", "")

    if state == "B3_HAZARDOUS":
        kind, pill, color = "b3", "☣️ Limbah B3 — Berbahaya", "#DC2626"
    elif state == "NON_B3_SAFE":
        kind, pill, color = "nonb3", "🌿 Non-B3 — Dapat Didaur Ulang", "#059669"
    else:
        kind, pill, color = "unsure", "⚠️ Hasil Kurang Yakin (< 60%)", "#D97706"

    others = [d for d in result.get("distribution", []) if d["class_id"] != top_id][:3]
    others_html = "".join(
        f'<div class="other-row"><span class="name">{d["name"]}</span>'
        f'{_bar(d["confidence"], "#94A3B8")}<span class="val">{d["confidence"]:.1f}%</span></div>'
        for d in others
    )

    unsure_msg = ""
    if state == "UNCERTAIN":
        unsure_msg = (
            '<div class="avoid-item" style="background:#FFFBEB;color:#78350F;border-color:#FDE68A;margin-top:16px;">'
            '<span class="ico">⚠️</span><div>Skor keyakinan di bawah ambang batas <b>60%</b>. '
            'Disarankan memotret ulang objek limbah di tempat terang, fokus jelas, dan latar tidak ramai.</div></div>'
        )

    impact_html = ""
    if env_impact:
        impact_html = (
            f'<div class="impact-box">'
            f'<b>🌍 Dampak Lingkungan &amp; Kesehatan:</b><br>{env_impact}'
            f'</div>'
        )

    latency_ms = result.get("latency_ms", 0)
    model_ver = result.get("model_version", "v1.0-mobilenetv2")
    fname = result.get("filename", "image.jpg")
    latency_info = (
        f'<div style="display:flex;flex-wrap:wrap;gap:12px;font-size:0.76rem;color:#64748B;'
        f'margin-top:16px;border-top:1px dashed #E2E8F0;padding-top:10px;">'
        f'<span>⏱️ Latensi API: <b>{latency_ms} ms</b></span>'
        f'<span>🧠 Model: <b>{model_ver}</b></span>'
        f'<span>📄 Berkas: <b>{fname}</b></span>'
        f'</div>'
    )

    result_card_html = f"""
    <div class="result-card {kind}">
        <div class="pill-row">
            <span class="pill {kind}">{pill}</span>
            <span class="hazard-pill">⚡ Sifat: {hazard_level}</span>
        </div>
        <div class="result-name">{icon} {result.get("class_name", top_id)}</div>
        <div class="result-desc">{result.get("description", "")}</div>
        {impact_html}
        <div class="conf-row">
            <span class="conf-label">Tingkat Keyakinan Prediksi (Confidence Score)</span>
            <span class="conf-value">{conf:.1f}%</span>
        </div>
        {_bar(conf, color)}
        {unsure_msg}
        {'<div style="margin-top:22px;font-weight:700;font-size:.84rem;color:#64748B;margin-bottom:10px;">Distribusi Kemungkinan Kelas Lainnya</div>' + others_html if others else ''}
        {latency_info}
    </div>
    """
    st.markdown(_clean_html(result_card_html), unsafe_allow_html=True)

    # Kartu Saran SOP & Larangan
    advice = result.get("sop_actions", [])
    avoid = result.get("prohibitions", [])
    if advice or avoid:
        advice_html = "".join(
            f'<div class="advice-item"><span class="ico">✓</span><div>{a}</div></div>' for a in advice
        )
        avoid_html = "".join(
            f'<div class="avoid-item"><span class="ico">✕</span><div>{a.replace("DILARANG ", "Jangan ")}</div></div>'
            for a in avoid
        )
        sop_card_html = f"""
        <div class="result-card">
            <div style="font-size:1.05rem;font-weight:800;color:var(--ink);margin:0 0 12px;">
                💡 Prosedur Penanganan Aman (SOP)
            </div>
            {advice_html}
            {'<div style="font-size:1.05rem;font-weight:800;color:var(--ink);margin:18px 0 12px;">🚫 Larangan Keras (Hindari)</div>' + avoid_html if avoid else ''}
            <div class="note">🛡️ <b>Catatan Keselamatan:</b> {OFFICIAL_DISCLAIMER}</div>
        </div>
        """
        st.markdown(_clean_html(sop_card_html), unsafe_allow_html=True)


def render_predict_view():
    is_online, health_msg = check_api_health(API_URL)
    badge_class = "online" if is_online else "offline"

    page_head_html = f"""
    <div class="page-head">
        <div>
            <div class="page-head-title">Analisis Citra Limbah</div>
            <p>Pilih gambar limbah melalui unggahan berkas atau kamera, lalu klik tombol <b>Analisis</b>.</p>
        </div>
        <div class="api-badge {badge_class}">
            <span class="api-badge-dot"></span>
            <span>Backend API: <b>{health_msg}</b></span>
        </div>
    </div>
    """
    st.markdown(_clean_html(page_head_html), unsafe_allow_html=True)

    col_in, col_out = st.columns([1, 1.15], gap="large")

    # ---------------- Kolom Kiri: Input Citra ----------------
    with col_in:
        st.markdown(
            '<div class="input-panel-header">📥 1. Pilih Sumber Gambar Limbah</div>',
            unsafe_allow_html=True,
        )
        tab_up, tab_cam = st.tabs(["📁  Unggah Berkas", "📸  Kamera Langsung"])
        with tab_up:
            uploaded = st.file_uploader(
                "Pilih gambar limbah (JPG, JPEG, PNG, WEBP)",
                type=["jpg", "jpeg", "png", "webp"],
                key="uploader",
                on_change=_set_source,
                args=("upload",),
            )
        with tab_cam:
            camera = st.camera_input(
                "Arahkan kamera ke objek limbah lalu ambil foto",
                key="camera",
                on_change=_set_source,
                args=("camera",),
            )

        src = st.session_state.get("active_src")
        image_file, filename = None, None
        if src == "camera" and camera is not None:
            image_file, filename = camera, "kamera_langsung.jpg"
        elif uploaded is not None:
            image_file, filename = uploaded, uploaded.name
        elif camera is not None:
            image_file, filename = camera, "kamera_langsung.jpg"

        image_bytes = image_file.getvalue() if image_file is not None else None
        image_id = hashlib.md5(image_bytes).hexdigest() if image_bytes else None

        # Reset hasil sebelumnya jika pengguna mengganti atau menghapus gambar
        if st.session_state.get("result_for") != image_id:
            st.session_state.pop("result", None)
            st.session_state.pop("api_error", None)

        # Tampilkan pratinjau gambar beserta ukuran file (Tanpa Auto-Analisis)
        if image_bytes:
            size_kb = len(image_bytes) / 1024.0
            if src != "camera" or camera is None:
                st.image(image_bytes, use_container_width=True)
            preview_meta_html = f"""
            <div class="preview-meta-bar">
                <span>📎 <b>{filename}</b> ({size_kb:.1f} KB)</span>
                <span style="color:#059669;font-weight:700;">✓ Siap Dianalisis</span>
            </div>
            """
            st.markdown(_clean_html(preview_meta_html), unsafe_allow_html=True)

        analyze = st.button(
            "🔍  Analisis Gambar Sekarang",
            type="primary",
            use_container_width=True,
            disabled=(image_bytes is None),
        )

        # Eksekusi inferensi via REST API hanya saat tombol diklik
        if analyze and image_bytes:
            st.session_state.pop("result", None)
            st.session_state.pop("api_error", None)

            with st.spinner("Mengirim gambar ke REST API & menjalankan inferensi MobileNetV2..."):
                result = predict_via_api(image_bytes, filename=filename, api_url=API_URL)

            if result.get("status") == "success":
                st.session_state["result"] = result
                st.session_state["result_for"] = image_id
                st.session_state.pop("api_error", None)
                st.rerun()
            else:
                err_msg = result.get("message", "Terjadi kesalahan inferensi di server API.")
                st.session_state["api_error"] = err_msg
                st.session_state["result_for"] = image_id
                st.session_state.pop("result", None)
                st.rerun()

    # ---------------- Kolom Kanan: Output Diagnosa ----------------
    with col_out:
        st.markdown(
            '<div class="input-panel-header">📊 2. Hasil Diagnosa &amp; Panduan SOP</div>',
            unsafe_allow_html=True,
        )
        result = st.session_state.get("result")
        api_error = st.session_state.get("api_error")

        # Keadaan 1: Success
        if result:
            _render_result(result)
            if st.button("🔄  Analisis Foto Lain", use_container_width=True):
                st.session_state.pop("result", None)
                st.session_state.pop("result_for", None)
                st.session_state.pop("api_error", None)
                st.session_state.pop("active_src", None)
                st.rerun()

        # Keadaan 2: Error
        elif api_error:
            st.error(f"❌ **Gagal Melakukan Analisis via REST API** — {api_error}")
            error_card_html = """
            <div class="result-card" style="border-top: 5px solid #DC2626; margin-top: 14px;">
                <div style="font-size:1.02rem;font-weight:800;color:#DC2626;margin:0 0 10px;">
                    🛠️ Panduan Mengaktifkan Backend API:
                </div>
                <ol style="margin: 0; padding-left: 20px; color: #475569; font-size: 0.9rem; line-height: 1.65;">
                    <li>Buka terminal baru pada direktori proyek <code>Klasifikasi_limbahB3</code>, lalu jalankan:<br>
                        <code style="background: #F1F5F9; padding: 4px 8px; border-radius: 6px; font-weight: 700; color: #0F172A; display: inline-block; margin-top: 4px;">uvicorn app.main:app --reload --port 8000</code>
                    </li>
                    <li style="margin-top: 8px;">Pastikan berkas model <code>models/mobilenetv2_limbah_b3.keras</code> sudah terpasang.</li>
                    <li style="margin-top: 8px;">Setelah badge status di kanan atas berubah menjadi <b>Hijau (Siap)</b>, klik kembali tombol <b>🔍 Analisis Gambar Sekarang</b>.</li>
                </ol>
            </div>
            """
            st.markdown(_clean_html(error_card_html), unsafe_allow_html=True)

        # Keadaan 3: Idle (Menunggu Input / Klik Tombol)
        else:
            status_hint = (
                "Gambar sudah dipilih! Silakan tekan tombol <b>🔍 Analisis Gambar Sekarang</b> di sebelah kiri."
                if image_bytes
                else "Unggah berkas gambar atau ambil foto limbah di panel sebelah kiri, lalu tekan tombol <b>Analisis</b>."
            )
            icon_idle = "✅" if image_bytes else "🖼️"
            title_idle = "Gambar Siap Dianalisis" if image_bytes else "Belum Ada Hasil Analisis"

            empty_state_html = f"""
            <div class="empty-state">
                <div class="big">{icon_idle}</div>
                <div style="font-weight:800;color:#0F172A;margin-bottom:6px;font-size:1.15rem;">{title_idle}</div>
                <div style="max-width:440px;margin:0 auto;font-size:0.92rem;line-height:1.55;">{status_hint}</div>
                <div class="tips-grid">
                    <div class="tip-box">
                        <b>💡 Pencahayaan Jelas</b>
                        Pastikan objek limbah terlihat terang dan tidak tertutup bayangan gelap.
                    </div>
                    <div class="tip-box">
                        <b>🎯 Fokus di Tengah</b>
                        Posisikan satu jenis limbah di bagian tengah bingkai foto.
                    </div>
                    <div class="tip-box">
                        <b>🔒 Manual &amp; Aman</b>
                        Prediksi hanya diproses ke server saat tombol Analisis ditekan.
                    </div>
                </div>
            </div>
            """
            st.markdown(_clean_html(empty_state_html), unsafe_allow_html=True)