import os
import json
import streamlit as st
import pandas as pd

from config.config import DATASET_PATH, METADATA_PATH
from src.data_loader import load_dataset
from src.train import train_and_evaluate_all
from components.cards import section_header, metric_card, info_card, status_badge

def render_page(is_noisy: bool):
    st.title("🧠 Model Training & Retraining")
    st.markdown("<p style='color: #8892B0;'>Train, benchmark, hyperparameter-tune, and save production traditional ML models.</p>", unsafe_allow_html=True)
    
    try:
        df = load_dataset(DATASET_PATH)
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return

    # Metadata status
    metadata = {}
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "r") as f:
            metadata = json.load(f)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Dataset Rows", f"{len(df):,}")
    with c2:
        metric_card("Train / Test Split", "80% / 20%", "8,000 / 2,000 Samples")
    with c3:
        metric_card("Operating Mode", "Sensor Noise" if is_noisy else "Clean Simulation")
    with c4:
        metric_card("Current Best Model", metadata.get("best_model_name", "Random Forest"))

    st.markdown("<br>", unsafe_allow_html=True)
    section_header("Model Training Control Center", icon="⚙️")
    
    st.markdown(
        """
        Clicking the button below will execute the full ML pipeline:
        1. Fit Scikit-Learn `ColumnTransformer` & `StandardScaler` strictly on Train set.
        2. Benchmark 10 traditional ML algorithms (Dummy, Linear, Ridge, Random Forest, Extra Trees, Gradient Boosting, HistGradientBoosting, XGBoost, LightGBM, CatBoost).
        3. Perform 5-Fold Cross Validation.
        4. Select & save the best model to `models/best_model.joblib`.
        """
    )
    
    if st.button("🚀 TRAIN ALL MODELS & UPDATE PRODUCTION MODEL", type="primary", use_container_width=True):
        with st.spinner("Training models... Please wait..."):
            res = train_and_evaluate_all(is_noisy=is_noisy)
            st.success(f"Training completed successfully! Best Production Model: **{res['best_model_name']}**")
            
            st.markdown("### Updated Leaderboard Metrics:")
            df_lead = pd.DataFrame([
                {"Model": k, **v} for k, v in res["results"].items()
            ])
            st.dataframe(df_lead, use_container_width=True)
