import streamlit as st

def inject_custom_css():
    """
    Injects custom high-end industrial dark theme CSS styling into Streamlit.
    Enhanced color scheme, modern typography (Outfit, Plus Jakarta Sans), font sizing,
    gradient titles, glassmorphism cards, and interactive controls.
    """
    css = """
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Fira+Code:wght@400;600&display=swap');
    
    /* Global Page Dark Theme */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #CBD5E1;
        background-color: #0B0E17;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 0%, #111827 0%, #0B0E17 75%);
    }
    
    /* Typography & Font Sizing */
    h1 {
        font-family: 'Outfit', sans-serif !important;
        font-size: 2.35rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #00F2FE 55%, #4FACFE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.4rem !important;
    }
    
    h2 {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.7rem !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
        letter-spacing: -0.01em !important;
    }
    
    h3 {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        color: #E2E8F0 !important;
    }
    
    h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        color: #CBD5E1 !important;
    }

    p, span, label {
        font-size: 1.02rem;
        line-height: 1.6;
    }

    /* Metric Cards - Glassmorphism Aesthetic */
    .metric-card {
        background: linear-gradient(145deg, rgba(23, 31, 49, 0.85) 0%, rgba(15, 21, 35, 0.95) 100%);
        border: 1px solid rgba(0, 242, 254, 0.18);
        border-radius: 14px;
        padding: 22px 24px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
        backdrop-filter: blur(12px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #00F2FE 0%, #4FACFE 100%);
        border-radius: 4px 0 0 4px;
    }

    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 242, 254, 0.5);
        box-shadow: 0 12px 30px rgba(0, 242, 254, 0.2);
    }
    
    .metric-title {
        font-size: 0.88rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94A3B8;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 2.1rem;
        font-weight: 800;
        color: #00F2FE;
        font-family: 'Outfit', sans-serif;
        text-shadow: 0 0 15px rgba(0, 242, 254, 0.35);
        line-height: 1.1;
    }
    
    .metric-subtitle {
        font-size: 0.85rem;
        color: #64748B;
        margin-top: 6px;
        font-weight: 500;
    }
    
    /* Hero Prediction Card */
    .prediction-card {
        background: linear-gradient(135deg, #091E3A 0%, #103260 50%, #1A4D8C 100%);
        border: 2px solid #00F2FE;
        border-radius: 18px;
        padding: 32px 28px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0, 242, 254, 0.3), inset 0 0 20px rgba(0, 242, 254, 0.15);
        margin: 20px 0;
        position: relative;
    }
    
    .prediction-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #93C5FD;
        text-transform: uppercase;
        letter-spacing: 0.12em;
    }
    
    .prediction-value {
        font-size: 3.6rem;
        font-weight: 800;
        color: #FFFFFF;
        font-family: 'Outfit', sans-serif;
        text-shadow: 0 0 25px rgba(0, 242, 254, 0.7);
        margin: 12px 0;
        line-height: 1;
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    
    .status-badge-success {
        background: rgba(0, 245, 160, 0.12);
        color: #00F5A0;
        border: 1px solid rgba(0, 245, 160, 0.4);
        box-shadow: 0 0 10px rgba(0, 245, 160, 0.2);
    }
    
    .status-badge-warning {
        background: rgba(255, 183, 3, 0.12);
        color: #FFB703;
        border: 1px solid rgba(255, 183, 3, 0.4);
        box-shadow: 0 0 10px rgba(255, 183, 3, 0.2);
    }
    
    .status-badge-danger {
        background: rgba(239, 71, 111, 0.12);
        color: #EF476F;
        border: 1px solid rgba(239, 71, 111, 0.4);
        box-shadow: 0 0 10px rgba(239, 71, 111, 0.2);
    }

    /* Streamlit Buttons Styling */
    div.stButton > button {
        background: linear-gradient(90deg, #00C6FF 0%, #0072FF 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.05em !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        box-shadow: 0 6px 20px rgba(0, 114, 255, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }

    div.stButton > button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 10px 30px rgba(0, 198, 255, 0.6) !important;
        background: linear-gradient(90deg, #00F2FE 0%, #4FACFE 100%) !important;
    }

    /* Streamlit Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(17, 24, 39, 0.6);
        padding: 8px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Outfit', sans-serif;
        font-size: 1.02rem;
        font-weight: 600;
        color: #94A3B8;
        border-radius: 8px;
        padding: 10px 20px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        color: #00F2FE !important;
        border: 1px solid rgba(0, 242, 254, 0.4) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    /* Streamlit Inputs and Sliders */
    .stSelectbox label, .stSlider label, .stNumberInput label, .stTextInput label {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        color: #E2E8F0 !important;
        font-size: 0.98rem !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #1E293B !important;
        border-color: #334155 !important;
        color: #F8FAFC !important;
        border-radius: 10px !important;
    }

    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #080C14 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    section[data-testid="stSidebar"] .stRadio label {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 600;
        font-size: 0.98rem;
        color: #CBD5E1;
        padding: 8px 12px;
        border-radius: 8px;
        transition: all 0.2s ease;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        color: #00F2FE;
        background-color: rgba(0, 242, 254, 0.08);
    }

    /* Table & Dataframe Styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #1E293B;
    }

    /* Hide Default Footer */
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
