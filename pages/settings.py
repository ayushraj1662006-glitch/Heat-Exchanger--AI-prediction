import streamlit as st

from config.config import DATASET_PATH, MODEL_PATH, METADATA_PATH
from components.cards import section_header, info_card

def render_page(is_noisy: bool):
    st.title("⚙️ System Settings & Environment Configuration")
    st.markdown("<p style='color: #8892B0;'>System paths, number formatting, model settings, and caching management.</p>", unsafe_allow_html=True)
    
    st.markdown("### 📁 File Paths & Model Registries")
    st.text_input("Dataset File Location", value=DATASET_PATH, disabled=True)
    st.text_input("Model Artifact Location", value=MODEL_PATH, disabled=True)
    st.text_input("Metadata Registry Location", value=METADATA_PATH, disabled=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    section_header("Display & UI Preferences", icon="🎨")
    
    st.selectbox("Decimal Precision", [2, 3, 4], index=1)
    st.selectbox("Plotly Chart Color Palette", ["plotly_dark", "cyberpunk", "slate"], index=0)
    
    st.markdown("<br>", unsafe_allow_html=True)
    section_header("Cache Management", icon="🧹")
    
    if st.button("Clear Streamlit Application Cache"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.success("Application cache cleared successfully!")
