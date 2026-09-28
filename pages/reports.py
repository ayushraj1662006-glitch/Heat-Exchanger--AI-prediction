import os
import json
import streamlit as st
import pandas as pd

from config.config import METADATA_PATH, DATASET_PATH
from src.data_loader import load_dataset
from src.utils import generate_csv_report
from components.cards import section_header, metric_card, info_card

def render_page(is_noisy: bool):
    st.title("📄 Reports & Documentation Export")
    st.markdown("<p style='color: #8892B0;'>Generate and export technical analytics summary reports for engineering compliance.</p>", unsafe_allow_html=True)
    
    metadata = {}
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "r") as f:
            metadata = json.load(f)

    st.markdown("### Executive Technical Report")
    
    report_text = f"""
    ================================================================================
    AI-BASED HEAT EXCHANGER PERFORMANCE PREDICTION & OPTIMIZATION REPORT
    ================================================================================
    Generated Date/Time: {metadata.get('training_timestamp', 'N/A')}
    Operating Mode: {'Sensor Noise Mode' if is_noisy else 'Clean Simulation Mode'}
    
    1. PROJECT OVERVIEW
    --------------------------------------------------------------------------------
    This decision-support system models shell-and-tube heat exchanger thermal duty 
    (Q in kW) from input operating parameters using traditional Machine Learning.
    
    2. DATASET SUMMARY
    --------------------------------------------------------------------------------
    - Source: DWSIM Heat Exchanger Parametric Study Dataset
    - Total Observations: 10,000 rows
    - Total Variables: 20 columns (Clean & Noisy sensor pairings)
    
    3. BEST PRODUCTION MODEL METRICS
    --------------------------------------------------------------------------------
    - Selected Model: {metadata.get('best_model_name', 'N/A')}
    - R² Score (Test Set): {metadata.get('best_model_metrics', {}).get('R2', 'N/A')}
    - Root Mean Squared Error (RMSE): {metadata.get('best_model_metrics', {}).get('RMSE', 'N/A')} kW
    - Mean Absolute Error (MAE): {metadata.get('best_model_metrics', {}).get('MAE', 'N/A')} kW
    - 5-Fold Cross-Validation R²: {metadata.get('best_model_metrics', {}).get('CV_R2_Mean', 'N/A')}
    
    4. ENGINEERING COMPLIANCE & LIMITATIONS
    --------------------------------------------------------------------------------
    - Data Leakage Prevention: Verified (Outlet temperatures excluded from inputs).
    - Energy Balance Equation: Q = m_dot * Cp * delta_T verified.
    - Limitation: Data represents steady-state parametric simulation.
    ================================================================================
    """
    
    st.text_area("Technical Report Preview", report_text, height=350)
    
    st.markdown("<br>", unsafe_allow_html=True)
    section_header("Download Options", icon="💾")
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "📥 Download Technical Summary (.txt)",
            data=report_text,
            file_name="heat_exchanger_ai_report.txt",
            mime="text/plain"
        )
    with col2:
        try:
            df = load_dataset(DATASET_PATH)
            csv_data = df.to_csv(index=False)
            st.download_button(
                "📥 Download Processed Dataset (.csv)",
                data=csv_data,
                file_name="heat_exchanger_processed_dataset.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.warning(f"Error loading dataset for download: {e}")
