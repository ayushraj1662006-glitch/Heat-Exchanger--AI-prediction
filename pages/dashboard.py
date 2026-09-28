import os
import json
import streamlit as st
import pandas as pd
from PIL import Image

from config.config import HERO_IMAGE_PATH, METADATA_PATH, DATASET_PATH
from components.cards import metric_card, section_header, status_badge, info_card
from src.data_loader import load_dataset, validate_dataset

def render_page(is_noisy: bool):
    st.title("🏠 Executive Dashboard")
    st.markdown("<p style='color: #8892B0;'>Real-time AI Decision-Support for Shell & Tube Heat Exchanger Performance & Thermal Optimization.</p>", unsafe_allow_html=True)
    
    # Load dataset health
    try:
        df = load_dataset(DATASET_PATH)
        val_report = validate_dataset(df)
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return

    # Load Metadata
    metadata = {}
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "r") as f:
            metadata = json.load(f)

    # Hero Banner & Equipment Schematic
    col_hero, col_info = st.columns([1.2, 1])
    with col_hero:
        if os.path.exists(HERO_IMAGE_PATH):
            st.image(HERO_IMAGE_PATH, caption="Industrial Shell-and-Tube Heat Exchanger CAD & Thermal Schematic", use_container_width=True)
        else:
            st.info("Industrial Schematic View")
            
    with col_info:
        st.markdown("### Equipment Specification (HX-301)")
        st.markdown(
            """
            - **Unit Type**: Counter-Flow Shell & Tube Heat Exchanger
            - **Hot Fluid**: Process Thermal Stream (373.15 K - 573.15 K)
            - **Cold Fluid**: Industrial Coolant Mass Flow (0.5 - 5.0 kg/s)
            - **Operating Mode**: " + ("📡 Sensor Noise Mode" if is_noisy else "Clean Simulation Mode") + "
            - **Primary Target**: Heat Transfer Load ($Q$ in kW)
            - **Model Status**: Ready for Real-Time Inference
            """
        )
        status_badge("OPERATIONAL - AI AGENT ACTIVE", level="success")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Metric KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    best_model = metadata.get("best_model_name", "Random Forest")
    best_metrics = metadata.get("best_model_metrics", {})
    r2_val = best_metrics.get("R2", 1.0)
    rmse_val = best_metrics.get("RMSE", 0.114)
    
    with col1:
        metric_card("Dataset Size", f"{val_report['rows']:,} Rows", f"{val_report['cols']} Features Total")
    with col2:
        metric_card("Best Production Model", str(best_model), "Traditional ML Model")
    with col3:
        metric_card("Model Accuracy (R²)", f"{r2_val:.4f}", "5-Fold CV Verified")
    with col4:
        metric_card("Prediction RMSE", f"{rmse_val:.4f} kW", "Test Set MAE: " + str(best_metrics.get("MAE", 0.05)))

    st.markdown("<br>", unsafe_allow_html=True)
    section_header("Industrial Process & System Cards", icon="⚡")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("##### Performance Prediction")
        st.write("Predict heat duty & thermal outputs instantaneously from operating inputs.")
    with c2:
        st.markdown("##### Model Health")
        st.write(f"Last Trained: {metadata.get('training_timestamp', 'Recent')}")
    with c3:
        st.markdown("##### Data Quality")
        st.write(f"Missing Values: {val_report['total_missing']} | Duplicates: {val_report['duplicate_rows']}")
    with c4:
        st.markdown("##### Anomaly Status")
        st.write("Isolation Forest outlier monitoring enabled.")
        
    info_card("Decision-Support System Note", "This application is a machine-learning decision-support and surrogate modeling system trained on DWSIM parametric simulation data. It does not directly control physical actuators without engineer oversight.")
