"""
Apple Design System - Lite Theme for Streamlit & Plotly
Encodes Apple WWDC Design Principles:
- System fonts (-apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", sans-serif)
- Optical sizing, negative tracking (-0.02em) on headings
- Clean translucent materials (backdrop-filter: blur(20px))
- Micro-interactions (scale on active press, smooth spring ease)
- High contrast, legible typography and curated Apple color palette
"""

import plotly.graph_objects as go
import plotly.io as pio

# Apple Color Tokens (Light Mode)
APPLE_CANVAS_BG = "#F5F5F7"
APPLE_CARD_BG = "#FFFFFF"
APPLE_CARD_BORDER = "rgba(0, 0, 0, 0.08)"
APPLE_TEXT_PRIMARY = "#1D1D1F"
APPLE_TEXT_SECONDARY = "#86868B"
APPLE_TEXT_TERTIARY = "#A1A1A6"

# Accent Colors
APPLE_BLUE = "#0071E3"
APPLE_BLUE_HOVER = "#0077ED"
APPLE_GREEN = "#34C759"
APPLE_ORANGE = "#FF9500"
APPLE_INDIGO = "#5856D6"
APPLE_PURPLE = "#AF52DE"
APPLE_TEAL = "#30B0C7"
APPLE_RED = "#FF3B30"

