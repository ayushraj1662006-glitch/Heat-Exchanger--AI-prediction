import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
import shap

from src.prediction import load_trained_pipeline_and_model
from src.feature_engineering import get_feature_names

def get_native_feature_importance(is_noisy: bool = False) -> pd.DataFrame:
    """
    Returns native MDI feature importance dataframe from trained tree-based model.
    """
    pipeline, model = load_trained_pipeline_and_model()
    feature_cols = get_feature_names(is_noisy=is_noisy)
    
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = np.abs(model.coef_)
    else:
        importances = np.ones(len(feature_cols)) / len(feature_cols)
        
    df_imp = pd.DataFrame({
        "Feature": feature_cols[:len(importances)],
        "Importance": importances
    }).sort_values(by="Importance", ascending=False).reset_index(drop=True)
    
    df_imp["Importance_Pct"] = (df_imp["Importance"] / df_imp["Importance"].sum()) * 100.0
    return df_imp

def get_permutation_importance(X_val: pd.DataFrame, y_val: pd.Series) -> pd.DataFrame:
    """
    Calculates permutation feature importance on validation data.
    """
    pipeline, model = load_trained_pipeline_and_model()
    X_scaled = pipeline.transform(X_val)
    
    perm_res = permutation_importance(model, X_scaled, y_val, n_repeats=10, random_state=42, n_jobs=-1)
    
    df_perm = pd.DataFrame({
        "Feature": X_val.columns,
        "Permutation_Importance_Mean": perm_res.importances_mean,
        "Permutation_Importance_Std": perm_res.importances_std
    }).sort_values(by="Permutation_Importance_Mean", ascending=False).reset_index(drop=True)
    
    return df_perm

def compute_shap_values(X_sample: pd.DataFrame):
    """
    Computes SHAP values for a sample dataset.
    """
    pipeline, model = load_trained_pipeline_and_model()
    X_scaled = pipeline.transform(X_sample)
    
    try:
        explainer = shap.TreeExplainer(model)
        shap_vals = explainer.shap_values(X_scaled)
    except Exception:
        # Fallback to KernelExplainer
        explainer = shap.KernelExplainer(model.predict, shap.sample(X_scaled, 50))
        shap_vals = explainer.shap_values(X_scaled)
        
    return explainer, shap_vals, X_scaled

def explain_single_prediction(input_dict: dict, is_noisy: bool = False) -> dict:
    """
    Generates human-readable engineering narrative explanation for a single prediction.
    """
    df_imp = get_native_feature_importance(is_noisy=is_noisy)
    top_feats = df_imp.head(3)["Feature"].tolist()
    
    t_hot = input_dict.get("hot_inlet_temperature_k", input_dict.get("hot_inlet_temperature_k_noisy", 473.15))
    m_cold = input_dict.get("cold_inlet_mass_flow_kg_s", input_dict.get("cold_inlet_mass_flow_kg_s_noisy", 2.75))
    
    narrative = (
        f"The predicted heat-transfer performance is primarily influenced by **{top_feats[0]}** "
        f"and **{top_feats[1]}**. Operating at a hot inlet temperature of **{t_hot:.1f} K** "
        f"and a cold coolant flow rate of **{m_cold:.2f} kg/s**, the model associates higher thermal energy "
        f"input and coolant mass throughput with an elevated heat transfer rate."
    )
    
    return {
        "top_features": top_feats,
        "narrative": narrative,
        "feature_importance_df": df_imp
    }
