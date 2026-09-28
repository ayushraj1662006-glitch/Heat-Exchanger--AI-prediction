import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple

from config.config import MODEL_PATH, PIPELINE_PATH, METADATA_PATH, PRIMARY_TARGET
from src.feature_engineering import create_engineering_features, get_feature_names

def load_trained_pipeline_and_model():
    """
    Loads saved Scikit-Learn preprocessing pipeline and best model.
    """
    if not os.path.exists(MODEL_PATH) or not os.path.exists(PIPELINE_PATH):
        raise FileNotFoundError("Trained model or pipeline not found. Please train the model first.")
        
    model = joblib.load(MODEL_PATH)
    pipeline = joblib.load(PIPELINE_PATH)
    return pipeline, model

def predict_single(input_dict: dict, is_noisy: bool = False) -> Dict[str, Any]:
    """
    Predicts Heat Load (kW) for a single input record with uncertainty estimation.
    """
    pipeline, model = load_trained_pipeline_and_model()
    
    # Convert input dict to DataFrame
    df_input = pd.DataFrame([input_dict])
    
    # Create engineered features
    df_feat = create_engineering_features(df_input, is_noisy=is_noisy)
    feature_cols = get_feature_names(is_noisy=is_noisy)
    
    # Ensure all required features are present (fill missing engineered with 0 if any)
    for col in feature_cols:
        if col not in df_feat.columns:
            df_feat[col] = 0.0
            
    X_input = df_feat[feature_cols]
    
    # Transform
    X_scaled = pipeline.transform(X_input)
    
    # Prediction
    pred_val = float(model.predict(X_scaled)[0])
    
    # Uncertainty estimation using tree ensemble variance if model supports estimators_
    std_uncertainty = 0.0
    if hasattr(model, "estimators_"):
        tree_preds = [t.predict(X_scaled)[0] for t in model.estimators_]
        std_uncertainty = float(np.std(tree_preds))
        
    ci_lower = max(0.0, pred_val - 1.96 * std_uncertainty)
    ci_upper = pred_val + 1.96 * std_uncertainty
    
    return {
        "predicted_heat_load_kw": round(pred_val, 4),
        "uncertainty_std_kw": round(std_uncertainty, 4),
        "confidence_interval_95": (round(ci_lower, 4), round(ci_upper, 4)),
        "input_features_used": feature_cols
    }

def predict_batch(df_input: pd.DataFrame, is_noisy: bool = False) -> pd.DataFrame:
    """
    Predicts Heat Load (kW) for a batch DataFrame.
    """
    pipeline, model = load_trained_pipeline_and_model()
    
    df_feat = create_engineering_features(df_input, is_noisy=is_noisy)
    feature_cols = get_feature_names(is_noisy=is_noisy)
    
    for col in feature_cols:
        if col not in df_feat.columns:
            df_feat[col] = 0.0
            
    X_input = df_feat[feature_cols]
    X_scaled = pipeline.transform(X_input)
    
    preds = model.predict(X_scaled)
    df_result = df_input.copy()
    df_result["Predicted_Heat_Load_kW"] = preds
    
    return df_result
