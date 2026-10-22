"""
Apple Design System - Lite Theme for Streamlit & Plotly
Encodes Apple WWDC Design Principles:
- System fonts (-apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Segoe UI", sans-serif)
- Optical sizing, negative tracking (-0.02em) on headings
- Clean translucent materials (backdrop-filter: blur(20px))
- Micro-interactions (scale on active press, smooth spring ease)
- High contrast, legible typography and curated Apple color palette
- Comprehensive Mobile & Cross-Device Responsiveness (iPhone, iPad, Android, Desktop)
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
    """Returns CSS adhering to the Apple Design System Lite Theme with mobile-native responsiveness."""
    return f"""
    <style>
    /* Google / Apple System Fonts */
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;500;600;700&family=SF+Pro+Text:wght@400;500;600&display=swap');

    /* Global Body & Container */
    html {{
        -webkit-tap-highlight-color: transparent !important;
        scroll-behavior: smooth;
    }}

    .stApp {{
        background-color: {APPLE_CANVAS_BG} !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        color: {APPLE_TEXT_PRIMARY} !important;
        -webkit-font-smoothing: antialiased;
        padding-top: env(safe-area-inset-top);
        padding-bottom: env(safe-area-inset-bottom);
        padding-left: env(safe-area-inset-left);
        padding-right: env(safe-area-inset-right);
    }}

    /* Top App Header Banner */
    .apple-header {{
        background: rgba(255, 255, 255, 0.88);
        backdrop-filter: blur(24px) saturate(180%);
        -webkit-backdrop-filter: blur(24px) saturate(180%);
        border-bottom: 1px solid rgba(0, 0, 0, 0.08);
        padding: 16px 24px;
        margin: -3.5rem -3.5rem 1.8rem -3.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: sticky;
        top: 0;
        z-index: 999;
    }}

    .apple-header-title {{
        font-size: 1.35rem;
        font-weight: 700;
        letter-spacing: -0.025em;
        color: {APPLE_TEXT_PRIMARY};
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }}

    .apple-header-subtitle {{
        font-size: 0.82rem;
        color: {APPLE_TEXT_SECONDARY};
        margin-top: 3px;
        font-weight: 400;
        letter-spacing: -0.01em;
    }}

    .apple-header-badges {{
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    /* Status Pills / Badges */
    .apple-badge {{
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 4px 11px;
        border-radius: 999px;
        font-size: 0.76rem;
        font-weight: 600;
        letter-spacing: -0.01em;
        white-space: nowrap;
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
        padding: 20px 22px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04), 0 1px 3px rgba(0, 0, 0, 0.02);
        margin-bottom: 18px;
        transition: transform 180ms ease, box-shadow 180ms ease;
    }}

    .apple-card-title {{
        font-size: 1.05rem;
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
        padding: 14px 16px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin-bottom: 10px;
    }}

    .apple-kpi-label {{
        font-size: 0.74rem;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.03em;
        color: {APPLE_TEXT_SECONDARY};
        margin-bottom: 3px;
    }}

    .apple-kpi-value {{
        font-size: 1.6rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: {APPLE_TEXT_PRIMARY};
        line-height: 1.15;
    }}

    .apple-kpi-subtext {{
        font-size: 0.74rem;
        color: {APPLE_TEXT_SECONDARY};
        margin-top: 3px;
        font-weight: 400;
    }}

    /* Direct Manipulation Buttons with mobile haptic active state */
    .stButton > button {{
        background-color: {APPLE_BLUE} !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 0.90rem !important;
        padding: 10px 20px !important;
        letter-spacing: -0.01em !important;
        box-shadow: 0 2px 8px rgba(0, 113, 227, 0.22) !important;
        touch-action: manipulation !important;
        user-select: none !important;
        -webkit-user-select: none !important;
        transition: transform 100ms ease-out, background-color 150ms ease !important;
    }}

    .stButton > button:active {{
        transform: scale(0.97) !important;
        transition: transform 100ms ease-out !important;
    }}

    /* Gate hover states strictly to fine pointers (Desktop Mouse) to avoid sticky hover on touch */
    @media (hover: hover) and (pointer: fine) {{
        .stButton > button:hover {{
            background-color: {APPLE_BLUE_HOVER} !important;
            box-shadow: 0 4px 14px rgba(0, 113, 227, 0.35) !important;
        }}
        .apple-card:hover {{
            box-shadow: 0 8px 30px -4px rgba(0, 0, 0, 0.07), 0 2px 6px rgba(0, 0, 0, 0.03);
        }}
    }}

    /* Tabs Styling - macOS Segments with smooth horizontal touch scroll on mobile */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: rgba(118, 118, 128, 0.12) !important;
        padding: 4px !important;
        border-radius: 12px !important;
        gap: 4px !important;
        border: none !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        scrollbar-width: none !important;
        flex-wrap: nowrap !important;
        white-space: nowrap !important;
    }}

    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {{
        display: none !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        padding: 8px 14px !important;
        color: {APPLE_TEXT_SECONDARY} !important;
        border: none !important;
        background: transparent !important;
        flex-shrink: 0 !important;
        white-space: nowrap !important;
        touch-action: manipulation !important;
        transition: background 150ms ease, color 150ms ease, box-shadow 150ms ease !important;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: #FFFFFF !important;
        color: {APPLE_TEXT_PRIMARY} !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
    }}

    /* Inputs, Sliders, Selectboxes with iOS auto-zoom prevention */
    .stSelectbox > div > div, .stNumberInput > div > div > input, .stTextInput > div > div > input {{
        border-radius: 10px !important;
        border: 1px solid rgba(0, 0, 0, 0.12) !important;
        background-color: #FFFFFF !important;
        color: {APPLE_TEXT_PRIMARY} !important;
        font-weight: 500 !important;
    }}

    /* Prevent auto-zoom on mobile inputs */
    @media (pointer: coarse) {{
        input, textarea, select {{
            font-size: 16px !important;
        }}
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
        margin-bottom: 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
    }}

    .matlab-fig-titlebar {{
        background: linear-gradient(180deg, #F0F0F3 0%, #E6E6EA 100%);
        border-bottom: 1px solid rgba(0, 0, 0, 0.12);
        padding: 8px 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.80rem;
        font-weight: 600;
        color: #333336;
    }}

    .mac-window-dots {{
        display: flex;
        gap: 6px;
    }}
    .mac-dot {{
        width: 10px;
        height: 10px;
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
        overflow-x: auto;
        display: block;
        border: 1px solid rgba(0,0,0,0.08);
        background: #FFFFFF;
    }}
    th {{
        background: #F8F8FA;
        color: {APPLE_TEXT_PRIMARY};
        font-weight: 600;
        font-size: 0.80rem;
        padding: 9px 12px;
        border-bottom: 1px solid rgba(0,0,0,0.08);
        text-align: left;
    }}
    td {{
        padding: 9px 12px;
        border-bottom: 1px solid rgba(0,0,0,0.04);
        font-size: 0.82rem;
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
        padding: 10px 16px;
        margin: 6px 0;
        max-width: 85%;
        margin-left: auto;
        font-size: 0.88rem;
        line-height: 1.4;
        word-break: break-word;
    }}

    .chat-assistant {{
        background: #FFFFFF;
        color: {APPLE_TEXT_PRIMARY};
        border-radius: 18px 18px 18px 4px;
        padding: 12px 18px;
        margin: 6px 0;
        max-width: 90%;
        border: 1px solid rgba(0, 0, 0, 0.08);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
        font-size: 0.88rem;
        line-height: 1.5;
        word-break: break-word;
    }}

    /* =========================================================================
       RESPONSIVE BREAKPOINTS (Mobile, Phablets, Tablets, Laptops)
       ========================================================================= */

    /* Small Mobile Phones (iPhone SE, Galaxy S, up to 480px) */
    @media (max-width: 480px) {{
        .apple-header {{
            margin: -1.5rem -1rem 1rem -1rem !important;
            padding: 10px 14px !important;
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 8px !important;
        }}
        .apple-header-title {{
            font-size: 1.10rem !important;
            flex-wrap: wrap !important;
        }}
        .apple-header-badges {{
            flex-wrap: wrap !important;
            gap: 4px !important;
            width: 100% !important;
        }}
        .apple-card {{
            padding: 12px 14px !important;
            border-radius: 12px !important;
        }}
        .apple-kpi {{
            padding: 10px 12px !important;
        }}
        .apple-kpi-value {{
            font-size: 1.25rem !important;
        }}
        .chat-user, .chat-assistant {{
            max-width: 95% !important;
            font-size: 0.82rem !important;
            padding: 9px 12px !important;
        }}
    }}

    /* Large Phones & Small Tablets (481px to 768px) */
    @media (min-width: 481px) and (max-width: 768px) {{
        .apple-header {{
            margin: -2rem -1.5rem 1.25rem -1.5rem !important;
            padding: 12px 18px !important;
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 10px !important;
        }}
        .apple-header-title {{
            font-size: 1.25rem !important;
        }}
        .apple-card {{
            padding: 16px 18px !important;
        }}
        .apple-kpi-value {{
            font-size: 1.45rem !important;
        }}
    }}

    /* Tablets (iPad, iPad Mini, 769px to 1024px) */
    @media (min-width: 769px) and (max-width: 1024px) {{
        .apple-header {{
            margin: -2.5rem -2rem 1.5rem -2rem !important;
            padding: 14px 20px !important;
        }}
    }}
    </style>
    """

def apply_apple_plotly_theme(fig: go.Figure) -> go.Figure:
    """Applies Apple light aesthetics to Plotly charts with responsive margins."""
    fig.update_layout(
        paper_bgcolor=APPLE_CARD_BG,
        plot_bgcolor="#FCFCFD",
        font=dict(
            family='-apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", sans-serif',
            size=11,
            color=APPLE_TEXT_PRIMARY
        ),
        margin=dict(l=32, r=32, t=38, b=38),
        autosize=True,
        hoverlabel=dict(
            bgcolor=APPLE_CARD_BG,
            font_size=11,
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
            bgcolor="rgba(255, 255, 255, 0.85)",
            bordercolor=APPLE_CARD_BORDER,
            borderwidth=1,
            font=dict(size=10),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig
