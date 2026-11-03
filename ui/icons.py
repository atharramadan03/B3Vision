"""
Modul ikon vektor SVG resmi Lucide Icons (lucide.dev) untuk B3Vision.
Menyediakan SVG murni yang ringan, presisi (stroke 2px), dan bebas dari emoji / AI slop.
"""

# Kamus SVG resmi Lucide Icons (viewBox 0 0 24 24)
LUCIDE_ICONS = {
    # 1. Baterai (battery)
    "battery": (
        '<rect width="16" height="10" x="2" y="7" rx="2" ry="2"/>'
        '<line x1="22" x2="22" y1="11" y2="13"/>'
        '<line x1="6" x2="6" y1="11" y2="13"/>'
    ),
    # 2. Botol Kaca Cokelat Farmasi / Kimia (flask-conical)
    "brown-glass": (
        '<path d="M10 2v7.527a2 2 0 0 1-.211.896L4.72 20.55a1 1 0 0 0 .9 1.45h12.76a1 1 0 0 0 .9-1.45l-5.069-10.127A2 2 0 0 1 14 9.527V2"/>'
        '<path d="M8.5 2h7"/>'
        '<path d="M7 16h10"/>'
    ),
    # 3. Kaca Hijau / Beling Botol (wine)
    "green-glass": (
        '<path d="M8 22h8"/>'
        '<path d="M7 10h10"/>'
        '<path d="M12 15v7"/>'
        '<path d="M12 15a5 5 0 0 0 5-5c0-2-.5-4-2-8H9c-1.5 4-2 6-2 8a5 5 0 0 0 5 5Z"/>'
    ),
    # 4. Kaleng Logam Aerosol (spray-can)
    "metal": (
        '<path d="M8 8v12a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2V8"/>'
        '<path d="M9 8V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v3"/>'
        '<line x1="12" x2="12" y1="3" y2="1"/>'
        '<line x1="8" x2="16" y1="8" y2="8"/>'
        '<circle cx="12" cy="14" r="1.5"/>'
    ),
    # 5. Kaca Bening / Lampu Neon Bohlam (lightbulb)
    "white-glass": (
        '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/>'
        '<path d="M9 18h6"/>'
        '<path d="M10 22h4"/>'
    ),
    # 6. Residu Medis Infeksius (biohazard)
    "trash": (
        '<circle cx="12" cy="12" r="2"/>'
        '<path d="M12 12a5 5 0 0 0-4-2.5 5 5 0 1 0-2.3 9.4 5 5 0 0 0 6.3-4.4"/>'
        '<path d="M12 12a5 5 0 0 0 4-2.5 5 5 0 1 1 2.3 9.4 5 5 0 0 1-6.3-4.4"/>'
        '<path d="M12 12a5 5 0 0 0 0-5 5 5 0 1 0-8.6 0 5 5 0 0 0 8.6 5"/>'
    ),
    # 7. Sampah Organik (leaf)
    "biological": (
        '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/>'
        '<path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>'
    ),
    # 8. Kardus Karton (package)
    "cardboard": (
        '<path d="m7.5 4.27 9 5.15"/>'
        '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/>'
        '<path d="m3.3 7 8.7 5 8.7-5"/>'
        '<path d="M12 22V12"/>'
    ),
    # 9. Pakaian / Tekstil (shirt)
    "clothes": (
        '<path d="M20.38 3.46 16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.47a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.47a2 2 0 0 0-1.34-2.23z"/>'
    ),
    # 10. Kertas Daur Ulang (file-text)
    "paper": (
        '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/>'
        '<path d="M14 2v4a2 2 0 0 0 2 2h4"/>'
        '<path d="M10 9H8"/>'
        '<path d="M16 13H8"/>'
        '<path d="M16 17H8"/>'
    ),
    # 11. Plastik Daur Ulang (recycle)
    "plastic": (
        '<path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881 1.785 1.785 0 0 1-.004-1.784L7.196 9.5"/>'
        '<path d="M11 19h8.203a1.83 1.83 0 0 0 1.556-.89 1.784 1.784 0 0 0 0-1.775l-1.226-2.12"/>'
        '<path d="m14 16-3 3 3 3"/>'
        '<path d="M8.293 13.596 5.617 8.97a1.83 1.83 0 0 1 0-1.78A1.785 1.785 0 0 1 7.196 6.3L11.5 6.29"/>'
        '<path d="m9.5 9.5-3-3 3-3"/>'
        '<path d="M15.707 10.404 18.383 5.78a1.83 1.83 0 0 0 0-1.78 1.785 1.785 0 0 0-1.579-.89H12.5"/>'
        '<path d="m14.5 3.5 3 3-3 3"/>'
    ),
    # 12. Sepatu / Alas Kaki (footprints)
    "shoes": (
        '<path d="M4 16v-2.38C4 11.5 2.97 10.5 3 8c.03-2.72 1.49-6 4.5-6C9.37 2 10 3.8 10 5.5c0 3.11-2 5.66-2 8.5v2"/>'
        '<path d="M20 20v-2.38c0-2.12 1.03-3.12 1-5.62-.03-2.72-1.49-6-4.5-6C14.63 6 14 7.8 14 9.5c0 3.11 2 5.66 2 8.5v2"/>'
        '<path d="M4 20h4"/>'
        '<path d="M16 22h4"/>'
    ),
    # Ikon UI Pembantu
    "sun": (
        '<circle cx="12" cy="12" r="4"/>'
        '<path d="M12 2v2"/>'
        '<path d="M12 20v2"/>'
        '<path d="m4.93 4.93 1.41 1.41"/>'
        '<path d="m17.66 17.66 1.41 1.41"/>'
        '<path d="M2 12h2"/>'
        '<path d="M20 12h2"/>'
        '<path d="m6.34 17.66-1.41 1.41"/>'
        '<path d="m19.07 4.93-1.41 1.41"/>'
    ),
    "target": (
        '<circle cx="12" cy="12" r="10"/>'
        '<line x1="22" x2="18" y1="12" y2="12"/>'
        '<line x1="6" x2="2" y1="12" y2="12"/>'
        '<line x1="12" x2="12" y1="6" y2="2"/>'
        '<line x1="12" x2="12" y1="22" y2="18"/>'
    ),
    "shield-check": (
        '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>'
        '<path d="m9 12 2 2 4-4"/>'
    ),
    "image-placeholder": (
        '<rect width="18" height="18" x="3" y="3" rx="2" ry="2"/>'
        '<circle cx="9" cy="9" r="2"/>'
        '<path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>'
    ),
    "cpu": (
        '<rect width="16" height="16" x="4" y="4" rx="2"/>'
        '<rect width="6" height="6" x="9" y="9" rx="1"/>'
        '<path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/>'
        '<path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/>'
    ),
    "alert-triangle": (
        '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>'
        '<line x1="12" x2="12" y1="9" y2="13"/>'
        '<line x1="12" x2="12.01" y1="17" y2="17"/>'
    ),
    "check-circle": (
        '<circle cx="12" cy="12" r="10"/>'
        '<path d="m9 12 2 2 4-4"/>'
    ),
    "check": (
        '<path d="M20 6 9 17l-5-5"/>'
    ),
    "x": (
        '<path d="M18 6 6 18"/>'
        '<path d="m6 6 12 12"/>'
    ),
    "recycle": (
        '<path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881 1.785 1.785 0 0 1-.004-1.784L7.196 9.5"/>'
        '<path d="M11 19h8.2a1.8 1.8 0 0 0 1.565-.89 1.79 1.79 0 0 0 .015-1.78l-3.92-6.83"/>'
        '<path d="m14 16-3 3 3 3"/>'
        '<path d="M8.2 9.5 5 15"/>'
        '<path d="m13.5 4.5 3.05 5.3a2 2 0 0 1-.05 2"/>'
        '<path d="m14.5 9-3-3-3 3"/>'
    )
}


def render_lucide_svg(icon_name: str, size: int = 20, stroke_width: float = 2.0, color: str = "currentColor", extra_class: str = "") -> str:
    """Merender icon Lucide resmi ke format string SVG inline."""
    body = LUCIDE_ICONS.get(icon_name, LUCIDE_ICONS["image-placeholder"])
    cls_attr = f' class="{extra_class}"' if extra_class else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round"{cls_attr}>{body}</svg>'
    )

