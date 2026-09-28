import streamlit as st
import pandas as pd
import plotly.express as px

from config.config import DATASET_PATH
from src.data_loader import load_dataset
from src.anomaly_detection import detect_anomalies_isolation_forest, get_anomaly_summary
from components.cards import metric_card, section_header, warning_card, info_card

def render_page(is_noisy: bool):
    st.title("⚠️ Anomaly Detection")
    st.markdown("<p style='color: #8892B0;'>Unsupervised traditional Machine Learning (Isolation Forest) for detecting unusual thermal operating conditions.</p>", unsafe_allow_html=True)
    
    try:
        df = load_dataset(DATASET_PATH)
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return

    st.markdown("### 🎛️ Anomaly Detection Sensitivity")
    contamination = st.slider("Select Contamination Fraction (Expected % Anomalies)", 0.01, 0.15, 0.05, 0.01)
    
    df_anom = detect_anomalies_isolation_forest(df, contamination=contamination, is_noisy=is_noisy)
    summary = get_anomaly_summary(df_anom)
    
    # KPI Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Total Observations", f"{summary['total_observations']:,}")
    with c2:
        metric_card("Normal Conditions", f"{summary['normal_operating_count']:,}")
    with c3:
        metric_card("Unusual Conditions", f"{summary['unusual_condition_count']:,}", border_color="#FFB703")
    with c4:
        metric_card("Anomaly Rate", f"{summary['anomaly_percentage']}%")

    st.markdown("<br>", unsafe_allow_html=True)
    section_header("Operating Condition Scatter Distribution", icon="🎯")
    
    suffix = "_noisy" if is_noisy else ""
    x_col = f"hot_inlet_temperature_k{suffix}"
    y_col = f"hx_1_heat_load_kw{suffix}"
    
    fig = px.scatter(
        df_anom,
        x=x_col,
        y=y_col,
        color="Anomaly_Flag",
        color_discrete_map={"Normal Operating": "#00D2FF", "Potentially Unusual": "#EF476F"},
        title="Operating Condition Map: Hot Inlet Temperature vs Heat Duty",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    warning_card("Industrial Operational Guidance", "Flagged observations represent statistically unusual combinations of temperature, flow, and pressure. These points warrant process verification but do not automatically imply mechanical hardware failure.")
