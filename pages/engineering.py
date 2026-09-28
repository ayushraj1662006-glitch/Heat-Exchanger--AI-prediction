import streamlit as st
import pandas as pd
import numpy as np

from config.config import DATASET_PATH
from src.data_loader import load_dataset
from src.prediction import predict_batch
from src.engineering import validate_physics_sanity
from components.cards import section_header, metric_card, info_card, warning_card

def render_page(is_noisy: bool):
    st.title("⚙️ Engineering Analysis & Physics Validation")
    st.markdown("<p style='color: #8892B0;'>Mechanical & thermal engineering verification of ML predictions against first-principles energy balance.</p>", unsafe_allow_html=True)
    
    try:
        df = load_dataset(DATASET_PATH)
        df_sample = df.sample(n=500, random_state=42)
        target_col = "hx_1_heat_load_kw_noisy" if is_noisy else "hx_1_heat_load_kw"
        
        pred_df = predict_batch(df_sample, is_noisy=is_noisy)
        pred_q = pred_df["Predicted_Heat_Load_kW"].values
        
        sanity_report = validate_physics_sanity(df_sample, pred_q)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            metric_card("Evaluated Samples", f"{sanity_report['total_evaluated']:,}")
        with c2:
            metric_card("Negative Predictions", f"{sanity_report['negative_predictions']}")
        with c3:
            metric_card("Physics Plausibility", f"{sanity_report['plausibility_score_pct']}%", border_color="#06D6A0")

        st.markdown("<br>", unsafe_allow_html=True)
        section_header("First-Principles Governing Equations", icon="📐")
        
        col_eq1, col_eq2 = st.columns(2)
        with col_eq1:
            st.markdown(
                r"""
                ##### Energy Conservation Equation
                $$Q = \dot{m}_{hot} \cdot C_{p, hot} \cdot (T_{hot, in} - T_{hot, out})$$
                Verifies that heat lost by the hot fluid equals total heat duty transferred into coolant.
                """
            )
        with col_eq2:
            st.markdown(
                r"""
                ##### Logarithmic Mean Temperature Difference (LMTD)
                $$Q = U \cdot A \cdot \text{LMTD}$$
                where $\text{LMTD} = \frac{\Delta T_1 - \Delta T_2}{\ln(\Delta T_1 / \Delta T_2)}$
                Connects total heat duty to overall heat-transfer coefficient $U$ and surface area $A$.
                """
            )

        st.markdown("<br>", unsafe_allow_html=True)
        section_header("Physics & Engineering Verification Status", icon="✅")
        
        c_passed, c_unsupported = st.columns(2)
        with c_passed:
            st.markdown("##### Verified Relationships:")
            for check in sanity_report["checks_passed"]:
                st.write(f"✔️ {check}")
        with c_unsupported:
            st.markdown("##### Constraints & Unsupported Checks:")
            for check in sanity_report["checks_unsupported"]:
                st.write(f"⚠️ {check}")

        info_card("Engineering Disclaimer", "Physics sanity checks ensure ML predictions remain within thermodynamic boundaries. The model provides surrogate predictions and does not replace full CFD or physical testing.")
        
    except Exception as e:
        st.error(f"Error performing engineering analysis: {e}")
