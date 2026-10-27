import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

:root {
    --primary: #059669;
    --primary-dark: #047857;
    --primary-light: #10B981;
    --primary-soft: #ECFDF5;
    --primary-border: #A7F3D0;
    --ink: #0F172A;
    --ink-soft: #1E293B;
    --muted: #64748B;
    --muted-light: #94A3B8;
    --line: #E2E8F0;
    --line-soft: #F1F5F9;
    --surface: #FFFFFF;
    --bg: #F8FAFC;
    --danger: #DC2626;
    --danger-dark: #991B1B;
    --danger-soft: #FEF2F2;
    --danger-border: #FECACA;
    --warn: #D97706;
    --warn-dark: #92400E;
    --warn-soft: #FFFBEB;
    --warn-border: #FDE68A;
    --radius-xl: 24px;
    --radius-lg: 18px;
    --radius-md: 14px;
    --shadow-sm: 0 2px 8px -2px rgba(15, 23, 42, 0.05);
    --shadow-md: 0 10px 25px -5px rgba(15, 23, 42, 0.06), 0 4px 10px -3px rgba(15, 23, 42, 0.03);
    --shadow-lg: 0 20px 35px -10px rgba(15, 23, 42, 0.10), 0 8px 16px -6px rgba(15, 23, 42, 0.04);
    --shadow-emerald: 0 10px 25px -5px rgba(5, 150, 105, 0.28);
}

/* ---------- Global Typography & Reset ---------- */
html, body, [class*="css"], .stApp, .stMarkdown, button, input, textarea {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

code, pre {
    font-family: 'JetBrains Mono', monospace !important;
}

.stApp {
    background: radial-gradient(circle at 50% 0%, #EFFDF6 0%, #F8FAFC 45%, #F8FAFC 100%) !important;
}

/* Sembunyikan elemen bawaan Streamlit yang mengganggu kebersihan UI */
section[data-testid="stSidebar"],
div[data-testid="stSidebarCollapsedControl"],
button[data-testid="stExpandSidebarButton"],
#MainMenu, footer, .stDeployButton,
div[data-testid="stMainMenu"],
div[data-testid="stAppDeployButton"],
div[data-testid="stDecoration"] {
    display: none !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0.75rem !important;
}

.block-container {
    max-width: 1120px !important;
    padding-top: 1.2rem !important;
    padding-bottom: 4rem !important;
}

/* Sembunyikan link ikon anchor bawaan heading Streamlit */
[data-testid="stHeadingActionElements"],
[data-testid="stHeaderActionElements"],
a.header-anchor, a.anchor-link,
h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* ---------- Keyframe Animations ---------- */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(14px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes scaleIn {
    from {
        opacity: 0;
        transform: scale(0.97);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

@keyframes progressFill {
    from {
        width: 0%;
    }
}

@keyframes pulseRing {
    0% {
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.45);
    }
    70% {
        box-shadow: 0 0 0 7px rgba(16, 185, 129, 0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
    }
}

@keyframes pulseRingRed {
    0% {
        box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.45);
    }
    70% {
        box-shadow: 0 0 0 7px rgba(239, 68, 68, 0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(239, 68, 68, 0);
    }
}

@keyframes floatSlow {
    0%, 100% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(-6px);
    }
}

.page-transition {
    animation: fadeInUp 0.42s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.anim-fade-1 { animation: fadeInUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) 0.04s both; }
.anim-fade-2 { animation: fadeInUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) 0.10s both; }
.anim-fade-3 { animation: fadeInUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) 0.16s both; }

/* ---------- Top Navbar ---------- */
.top-nav-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 4px 0;
}
.brand-icon {
    font-size: 1.85rem;
    line-height: 1;
}
.brand-text {
    font-size: 1.55rem;
    font-weight: 800;
    color: var(--ink);
    letter-spacing: -0.03em;
}

.top-nav-divider {
    height: 1px;
    background: linear-gradient(90deg, rgba(226,232,240,0.2) 0%, rgba(203,213,225,0.85) 50%, rgba(226,232,240,0.2) 100%);
    margin: 14px 0 28px 0;
}

/* ---------- Buttons & Interactive Navbar Pills ---------- */
div.stButton > button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    padding: 0.58rem 1.15rem !important;
    transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
    cursor: pointer !important;
}

/* Active Tab / Primary Button */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid #047857 !important;
    box-shadow: 0 6px 16px -4px rgba(5, 150, 105, 0.35) !important;
}

div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 22px -4px rgba(5, 150, 105, 0.45) !important;
}

