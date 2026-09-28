import pandas as pd
import numpy as np

def create_engineering_features(df: pd.DataFrame, is_noisy: bool = False) -> pd.DataFrame:
    """
    Engineers domain-specific thermal features from heat exchanger operating variables.
    Handles both clean and noisy feature names dynamically.
    """
    df_feat = df.copy()
    
    suffix = "_noisy" if is_noisy else ""
    t_hot_in_col = f"hot_inlet_temperature_k{suffix}"
    m_cold_col = f"cold_inlet_mass_flow_kg_s{suffix}"
    p_hot_col = f"hot_outlet_pressure_pa{suffix}"
    p_cold_col = f"cold_outlet_pressure_pa{suffix}"
    m_hot_col = f"hot_outlet_mass_flow_kg_s{suffix}"

    # Verify key columns exist
    if t_hot_in_col in df_feat.columns and m_cold_col in df_feat.columns:
        # 1. Thermal interaction parameter (Inlet Temperature x Cold Mass Flow)
        df_feat['feat_thermal_interaction'] = df_feat[t_hot_in_col] * df_feat[m_cold_col]
        
        # 2. Mass flow ratio (Cold mass flow / Hot mass flow)
        if m_hot_col in df_feat.columns:
            # Add small epsilon to prevent division by zero
            df_feat['feat_mass_flow_ratio'] = df_feat[m_cold_col] / (df_feat[m_hot_col] + 1e-6)
            df_feat['feat_hot_enthalpy_proxy'] = df_feat[m_hot_col] * df_feat[t_hot_in_col]
        
        # 3. Cold energy rate capacity proxy
        df_feat['feat_cold_capacity_proxy'] = df_feat[m_cold_col] * df_feat[t_hot_in_col]
        
        # 4. Temperature non-linear features
        df_feat['feat_t_hot_in_sq'] = df_feat[t_hot_in_col] ** 2
        df_feat['feat_m_cold_sq'] = df_feat[m_cold_col] ** 2
        df_feat['feat_temp_delta_ref'] = df_feat[t_hot_in_col] - 298.15 # Relative to standard ambient (298.15K)

    # 5. Pressure ratios and differences
    if p_hot_col in df_feat.columns and p_cold_col in df_feat.columns:
        df_feat['feat_pressure_diff_pa'] = df_feat[p_hot_col] - df_feat[p_cold_col]
        df_feat['feat_pressure_ratio'] = df_feat[p_hot_col] / (df_feat[p_cold_col] + 1e-6)
        
    return df_feat

def get_feature_names(is_noisy: bool = False) -> list:
    """
    Returns the full list of input features (raw + engineered) used for model training.
    """
    suffix = "_noisy" if is_noisy else ""
    raw_features = [
        f"hot_inlet_temperature_k{suffix}",
        f"cold_inlet_mass_flow_kg_s{suffix}",
        f"hot_outlet_pressure_pa{suffix}",
        f"cold_outlet_pressure_pa{suffix}",
        f"hot_outlet_mass_flow_kg_s{suffix}",
        f"cold_outlet_mass_flow_kg_s{suffix}"
    ]
    
    engineered = [
        'feat_thermal_interaction',
        'feat_mass_flow_ratio',
        'feat_hot_enthalpy_proxy',
        'feat_cold_capacity_proxy',
        'feat_t_hot_in_sq',
        'feat_m_cold_sq',
        'feat_temp_delta_ref',
        'feat_pressure_diff_pa',
        'feat_pressure_ratio'
    ]
    
    return raw_features + engineered
