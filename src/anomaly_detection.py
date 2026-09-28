import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

def detect_anomalies_isolation_forest(df: pd.DataFrame, contamination: float = 0.05, is_noisy: bool = False) -> pd.DataFrame:
    """
    Detects unusual operating conditions using Isolation Forest.
    """
    df_res = df.copy()
    
    suffix = "_noisy" if is_noisy else ""
    target_cols = [
        f"hot_inlet_temperature_k{suffix}",
        f"cold_inlet_mass_flow_kg_s{suffix}",
        f"hx_1_heat_load_kw{suffix}"
    ]
    # Filter available columns
    avail_cols = [c for c in target_cols if c in df_res.columns]
    
    if not avail_cols:
        avail_cols = df_res.select_dtypes(include=[np.number]).columns.tolist()[:3]
        
    iso = IsolationForest(contamination=contamination, random_state=42)
    labels = iso.fit_predict(df_res[avail_cols].fillna(0))
    scores = iso.decision_function(df_res[avail_cols].fillna(0))
    
    df_res["Anomaly_Flag"] = np.where(labels == -1, "Potentially Unusual", "Normal Operating")
    df_res["Anomaly_Score"] = scores
    df_res["Is_Anomaly"] = (labels == -1)
    
    return df_res

def get_anomaly_summary(df_anomalies: pd.DataFrame) -> dict:
    """
    Generates summary report of anomaly status.
    """
    total = len(df_anomalies)
    anomaly_count = int(df_anomalies["Is_Anomaly"].sum())
    normal_count = total - anomaly_count
    anomaly_pct = round((anomaly_count / total) * 100.0, 2)
    
    return {
        "total_observations": total,
        "normal_operating_count": normal_count,
        "unusual_condition_count": anomaly_count,
        "anomaly_percentage": anomaly_pct,
        "method_used": "Isolation Forest (Unsupervised ML Outlier Analysis)"
    }
