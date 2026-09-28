import os
import json
import streamlit as st
import pandas as pd
import numpy as np

from config.config import METADATA_PATH, DATASET_PATH
from src.data_loader import load_dataset
from src.train import train_and_evaluate_all
from src.evaluate import calculate_residuals
from src.prediction import predict_batch
from components.cards import section_header, metric_card, info_card
from components.charts import (
    plot_actual_vs_predicted,
    plot_residuals,
    plot_model_comparison_bar
)

def render_page(is_noisy: bool):
    st.title("🤖 Model Performance & Evaluation")
    st.markdown("<p style='color: #8892B0;'>Empirical benchmarking of 10 traditional ML algorithms, cross-validation, and error diagnostics.</p>", unsafe_allow_html=True)
    
    if not os.path.exists(METADATA_PATH):
        st.warning("No metadata found. Please train models first on the Model Training page.")
        return
        
    with open(METADATA_PATH, "r") as f:
        metadata = json.load(f)
        
    all_metrics = metadata.get("all_model_metrics", {})
    best_model_name = metadata.get("best_model_name", "Random Forest")
    
    # Leaderboard Table
    st.markdown("### 🏆 Machine Learning Model Leaderboard")
    
    records = []
    for m_name, m_dict in all_metrics.items():
        rec = {"Model": m_name}
        rec.update(m_dict)
        records.append(rec)
        
    df_leaderboard = pd.DataFrame(records)
    st.dataframe(
        df_leaderboard.style.highlight_max(axis=0, subset=["R2", "CV_R2_Mean"], color="#1E3A8A")
        .highlight_min(axis=0, subset=["MAE", "RMSE", "MSE"], color="#064E3B")
        .format({
            "MAE": "{:.4f}", "MSE": "{:.4f}", "RMSE": "{:.4f}",
            "R2": "{:.4f}", "MAPE_pct": "{:.2f}%", "Explained_Variance": "{:.4f}",
            "CV_R2_Mean": "{:.4f}", "CV_R2_Std": "{:.4f}"
        }),
        use_container_width=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    section_header("Metric Comparison Charts", icon="📊")
    
    col_metric, col_chart = st.columns([1, 3])
    with col_metric:
        selected_metric = st.radio("Select Evaluation Metric", ["R2", "RMSE", "MAE", "MAPE_pct", "CV_R2_Mean"])
        info_card("Metric Definition", f"Selected **{selected_metric}** evaluates performance across all trained models.")
    with col_chart:
        fig_bar = plot_model_comparison_bar(df_leaderboard, metric_col=selected_metric)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_header("Actual vs Predicted & Residual Error Diagnostics", icon="🔍")
    
    try:
        df_raw = load_dataset(DATASET_PATH).sample(n=1000, random_state=42)
        target_col = metadata.get("target_col", "hx_1_heat_load_kw")
        df_pred = predict_batch(df_raw, is_noisy=is_noisy)
        
        y_actual = df_pred[target_col].values
        y_pred = df_pred["Predicted_Heat_Load_kW"].values
        df_res = calculate_residuals(y_actual, y_pred)
        
        c1, c2 = st.columns(2)
        with c1:
            fig_scat = plot_actual_vs_predicted(df_res)
            st.plotly_chart(fig_scat, use_container_width=True)
        with c2:
            fig_res = plot_residuals(df_res)
            st.plotly_chart(fig_res, use_container_width=True)
    except Exception as e:
        st.error(f"Error computing residual charts: {e}")
