import streamlit as st
import pandas as pd
import numpy as np

from config.config import DATASET_PATH
from src.data_loader import load_dataset
from src.explainability import (
    get_native_feature_importance,
    get_permutation_importance,
    explain_single_prediction
)
from components.cards import section_header, info_card
from components.charts import plot_feature_importance

def render_page(is_noisy: bool):
    st.title("🔍 Explainable AI (XAI)")
    st.markdown("<p style='color: #8892B0;'>Model transparency, feature importance, permutation importance, and local prediction explanations.</p>", unsafe_allow_html=True)
    
    try:
        df_imp = get_native_feature_importance(is_noisy=is_noisy)
    except Exception as e:
        st.error(f"Error loading feature importances: {e}. Train the model first.")
        return
        
    tab_global, tab_sample = st.tabs(["🌐 Global Feature Importance", "🎯 Local Prediction Explanation"])
    
    with tab_global:
        st.markdown("### Global Feature Ranking (Native Model Importance)")
        
        c1, c2 = st.columns([1.5, 1])
        with c1:
            fig_imp = plot_feature_importance(df_imp, top_n=10)
            st.plotly_chart(fig_imp, use_container_width=True)
        with c2:
            st.markdown("##### Feature Importance Data Table")
            st.dataframe(df_imp.style.format({"Importance": "{:.4f}", "Importance_Pct": "{:.2f}%"}), use_container_width=True)
            
        info_card("Interpretability Rule", "Features with high importance strongly influence the decision trees. Note that tree-based feature importances indicate predictive association, not direct physical causality.")
        
    with tab_sample:
        st.markdown("### Local Sample Explanation Generator")
        st.write("Select an operating point to inspect local feature drivers and natural language narrative:")
        
        try:
            df = load_dataset(DATASET_PATH)
            sample_idx = st.number_input("Select Dataset Row Index", 0, len(df)-1, 10)
            row_dict = df.iloc[sample_idx].to_dict()
            
            exp = explain_single_prediction(row_dict, is_noisy=is_noisy)
            
            st.markdown("##### Natural Language Explanation Narrative:")
            info_card("Prediction Explanation", exp["narrative"])
            
            st.markdown("##### Key Influencing Variables:")
            for idx, feat in enumerate(exp["top_features"], 1):
                st.write(f"**{idx}. {feat}**")
        except Exception as e:
            st.error(f"Error generating sample explanation: {e}")
