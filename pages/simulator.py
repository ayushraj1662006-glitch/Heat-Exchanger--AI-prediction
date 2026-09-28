import streamlit as st
import pandas as pd

from src.prediction import predict_single
from src.engineering import calculate_thermal_performance
from components.cards import section_header, metric_card, info_card, prediction_card
from components.charts import plot_what_if_comparison

def render_page(is_noisy: bool):
    st.title("🧪 What-If Simulator")
    st.markdown("<p style='color: #8892B0;'>Interactive thermal scenario simulator to evaluate process modifications and operating shifts.</p>", unsafe_allow_html=True)
    
    suffix = "_noisy" if is_noisy else ""
    
    col_base, col_scen = st.columns(2)
    
    with col_base:
        st.markdown("### 1. Baseline Operating Conditions")
        base_t_hot = st.number_input("Baseline Hot Inlet Temp (K)", value=473.15, key="b_t")
        base_m_cold = st.number_input("Baseline Cold Mass Flow (kg/s)", value=2.75, key="b_m")
        base_p_hot = st.number_input("Baseline Hot Pressure (Pa)", value=500000.0, key="b_p")
        base_p_cold = st.number_input("Baseline Cold Pressure (Pa)", value=100000.0, key="b_pc")
        
    with col_scen:
        st.markdown("### 2. Modified Scenario Conditions")
        scen_t_hot = st.slider("Modified Hot Inlet Temp (K)", 370.0, 580.0, base_t_hot, 1.0, key="s_t")
        scen_m_cold = st.slider("Modified Cold Mass Flow (kg/s)", 0.5, 5.0, base_m_cold, 0.1, key="s_m")
        scen_p_hot = st.number_input("Modified Hot Pressure (Pa)", value=base_p_hot, key="s_p")
        scen_p_cold = st.number_input("Modified Cold Pressure (Pa)", value=base_p_cold, key="s_pc")
        
    dict_base = {
        f"hot_inlet_temperature_k{suffix}": base_t_hot,
        f"cold_inlet_mass_flow_kg_s{suffix}": base_m_cold,
        f"hot_outlet_pressure_pa{suffix}": base_p_hot,
        f"cold_outlet_pressure_pa{suffix}": base_p_cold,
        f"hot_outlet_mass_flow_kg_s{suffix}": 1.0,
        f"cold_outlet_mass_flow_kg_s{suffix}": base_m_cold
    }
    
    dict_scen = {
        f"hot_inlet_temperature_k{suffix}": scen_t_hot,
        f"cold_inlet_mass_flow_kg_s{suffix}": scen_m_cold,
        f"hot_outlet_pressure_pa{suffix}": scen_p_hot,
        f"cold_outlet_pressure_pa{suffix}": scen_p_cold,
        f"hot_outlet_mass_flow_kg_s{suffix}": 1.0,
        f"cold_outlet_mass_flow_kg_s{suffix}": scen_m_cold
    }
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    try:
        res_b = predict_single(dict_base, is_noisy=is_noisy)
        res_s = predict_single(dict_scen, is_noisy=is_noisy)
        
        q_b = res_b["predicted_heat_load_kw"]
        q_s = res_s["predicted_heat_load_kw"]
        
        delta_q = q_s - q_b
        pct_change = (delta_q / q_b) * 100.0 if q_b != 0 else 0.0
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card("Baseline Prediction", f"{q_b:.2f} kW")
        with c2:
            metric_card("Scenario Prediction", f"{q_s:.2f} kW", border_color="#00D2FF")
        with c3:
            metric_card("Absolute Δ Heat Load", f"{delta_q:+.2f} kW", border_color="#06D6A0" if delta_q>=0 else "#EF476F")
        with c4:
            metric_card("Percentage Δ Change", f"{pct_change:+.2f}%")

        st.markdown("<br>", unsafe_allow_html=True)
        
        col_chart, col_therm = st.columns([1.2, 1])
        with col_chart:
            fig_comp = plot_what_if_comparison(q_b, q_s)
            st.plotly_chart(fig_comp, use_container_width=True)
        with col_therm:
            st.markdown("### Scenario Thermal Impact")
            therm_s = calculate_thermal_performance(scen_t_hot, scen_m_cold, q_s)
            st.write(f"- **Est. Hot Outlet Temp**: {therm_s['estimated_t_hot_out_k']} K")
            st.write(f"- **Est. Coolant Outlet Temp**: {therm_s['estimated_t_cold_out_k']} K")
            st.write(f"- **Thermal Effectiveness**: {therm_s['thermal_effectiveness']*100:.1f}%")
            st.write(f"- **Est. LMTD**: {therm_s['estimated_lmtd_k']} K")
            
    except Exception as e:
        st.error(f"Error executing What-If simulation: {e}")