def get_apple_css() -> str:
    """Returns CSS adhering to the Apple Design System Lite Theme."""
    return f"""
    <style>
    /* Google / Apple System Fonts */
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;500;600;700&family=SF+Pro+Text:wght@400;500;600&display=swap');

    /* Global Body & Container */
    .stApp {{
        background-color: {APPLE_CANVAS_BG} !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        color: {APPLE_TEXT_PRIMARY} !important;
        -webkit-font-smoothing: antialiased;
    }}

    /* Top App Header Banner */
    .apple-header {{
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(24px) saturate(180%);
        -webkit-backdrop-filter: blur(24px) saturate(180%);
        border-bottom: 1px solid rgba(0, 0, 0, 0.08);
        padding: 18px 28px;
        margin: -4rem -4rem 2rem -4rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: sticky;
        top: 0;
        z-index: 999;
    }}

    .apple-header-title {{
        font-size: 1.45rem;
        font-weight: 700;
        letter-spacing: -0.025em;
        color: {APPLE_TEXT_PRIMARY};
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }}

    .apple-header-subtitle {{
        font-size: 0.85rem;
        color: {APPLE_TEXT_SECONDARY};
        margin-top: 2px;
        font-weight: 400;
        letter-spacing: -0.01em;
    }}

    /* Status Pills / Badges */
    .apple-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: -0.01em;
    }}

    .badge-blue {{
        background: rgba(0, 113, 227, 0.09);
        color: {APPLE_BLUE};
        border: 1px solid rgba(0, 113, 227, 0.2);
    }}

    .badge-green {{
        background: rgba(52, 199, 89, 0.12);
        color: #248A3D;
        border: 1px solid rgba(52, 199, 89, 0.25);
    }}

    .badge-orange {{
        background: rgba(255, 149, 0, 0.12);
        color: #B25E00;
        border: 1px solid rgba(255, 149, 0, 0.25);
    }}

    .badge-purple {{
        background: rgba(175, 82, 222, 0.12);
        color: #8936B3;
        border: 1px solid rgba(175, 82, 222, 0.25);
    }}

    /* Card Containers */
    .apple-card {{
        background: {APPLE_CARD_BG};
        border-radius: 16px;
        border: 1px solid {APPLE_CARD_BORDER};
        padding: 22px 24px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04), 0 1px 3px rgba(0, 0, 0, 0.02);
        margin-bottom: 20px;
        transition: transform 180ms ease, box-shadow 180ms ease;
    }}

    .apple-card:hover {{
        box-shadow: 0 8px 30px -4px rgba(0, 0, 0, 0.07), 0 2px 6px rgba(0, 0, 0, 0.03);
    }}

    .apple-card-title {{
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: -0.02em;
        color: {APPLE_TEXT_PRIMARY};
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    /* KPI Stat Boxes */
    .apple-kpi {{
        background: {APPLE_CARD_BG};
        border-radius: 14px;
        border: 1px solid {APPLE_CARD_BORDER};
        padding: 16px 18px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}

    .apple-kpi-label {{
        font-size: 0.78rem;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.03em;
        color: {APPLE_TEXT_SECONDARY};
        margin-bottom: 4px;
    }}

    .apple-kpi-value {{
        font-size: 1.75rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: {APPLE_TEXT_PRIMARY};
        line-height: 1.1;
    }}

    .apple-kpi-subtext {{
        font-size: 0.78rem;
        color: {APPLE_TEXT_SECONDARY};
        margin-top: 4px;
        font-weight: 400;
    }}

    /* Buttons with direct haptic-like active state */
    .stButton > button {{
        background-color: {APPLE_BLUE} !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        padding: 10px 22px !important;
        letter-spacing: -0.01em !important;
        box-shadow: 0 2px 8px rgba(0, 113, 227, 0.25) !important;
        transition: transform 100ms ease-out, background-color 150ms ease !important;
    }}

    .stButton > button:hover {{
        background-color: {APPLE_BLUE_HOVER} !important;
        box-shadow: 0 4px 14px rgba(0, 113, 227, 0.35) !important;
    }}

    .stButton > button:active {{
        transform: scale(0.97) !important;
        transition: transform 100ms ease-out !important;
    }}

    /* Secondary Button */
    .apple-btn-secondary {{
        background: rgba(0, 0, 0, 0.05) !important;
        color: {APPLE_TEXT_PRIMARY} !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        box-shadow: none !important;
    }}

    /* Tabs Styling - macOS Segments */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: rgba(118, 118, 128, 0.12);
        padding: 4px;
        border-radius: 12px;
        gap: 4px;
        border: none;
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.88rem;
        padding: 8px 18px;
        color: {APPLE_TEXT_SECONDARY};
        border: none;
        background: transparent;
        transition: background 150ms ease, color 150ms ease, box-shadow 150ms ease;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: #FFFFFF !important;
        color: {APPLE_TEXT_PRIMARY} !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
    }}

    /* Inputs, Sliders, Selectboxes */
    .stSelectbox > div > div, .stNumberInput > div > div > input, .stTextInput > div > div > input {{
        border-radius: 10px !important;
        border: 1px solid rgba(0, 0, 0, 0.12) !important;
        background-color: #FFFFFF !important;
        color: {APPLE_TEXT_PRIMARY} !important;
        font-weight: 500 !important;
    }}

    /* Hide standard Streamlit header & footer for clean app feel */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* MATLAB Figure window frame styling */
    .matlab-fig-frame {{
        background: #FDFDFD;
        border: 1px solid rgba(0, 0, 0, 0.12);
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
    }}

    .matlab-fig-titlebar {{
        background: linear-gradient(180deg, #F0F0F3 0%, #E6E6EA 100%);
        border-bottom: 1px solid rgba(0, 0, 0, 0.12);
        padding: 8px 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.82rem;
        font-weight: 600;
        color: #333336;
    }}

    .mac-window-dots {{
        display: flex;
        gap: 6px;
    }}
    .mac-dot {{
        width: 11px;
        height: 11px;
        border-radius: 50%;
    }}
    .mac-dot-red {{ background: #FF5F56; border: 1px solid #E0443E; }}
    .mac-dot-yellow {{ background: #FFBD2E; border: 1px solid #DEA123; }}
    .mac-dot-green {{ background: #27C93F; border: 1px solid #1AAB29; }}

    /* Markdown Code & Tables */
    table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid rgba(0,0,0,0.08);
        background: #FFFFFF;
    }}
    th {{
        background: #F8F8FA;
        color: {APPLE_TEXT_PRIMARY};
        font-weight: 600;
        font-size: 0.82rem;
        padding: 10px 14px;
        border-bottom: 1px solid rgba(0,0,0,0.08);
        text-align: left;
    }}
    td {{
        padding: 10px 14px;
        border-bottom: 1px solid rgba(0,0,0,0.04);
        font-size: 0.85rem;
        color: {APPLE_TEXT_PRIMARY};
    }}
    tr:last-child td {{
        border-bottom: none;
    }}

    /* Chat bubble styling */
    .chat-user {{
        background: {APPLE_BLUE};
        color: white;
        border-radius: 18px 18px 4px 18px;
        padding: 12px 18px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 0.9rem;
        line-height: 1.4;
    }}

    .chat-assistant {{
        background: #FFFFFF;
        color: {APPLE_TEXT_PRIMARY};
        border-radius: 18px 18px 18px 4px;
        padding: 14px 20px;
        margin: 8px 0;
        max-width: 85%;
        border: 1px solid rgba(0, 0, 0, 0.08);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
        font-size: 0.9rem;
        line-height: 1.5;
    }}
    </style>
    """

def apply_apple_plotly_theme(fig: go.Figure) -> go.Figure:
    """Applies Apple light aesthetics to Plotly charts."""
    fig.update_layout(
        paper_bgcolor=APPLE_CARD_BG,
        plot_bgcolor="#FCFCFD",
        font=dict(
            family='-apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", sans-serif',
            size=12,
            color=APPLE_TEXT_PRIMARY
        ),
        margin=dict(l=48, r=48, t=44, b=44),
        hoverlabel=dict(
            bgcolor=APPLE_CARD_BG,
            font_size=12,
            font_family='-apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", sans-serif',
            bordercolor=APPLE_CARD_BORDER
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(0, 0, 0, 0.05)",
            linecolor="rgba(0, 0, 0, 0.12)",
            tickcolor="rgba(0, 0, 0, 0.12)",
            zerolinecolor="rgba(0, 0, 0, 0.08)"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(0, 0, 0, 0.05)",
            linecolor="rgba(0, 0, 0, 0.12)",
            tickcolor="rgba(0, 0, 0, 0.12)",
            zerolinecolor="rgba(0, 0, 0, 0.08)"
        ),
        legend=dict(
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor=APPLE_CARD_BORDER,
            borderwidth=1,
            font=dict(size=11)
        )
    )
    return fig