div.stButton > button[kind="primary"]:active {
    transform: translateY(0px) !important;
}

/* Inactive Tab / Secondary Button */
div.stButton > button[kind="secondary"] {
    background: #FFFFFF !important;
    color: #475569 !important;
    border: 1px solid var(--line) !important;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03) !important;
}

div.stButton > button[kind="secondary"]:hover {
    background: #F0FDF4 !important;
    color: var(--primary-dark) !important;
    border-color: var(--primary-border) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 14px -4px rgba(5, 150, 105, 0.14) !important;
}

div.stButton > button:disabled {
    background: #F1F5F9 !important;
    color: #94A3B8 !important;
    border-color: #E2E8F0 !important;
    box-shadow: none !important;
    transform: none !important;
    cursor: not-allowed !important;
}

/* ---------- Hero Section (Beranda) ---------- */
.hero {
    position: relative;
    text-align: center;
    padding: 54px 28px 42px;
    background: linear-gradient(180deg, rgba(209, 250, 229, 0.55) 0%, rgba(255, 255, 255, 0.92) 100%);
    border: 1px solid #D1FAE5;
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow-md);
    overflow: hidden;
    animation: scaleIn 0.45s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--primary-dark);
    background: #FFFFFF;
    border: 1px solid var(--primary-border);
    padding: 6px 16px;
    border-radius: 999px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(5, 150, 105, 0.08);
}

.hero-title {
    font-size: 2.95rem;
    font-weight: 800;
    line-height: 1.12;
    margin: 0 auto 16px;
    letter-spacing: -0.03em;
    color: var(--ink);
    max-width: 760px;
}

.hero-title span {
    background: linear-gradient(135deg, #059669 0%, #10B981 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    font-size: 1.08rem;
    color: var(--muted);
    max-width: 640px;
    margin: 0 auto 28px;
    line-height: 1.65;
}

/* Stat Strip inside Hero */
.hero-stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    max-width: 820px;
    margin: 0 auto;
    padding-top: 12px;
}

@media (max-width: 768px) {
    .hero-stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    .hero-title {
        font-size: 2.2rem;
    }
}

.hero-stat-item {
    background: rgba(255, 255, 255, 0.88);
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 12px 14px;
    text-align: center;
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.hero-stat-item:hover {
    transform: translateY(-2px);
    border-color: var(--primary-border);
}

.hero-stat-val {
    font-size: 1.25rem;
    font-weight: 800;
    color: var(--primary-dark);
    line-height: 1.2;
}

.hero-stat-lbl {
    font-size: 0.76rem;
    font-weight: 600;
    color: var(--muted);
    margin-top: 2px;
}

/* ---------- Section Heading ---------- */
.section-title {
    text-align: center;
    margin: 44px 0 6px;
    font-size: 1.55rem;
    font-weight: 800;
    color: var(--ink);
    letter-spacing: -0.02em;
}

.section-sub {
    text-align: center;
    color: var(--muted);
    font-size: 0.96rem;
    margin-bottom: 26px;
}

/* ---------- Step Cards (4 Langkah Cara Kerja) ---------- */
.steps-grid {
    display: grid !important;
    grid-template-columns: repeat(4, 1fr) !important;
    gap: 18px !important;
    align-items: stretch !important;
    margin-top: 14px !important;
    margin-bottom: 32px !important;
}

@media (max-width: 960px) {
    .steps-grid {
        grid-template-columns: repeat(2, 1fr) !important;
    }
}

@media (max-width: 580px) {
    .steps-grid {
        grid-template-columns: 1fr !important;
    }
}

.step-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 26px 22px;
    height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    box-sizing: border-box !important;
    box-shadow: var(--shadow-sm);
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    position: relative;
    overflow: hidden;
}

.step-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
    border-color: var(--primary-border);
}

.step-top-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
}

.step-num {
    padding: 5px 12px;
    border-radius: 999px;
    background: var(--primary-soft);
    color: var(--primary-dark);
    border: 1px solid var(--primary-border);
    font-weight: 800;
    font-size: 0.78rem;
    letter-spacing: 0.04em;
}

.step-icon {
    font-size: 1.55rem;
    line-height: 1;
}

.step-title {
    font-weight: 800;
    font-size: 1.06rem;
    color: var(--ink);
    margin-bottom: 8px;
    line-height: 1.35;
}

.step-desc {
    color: var(--muted);
    font-size: 0.9rem;
    line-height: 1.6;
    flex-grow: 1;
    margin: 0;
}

