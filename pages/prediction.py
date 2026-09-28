import streamlit as st
import pandas as pd

from src.prediction import predict_single
from src.engineering import calculate_thermal_performance
from src.explainability import explain_single_prediction
from components.cards import prediction_card, section_header, info_card, metric_card

def render_page(is_noisy: bool):
    st.title("🎯 Performance Prediction")
    st.markdown("<p style='color: #8892B0;'>Interactive prediction panel for Heat Exchanger Heat Duty & Thermal Performance.</p>", unsafe_allow_html=True)
    
    suffix = "_noisy" if is_noisy else ""
    
    st.markdown("### 🎛️ Input Operating Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        t_hot_in = st.slider(
            "Hot Fluid Inlet Temperature (K)",
            min_value=370.0,
            max_value=580.0,
            value=473.15,
            step=1.0,
            help="Temperature of the entering hot fluid stream in Kelvin."
        )
        m_cold_in = st.slider(
            "Cold Fluid Inlet Mass Flow Rate (kg/s)",
            min_value=0.5,
            max_value=5.0,
            value=2.75,
            step=0.05,
            help="Mass flow rate of the coolant stream in kg/s."
        )
        p_hot_out = st.number_input(
            "Hot Stream Outlet Pressure (Pa)",
            value=500000.0,
            step=1000.0
        )
        
    with col2:
        m_hot_out = st.number_input(
            "Hot Stream Mass Flow Rate (kg/s)",
            value=1.0,
            step=0.1
        )
        p_cold_out = st.number_input(
            "Cold Stream Outlet Pressure (Pa)",
            value=100000.0,
            step=1000.0
        )
        
    input_dict = {
        f"hot_inlet_temperature_k{suffix}": t_hot_in,
        f"cold_inlet_mass_flow_kg_s{suffix}": m_cold_in,
        f"hot_outlet_pressure_pa{suffix}": p_hot_out,
        f"cold_outlet_pressure_pa{suffix}": p_cold_out,
        f"hot_outlet_mass_flow_kg_s{suffix}": m_hot_out,
        f"cold_outlet_mass_flow_kg_s{suffix}": m_cold_in
    }
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 RUN PERFORMANCE PREDICTION", type="primary", use_container_width=True):
        try:
            res = predict_single(input_dict, is_noisy=is_noisy)
            pred_q = res["predicted_heat_load_kw"]
            unc_std = res["uncertainty_std_kw"]
            ci = res["confidence_interval_95"]
            
            prediction_card(
                "PREDICTED HEAT LOAD (HEAT DUTY)",
                f"{pred_q:.2f}",
                unit="kW",
                subtitle=f"95% Confidence Interval: [{ci[0]:.2f} kW - {ci[1]:.2f} kW] (±{1.96*unc_std:.2f} kW)"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            section_header("Physics-Aware Thermal Performance Breakdown", icon="🌡️")
            
            # Physics calculations
            thermal_res = calculate_thermal_performance(t_hot_in, m_cold_in, pred_q, m_hot_in=m_hot_out)
            
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                metric_card("Est. Hot Outlet Temp", f"{thermal_res['estimated_t_hot_out_k']} K", f"ΔT_hot: {thermal_res['hot_stream_delta_t_k']} K")
            with c2:
                metric_card("Est. Coolant Outlet Temp", f"{thermal_res['estimated_t_cold_out_k']} K", f"ΔT_cold: {thermal_res['cold_stream_delta_t_k']} K")
            with c3:
                metric_card("Thermal Effectiveness (ε)", f"{thermal_res['thermal_effectiveness']*100:.1f}%", f"Q_max: {thermal_res['q_max_possible_kw']} kW")
            with c4:
                metric_card("Estimated LMTD", f"{thermal_res['estimated_lmtd_k']} K", "Counter-flow approximation")

            st.markdown("<br>", unsafe_allow_html=True)
            section_header("Prediction Narrative & Influence", icon="🧠")
            exp_res = explain_single_prediction(input_dict, is_noisy=is_noisy)
            info_card("Model Explanation", exp_res["narrative"])
            
        except Exception as e:
            st.error(f"Error during prediction: {e}. Ensure the model is trained.")
