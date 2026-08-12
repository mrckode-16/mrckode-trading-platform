def get_custom_css():
    return """
    <style>
    /* ===== FONTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    /* ===== GLOBAL BACKGROUND ===== */
    .stApp {
        background: 
            radial-gradient(ellipse at top left, rgba(168, 85, 247, 0.12) 0%, transparent 50%),
            radial-gradient(ellipse at bottom right, rgba(59, 130, 246, 0.08) 0%, transparent 50%),
            #050810;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* ===== HIDE STREAMLIT DEFAULTS ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* ===== MAIN CONTAINER - TIGHTER SPACING ===== */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }
    
    /* Remove extra spacing between elements */
    .element-container {
        margin-bottom: 0 !important;
    }
    
    div[data-testid="stVerticalBlock"] > div {
        gap: 0.75rem !important;
    }
    
    /* ===== SIDEBAR (FORCE VISIBLE) ===== */
section[data-testid="stSidebar"] {
    background: rgba(10, 14, 26, 0.98) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255, 255, 255, 0.06);
    min-width: 300px !important;
    max-width: 300px !important;
    display: block !important;
    visibility: visible !important;
    transform: translateX(0px) !important;
    position: relative !important;
    left: 0 !important;
}

section[data-testid="stSidebar"][aria-expanded="false"] {
    transform: translateX(0px) !important;
    min-width: 300px !important;
    max-width: 300px !important;
    margin-left: 0 !important;
}

section[data-testid="stSidebar"] > div {
    padding: 1rem 1.25rem !important;
}

section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div {
    gap: 0.5rem !important;
}

/* Hide the collapse button so it can't be hidden accidentally */
div[data-testid="collapsedControl"] {
    display: none !important;
}

/* Sidebar collapse button style */
button[kind="header"] {
    background: linear-gradient(135deg, #A855F7 0%, #3B82F6 100%) !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
}
    
    /* ===== TOP NAVIGATION BAR ===== */
    .top-nav {
        background: rgba(19, 23, 34, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 14px 24px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .nav-logo {
        font-size: 22px;
        font-weight: 900;
        background: linear-gradient(135deg, #A855F7 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    
    .nav-badge {
        background: rgba(168, 85, 247, 0.15);
        color: #A855F7;
        font-size: 9px;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 5px;
        letter-spacing: 1.5px;
        border: 1px solid rgba(168, 85, 247, 0.3);
    }
    
    .nav-right {
        display: flex;
        align-items: center;
        gap: 24px;
    }
    
    .nav-symbol {
        color: #6B7280;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    .nav-price {
        color: #FFFFFF;
        font-size: 20px;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.5px;
    }
    
    /* ===== METRIC CARDS ===== */
    .metric-card {
        background: linear-gradient(135deg, rgba(19, 23, 34, 0.9) 0%, rgba(15, 18, 27, 0.9) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 18px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        height: 100%;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(168, 85, 247, 0.6), transparent);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(168, 85, 247, 0.3);
        box-shadow: 0 15px 30px rgba(168, 85, 247, 0.12);
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .metric-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
        margin-bottom: 10px;
        font-size: 18px;
    }
    
    .metric-label {
        color: #6B7280;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 6px;
    }
    
    .metric-value {
        color: #FFFFFF;
        font-size: 26px;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        line-height: 1.2;
        letter-spacing: -1px;
    }
    
    .metric-sub {
        display: flex;
        align-items: center;
        gap: 6px;
        margin-top: 8px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .metric-positive { color: #10B981; }
    .metric-negative { color: #EF4444; }
    .metric-neutral { color: #6B7280; }
    
    /* ===== LIVE PULSE INDICATOR ===== */
    .pulse-dot {
        width: 7px;
        height: 7px;
        background: #10B981;
        border-radius: 50%;
        display: inline-block;
        animation: pulse 2s infinite;
        box-shadow: 0 0 10px #10B981;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.3); }
    }
    
    .pulse-dot-red {
        width: 7px;
        height: 7px;
        background: #EF4444;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #EF4444;
    }
    
    /* ===== STATUS PILLS ===== */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .status-live {
        background: rgba(16, 185, 129, 0.1);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .status-paused {
        background: rgba(239, 68, 68, 0.1);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    /* ===== SECTION HEADERS (TIGHTER SPACING) ===== */
    .section-title {
        color: #FFFFFF;
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 20px 0 12px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .section-title::before {
        content: '';
        width: 3px;
        height: 18px;
        background: linear-gradient(180deg, #A855F7 0%, #3B82F6 100%);
        border-radius: 2px;
    }
    
    /* Sidebar section titles - smaller */
    section[data-testid="stSidebar"] .section-title {
        font-size: 10px;
        margin: 14px 0 8px 0;
        letter-spacing: 1.5px;
    }
    
    /* ===== BUTTONS ===== */
    .stButton>button {
        background: linear-gradient(135deg, #A855F7 0%, #3B82F6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 700;
        font-size: 12px;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.35);
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.5);
    }
    
    /* ===== POSITION EMPTY STATE (SMALLER) ===== */
    .position-empty {
        background: rgba(19, 23, 34, 0.4);
        border: 1px dashed rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 30px 20px;
        text-align: center;
        color: #6B7280;
    }
    
    .position-empty-icon {
        font-size: 40px;
        margin-bottom: 10px;
        opacity: 0.6;
    }
    
    /* ===== INFO BOXES ===== */
    .info-box {
        background: rgba(59, 130, 246, 0.08);
        border-left: 3px solid #3B82F6;
        padding: 10px 14px;
        border-radius: 8px;
        color: #E5E7EB;
        font-size: 12px;
        margin: 8px 0;
    }
    
    /* ===== STREAMLIT SELECTBOX ===== */
    div[data-baseweb="select"] > div {
        background: rgba(19, 23, 34, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        min-height: 40px !important;
    }
    
    div[data-baseweb="select"] > div:hover {
        border-color: rgba(168, 85, 247, 0.5) !important;
    }
    
    /* Selectbox dropdown */
    div[data-baseweb="popover"] {
        background: #131722 !important;
        border: 1px solid rgba(168, 85, 247, 0.3) !important;
    }
    
    /* ===== NUMBER INPUT ===== */
    .stNumberInput > div > div {
        background: rgba(19, 23, 34, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
    }
    
    .stNumberInput input {
        background: transparent !important;
        color: #FFFFFF !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 600 !important;
    }
    
    .stNumberInput button {
        background: rgba(168, 85, 247, 0.15) !important;
        color: #A855F7 !important;
        border: none !important;
    }
    
    /* ===== LABELS ===== */
    label {
        color: #9CA3AF !important;
        font-size: 10px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    /* Reduce label margin */
    div[data-testid="stWidgetLabel"] {
        margin-bottom: 4px !important;
    }
    
    /* ===== DATAFRAMES ===== */
    div[data-testid="stDataFrame"] {
        background: rgba(19, 23, 34, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        overflow: hidden;
    }
    
    /* ===== ALERTS ===== */
    div[data-testid="stAlert"] {
        background: rgba(19, 23, 34, 0.8) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(19, 23, 34, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #A855F7, #3B82F6);
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #9333EA, #2563EB);
    }
    
    /* ===== PLOTLY CHART CONTAINER ===== */
    .js-plotly-plot {
        border-radius: 14px !important;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    
    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        padding: 20px 0;
        color: #4B5563;
        font-size: 10px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-top: 24px;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* ===== REMOVE GAPS FROM COLUMNS ===== */
    div[data-testid="column"] {
        padding: 0 0.4rem !important;
    }
    
    div[data-testid="column"]:first-child {
        padding-left: 0 !important;
    }
    
    div[data-testid="column"]:last-child {
        padding-right: 0 !important;
    }
    </style>
    """