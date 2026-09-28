import streamlit as st
import pandas as pd
import numpy as np

from config.config import DATASET_PATH
from src.data_loader import load_dataset
from src.prediction import predict_batch
from components.cards import section_header, metric_card, status_badge
from components.charts import plot_gauge_chart
import plotly.express as px

def render_page(is_noisy: bool):
    st.title("🌡️ Heat Exchanger Monitoring")
    st.markdown("<p style='color: #8892B0;'>Real-time engineering telemetry, gauge indicators, and operational performance trends.</p>", unsafe_allow_html=True)
    
    try:
        df = load_dataset(DATASET_PATH)
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return

    suffix = "_noisy" if is_noisy else ""
    t_hot_col = f"hot_inlet_temperature_k{suffix}"
    m_cold_col = f"cold_inlet_mass_flow_kg_s{suffix}"
    p_hot_col = f"hot_outlet_pressure_pa{suffix}"
    q_col = f"hx_1_heat_load_kw{suffix}"

    # Sample selector for live telemetry simulation
    st.markdown("### 🎛️ Live Operating Point Selector")
    sample_idx = st.slider("Select Sample Index (1 to 10,000)", 0, len(df)-1, 500)
    
    row = df.iloc[sample_idx]
    
    # Render Gauges
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        fig1 = plot_gauge_chart(float(row[t_hot_col]), 300, 650, "Hot Inlet Temp", "K")
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        fig2 = plot_gauge_chart(float(row[m_cold_col]), 0.1, 6.0, "Cold Mass Flow", "kg/s")
        st.plotly_chart(fig2, use_container_width=True)
    with c3:
        fig3 = plot_gauge_chart(float(row[p_hot_col])/1000.0, 300, 650, "Hot Outlet Press", "kPa")
        st.plotly_chart(fig3, use_container_width=True)
    with c4:
        fig4 = plot_gauge_chart(float(row[q_col]), 40, 160, "Measured Heat Load", "kW")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_header("Performance Trend over 100 Consecutive Operating Steps", icon="📈")
    
    # Run batch prediction on window of 100 samples
    window_df = df.iloc[max(0, sample_idx-50): min(len(df), sample_idx+50)].copy()
    try:
        pred_df = predict_batch(window_df, is_noisy=is_noisy)
        
        fig_trend = px.line(
            pred_df,
            y=[q_col, "Predicted_Heat_Load_kW"],
            title="Actual vs ML Predicted Heat Duty (kW) along Operating Range",
            labels={"value": "Heat Load (kW)", "variable": "Series"},
            template="plotly_dark",
            color_discrete_map={q_col: "#FFB703", "Predicted_Heat_Load_kW": "#00D2FF"}
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    except Exception as e:
        st.warning(f"Prediction model not loaded or needs training: {e}")
