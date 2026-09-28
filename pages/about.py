import os
import streamlit as st

from config.config import PROCESS_IMAGE_PATH
from components.cards import section_header, info_card, warning_card

def render_page(is_noisy: bool):
    st.title("ℹ️ About HEAT-X AI")
    st.markdown("<p style='color: #8892B0;'>Technical background, thermal engineering methodology, and software architecture.</p>", unsafe_allow_html=True)
    
    if os.path.exists(PROCESS_IMAGE_PATH):
        st.image(PROCESS_IMAGE_PATH, caption="Industrial Thermal Process Control Monitor Overview", use_container_width=True)

    st.markdown("### 🎯 Project Objective")
    st.write(
        """
        The **AI-Based Heat Exchanger Performance Prediction & Optimization System** is a production-grade 
        decision-support tool designed for thermal and chemical process engineers. It uses strictly traditional 
        Machine Learning algorithms to accurately estimate heat exchanger heat duty ($Q$ in kW) from input operating 
        conditions, run what-if scenario simulations, detect operational anomalies, and provide explainable AI insights.
        """
    )
    
    st.markdown("### 🛠️ Technology Stack")
    st.markdown(
        """
        - **Language**: Python 3.11+
        - **Data Processing**: Pandas, NumPy, SciPy
        - **Machine Learning**: Scikit-Learn, XGBoost, LightGBM, CatBoost
        - **Explainability**: SHAP (SHapley Additive exPlanations), Permutation Importance
        - **Visualization**: Plotly Express & Plotly Graph Objects
        - **Frontend Dashboard**: Streamlit with Custom Industrial CSS
        """
    )

    st.markdown("### 🌡️ Thermal Engineering Background")
    st.write(
        """
        In process plants, shell-and-tube heat exchangers transfer thermal energy between hot fluid streams 
        and coolant streams. Traditional physical calculations rely on non-linear thermodynamic equations 
        and empirical fluid properties. Machine learning surrogate models learn these non-linear functional 
        mappings directly from data, enabling instant what-if evaluations and anomaly detection without 
        computationally expensive CFD or process simulation restarts.
        """
    )

    st.markdown("### ⚠️ Dataset Disclaimer & System Boundaries")
    warning_card(
        "Important Dataset & Industrial Boundary Notice",
        "This application uses benchmark/simulated data generated via DWSIM parametric sweep (10,000 observations) "
        "and is not a live industrial plant monitoring system. It provides machine learning decision support and surrogate "
        "modeling prototype capabilities. It does not replace physical instrumentation or safety relief valves."
    )
