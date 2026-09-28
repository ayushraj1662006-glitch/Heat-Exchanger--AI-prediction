import streamlit as st

def render_sidebar():
    """
    Renders the custom sidebar logo, subtitle, dataset mode toggle, and navigation options.
    """
    st.sidebar.markdown(
        """
        <div style="text-align: center; padding: 15px 0 5px 0;">
            <div style="background: linear-gradient(135deg, rgba(0, 242, 254, 0.15), rgba(79, 172, 254, 0.15)); border: 1px solid rgba(0, 242, 254, 0.3); border-radius: 14px; padding: 16px; margin-bottom: 12px;">
                <h2 style="background: linear-gradient(90deg, #00F2FE, #4FACFE); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 800; margin: 0; letter-spacing: 1px;">HEAT-X AI</h2>
                <div style="color: #94A3B8; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 4px;">Industrial Intelligence</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Mode selection: Clean simulation vs Noisy Sensor mode
    st.sidebar.markdown("<p style='font-size: 0.85rem; font-weight: 700; text-transform: uppercase; color: #64748B; letter-spacing: 0.08em; margin-bottom: 6px;'>⚙️ Operating Environment</p>", unsafe_allow_html=True)
    noisy_mode = st.sidebar.toggle("📡 Sensor Noise Mode", value=False, help="Toggle between Clean DWSIM simulation data and realistic industrial sensor noise.")
    
    if noisy_mode:
        st.sidebar.markdown("<div style='background: rgba(255, 183, 3, 0.15); border: 1px solid #FFB703; color: #FFB703; padding: 6px 12px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; text-align: center; margin-bottom: 15px;'>📡 SENSOR NOISE ACTIVE</div>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown("<div style='background: rgba(0, 245, 160, 0.15); border: 1px solid #00F5A0; color: #00F5A0; padding: 6px 12px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; text-align: center; margin-bottom: 15px;'>✨ CLEAN SIMULATION DATA</div>", unsafe_allow_html=True)

    st.sidebar.markdown("<hr style='border-color: rgba(255, 255, 255, 0.08); margin: 10px 0 15px 0;' />", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='font-size: 0.85rem; font-weight: 700; text-transform: uppercase; color: #64748B; letter-spacing: 0.08em; margin-bottom: 10px;'>📌 Navigation Menu</p>", unsafe_allow_html=True)
    
    pages = [
        "🏠 Executive Dashboard",
        "📊 Data Explorer",
        "🌡️ Monitoring",
        "🎯 Performance Prediction",
        "🤖 Model Performance",
        "🔍 Explainable AI",
        "⚠️ Anomaly Detection",
        "🧪 What-If Simulator",
        "⚙️ Engineering Analysis",
        "🧠 Model Training",
        "📄 Reports",
        "⚙️ Settings",
        "ℹ️ About"
    ]
    
    selected_page = st.sidebar.radio("Select Page", pages, label_visibility="collapsed")
    
    st.sidebar.markdown("<hr style='border-color: rgba(255, 255, 255, 0.08); margin: 20px 0 15px 0;' />", unsafe_allow_html=True)
    st.sidebar.markdown("<div style='text-align: center; color: #475569; font-size: 0.75rem; font-weight: 600;'>HEAT-X AI v2.0<br>Traditional ML Decision Support</div>", unsafe_allow_html=True)
    
    return selected_page, noisy_mode