/* ---------- Info Banner Grid (Beranda & About) ---------- */
.compare-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    margin-top: 12px;
}

@media (max-width: 768px) {
    .compare-grid {
        grid-template-columns: 1fr;
    }
}

.compare-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 24px;
    box-shadow: var(--shadow-sm);
    transition: transform 0.22s ease, box-shadow 0.22s ease;
}

.compare-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-md);
}

.compare-card.b3-box {
    border-left: 5px solid var(--danger);
}

.compare-card.nonb3-box {
    border-left: 5px solid var(--primary);
}

/* ---------- Generic Card ---------- */
.card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius-lg);
    padding: 26px;
    margin-bottom: 20px;
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.22s ease, border-color 0.22s ease;
}

.card:hover {
    box-shadow: var(--shadow-md);
}

/* ---------- Page Header ---------- */
.page-head {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    margin-bottom: 22px;
}

.page-head-title {
    font-size: 1.95rem;
    font-weight: 800;
    margin-bottom: 4px;
    letter-spacing: -0.03em;
    color: var(--ink);
}

.page-head p {
    color: var(--muted);
    margin: 0;
    font-size: 0.98rem;
}

/* ---------- API Status Badge ---------- */
.api-badge {
    display: inline-flex;
    align-items: center;
    gap: 9px;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 7px 15px;
    border-radius: 999px;
    transition: all 0.2s ease;
}

.api-badge.online {
    background: #ECFDF5;
    color: #065F46;
    border: 1px solid #A7F3D0;
}

.api-badge.offline {
    background: #FEF2F2;
    color: #991B1B;
    border: 1px solid #FECACA;
}

.api-badge-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
}

.api-badge.online .api-badge-dot {
    background: #10B981;
    animation: pulseRing 2s infinite;
}

.api-badge.offline .api-badge-dot {
    background: #EF4444;
    animation: pulseRingRed 2s infinite;
}

/* ---------- Input Panel & Preview ---------- */
.input-panel-header {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 800;
    font-size: 1.02rem;
    color: var(--ink);
    margin-bottom: 10px;
}

.preview-meta-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #F1F5F9;
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 8px 12px;
    font-size: 0.8rem;
    color: #334155;
    margin: 8px 0 14px;
}

/* ---------- Result Card (Halaman Analisis) ---------- */
.result-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius-lg);
    padding: 26px;
    margin-bottom: 18px;
    box-shadow: var(--shadow-md);
    animation: fadeInUp 0.42s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.result-card.b3     { border-top: 5px solid var(--danger); }
.result-card.nonb3  { border-top: 5px solid var(--primary); }
.result-card.unsure { border-top: 5px solid var(--warn); }

.pill-row {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
}

.pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-weight: 700;
    font-size: 0.8rem;
    padding: 6px 14px;
    border-radius: 999px;
}

.pill.b3     { background: var(--danger-soft); color: var(--danger-dark); border: 1px solid var(--danger-border); }
.pill.nonb3  { background: var(--primary-soft); color: #065F46; border: 1px solid var(--primary-border); }
.pill.unsure { background: var(--warn-soft); color: var(--warn-dark); border: 1px solid var(--warn-border); }

.hazard-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-weight: 600;
    font-size: 0.76rem;
    padding: 5px 12px;
    border-radius: 999px;
    background: #F1F5F9;
    color: #334155;
    border: 1px solid #CBD5E1;
}

.result-name {
    font-size: 1.75rem;
    font-weight: 800;
    color: var(--ink);
    margin: 6px 0 6px;
    line-height: 1.2;
    letter-spacing: -0.02em;
}

.result-desc {
    color: var(--muted);
    font-size: 0.93rem;
    line-height: 1.6;
}

.impact-box {
    margin-top: 14px;
    padding: 12px 14px;
    border-radius: 12px;
    background: #F8FAFC;
    border-left: 3px solid #64748B;
    font-size: 0.85rem;
    color: #334155;
    line-height: 1.55;
}

.conf-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin: 20px 0 8px;
}

.conf-label {
    color: var(--muted);
    font-weight: 600;
    font-size: 0.88rem;
}

.conf-value {
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 800;
    font-size: 1.45rem;
    color: var(--ink);
}

.bar {
    height: 11px;
    background: #F1F5F9;
    border-radius: 999px;
    overflow: hidden;
    box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.06);
}

