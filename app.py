import os
import sys

# Ensure root workspace directory is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import streamlit as st

# Configure Streamlit page layout & theme FIRST before any other streamlit commands
st.set_page_config(
    page_title="HEAT-X AI | Industrial Heat Exchanger Analytics",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from config.config import APP_TITLE
from components.styles import inject_custom_css
from components.sidebar import render_sidebar

# Import all 13 pages
from pages import (
    dashboard,
    data_explorer,
    monitoring,
    prediction,
    model_performance,
    explainable_ai,
    anomaly,
    simulator,
    engineering,
    training,
    reports,
    settings,
    about
)

def main():
    # Inject custom industrial dark theme styling
    inject_custom_css()
    
    # Render Sidebar and get selected page and operating mode
    selected_page, is_noisy = render_sidebar()
    
    # Route to selected page
    if selected_page == "🏠 Executive Dashboard":
        dashboard.render_page(is_noisy)
    elif selected_page == "📊 Data Explorer":
        data_explorer.render_page(is_noisy)
    elif selected_page == "🌡️ Monitoring":
        monitoring.render_page(is_noisy)
    elif selected_page == "🎯 Performance Prediction":
        prediction.render_page(is_noisy)
    elif selected_page == "🤖 Model Performance":
        model_performance.render_page(is_noisy)
    elif selected_page == "🔍 Explainable AI":
        explainable_ai.render_page(is_noisy)
    elif selected_page == "⚠️ Anomaly Detection":
        anomaly.render_page(is_noisy)
    elif selected_page == "🧪 What-If Simulator":
        simulator.render_page(is_noisy)
    elif selected_page == "⚙️ Engineering Analysis":
        engineering.render_page(is_noisy)
    elif selected_page == "🧠 Model Training":
        training.render_page(is_noisy)
    elif selected_page == "📄 Reports":
        reports.render_page(is_noisy)
    elif selected_page == "⚙️ Settings":
        settings.render_page(is_noisy)
    elif selected_page == "ℹ️ About":
        about.render_page(is_noisy)

if __name__ == "__main__":
    main()
