import streamlit as st

st.set_page_config(
    page_title="B3Vision • Klasifikasi Limbah B3 (MobileNetV2)",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from ui.styles import apply_custom_css
from ui.views_home import render_home_view
from ui.views_predict import render_predict_view
from ui.views_about import render_about_view


def _switch_tab(tab_name: str):
    """Callback perpindahan tab yang instan dan bebas konflik state."""
    st.session_state["active_tab"] = tab_name


def render_top_navbar():
    """Merender Top Navigation Bar modern yang interaktif dan responsif."""
    if "active_tab" not in st.session_state:
        st.session_state["active_tab"] = "Beranda"

    active = st.session_state["active_tab"]

    st.markdown('<div class="navbar-wrapper">', unsafe_allow_html=True)
    col_brand, col_nav = st.columns([1, 1.2], vertical_alignment="center")

    with col_brand:
        st.markdown(
            '<div class="top-nav-brand">'
            '<span class="brand-icon">♻️</span>'
            '<span class="brand-text">B3Vision</span>'
            '</div>',
            unsafe_allow_html=True,
        )

    with col_nav:
        nav_cols = st.columns(3, gap="small")
        tabs = [
            ("Beranda", "🏠 Beranda"),
            ("Analisis", "🔍 Analisis"),
            ("Tentang", "ℹ️ Tentang"),
        ]
        for col, (tab_id, tab_label) in zip(nav_cols, tabs):
            with col:
                is_active = active == tab_id
                st.button(
                    tab_label,
                    key=f"nav_btn_{tab_id}",
                    type="primary" if is_active else "secondary",
                    use_container_width=True,
                    on_click=_switch_tab,
                    args=(tab_id,),
                )

    st.markdown('</div><div class="top-nav-divider"></div>', unsafe_allow_html=True)


def main():
    apply_custom_css()
    render_top_navbar()

    active_tab = st.session_state.get("active_tab", "Beranda")

    # Container halaman dengan animasi transisi halus setiap pindah tab
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)
    if active_tab == "Analisis":
        render_predict_view()
    elif active_tab == "Tentang":
        render_about_view(on_navigate=_switch_tab)
    else:
        render_home_view(on_navigate=_switch_tab)
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()