.bar > div {
    height: 100%;
    border-radius: 999px;
    animation: progressFill 0.85s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.other-row {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 0.86rem;
    color: #334155;
    margin-bottom: 9px;
}

.other-row .name { width: 42%; font-weight: 600; }
.other-row .bar  { flex: 1; height: 7px; }
.other-row .val  {
    width: 56px;
    text-align: right;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 600;
    font-size: 0.8rem;
    color: var(--muted);
}

.advice-item, .avoid-item {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    padding: 12px 15px;
    border-radius: 12px;
    font-size: 0.91rem;
    line-height: 1.55;
    margin-bottom: 8px;
    transition: transform 0.15s ease;
}

.advice-item:hover, .avoid-item:hover {
    transform: translateX(3px);
}

.advice-item { background: #F0FDF4; color: #14532D; border: 1px solid #BBF7D0; }
.avoid-item  { background: #FEF2F2; color: #7F1D1D; border: 1px solid #FECACA; }
.advice-item .ico, .avoid-item .ico { font-weight: 800; flex-shrink: 0; }

.note {
    color: var(--muted);
    font-size: 0.8rem;
    line-height: 1.55;
    border-top: 1px dashed var(--line);
    padding-top: 14px;
    margin-top: 10px;
}

/* ---------- Empty State (Idle) ---------- */
.empty-state {
    background: var(--surface);
    border: 2px dashed #CBD5E1;
    border-radius: var(--radius-lg);
    padding: 44px 26px;
    text-align: center;
    color: var(--muted);
    animation: fadeInUp 0.4s ease both;
}

.empty-state .big {
    font-size: 2.8rem;
    margin-bottom: 10px;
    display: inline-block;
    animation: floatSlow 3.2s ease-in-out infinite;
}

.tips-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-top: 22px;
    text-align: left;
}

@media (max-width: 640px) {
    .tips-grid {
        grid-template-columns: 1fr;
    }
}

.tip-box {
    background: #F8FAFC;
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 11px 12px;
    font-size: 0.78rem;
    color: #475569;
    line-height: 1.45;
}

.tip-box b {
    display: block;
    color: var(--ink);
    margin-bottom: 2px;
    font-size: 0.8rem;
}

/* ---------- About & Class Chips ---------- */
.category-subhead {
    font-weight: 800;
    font-size: 1.08rem;
    color: var(--ink);
    margin: 20px 0 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.class-chip {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 14px;
    display: flex;
    gap: 16px;
    align-items: flex-start;
    box-shadow: var(--shadow-sm);
    transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
}

.class-chip:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-md);
    border-color: #CBD5E1;
}

.class-chip .ico {
    font-size: 1.85rem;
    line-height: 1;
    background: #F8FAFC;
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--line);
    flex-shrink: 0;
}

.class-chip .t {
    font-weight: 800;
    color: var(--ink);
    font-size: 0.98rem;
    line-height: 1.3;
}

.class-chip .d {
    color: var(--muted);
    font-size: 0.85rem;
    line-height: 1.55;
    margin-top: 5px;
}

.class-chip .impact-mini {
    margin-top: 8px;
    font-size: 0.78rem;
    color: #475569;
    background: #F8FAFC;
    padding: 6px 10px;
    border-radius: 8px;
    border: 1px solid var(--line-soft);
}

.tag {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 2px 9px;
    border-radius: 999px;
    margin-left: 6px;
    vertical-align: middle;
}

.tag.b3    { background: var(--danger-soft); color: var(--danger-dark); border: 1px solid var(--danger-border); }
.tag.nonb3 { background: var(--primary-soft); color: #065F46; border: 1px solid var(--primary-border); }

/* ---------- Streamlit File Uploader & Tabs ---------- */
div[data-testid="stFileUploader"] section {
    border-radius: 16px !important;
    border: 2px dashed #CBD5E1 !important;
    background: var(--surface) !important;
    padding: 22px 16px !important;
    transition: all 0.22s ease !important;
}

div[data-testid="stFileUploader"] section:hover {
    border-color: var(--primary) !important;
    background: #F0FDF4 !important;
}

div[data-testid="stTabs"] button[role="tab"] {
    font-weight: 700 !important;
    font-size: 0.93rem !important;
    padding: 8px 18px !important;
    transition: color 0.2s ease !important;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--primary) !important;
    border-bottom-color: var(--primary) !important;
}

div[data-testid="stImage"] img {
    border-radius: 14px !important;
    border: 1px solid var(--line) !important;
    box-shadow: var(--shadow-sm) !important;
}
</style>
"""


def apply_custom_css():
    """Menyuntikkan stylesheet modern ke halaman Streamlit."""
    st.markdown(_CSS, unsafe_allow_html=True)