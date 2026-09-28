import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pytest
import pandas as pd
import numpy as np

from src.data_loader import load_dataset, validate_dataset
from src.feature_engineering import create_engineering_features, get_feature_names
from src.preprocessing import build_preprocessing_pipeline
from src.prediction import predict_single
from src.engineering import calculate_lmtd, calculate_thermal_performance
from src.anomaly_detection import detect_anomalies_isolation_forest

def test_data_loading():
    df = load_dataset()
    assert df is not None
    assert len(df) == 10000
    report = validate_dataset(df)
    assert report["status"] == "VALID"
    assert report["duplicate_rows"] == 0

def test_feature_engineering():
    df = load_dataset()
    df_feat = create_engineering_features(df, is_noisy=False)
    assert "feat_thermal_interaction" in df_feat.columns
    assert "feat_mass_flow_ratio" in df_feat.columns
    assert df_feat["feat_thermal_interaction"].isnull().sum() == 0

def test_preprocessing_pipeline():
    df = load_dataset()
    df_feat = create_engineering_features(df, is_noisy=False)
    feature_cols = get_feature_names(is_noisy=False)
    X = df_feat[feature_cols]
    
    pipeline = build_preprocessing_pipeline()
    X_scaled = pipeline.fit_transform(X)
    assert X_scaled.shape[0] == X.shape[0]
    assert X_scaled.shape[1] == X.shape[1]

def test_model_prediction():
    input_dict = {
        "hot_inlet_temperature_k": 473.15,
        "cold_inlet_mass_flow_kg_s": 2.75,
        "hot_outlet_pressure_pa": 500000.0,
        "cold_outlet_pressure_pa": 100000.0,
        "hot_outlet_mass_flow_kg_s": 1.0,
        "cold_outlet_mass_flow_kg_s": 2.75
    }
    res = predict_single(input_dict, is_noisy=False)
    assert "predicted_heat_load_kw" in res
    assert res["predicted_heat_load_kw"] > 0

def test_physics_calculations():
    lmtd = calculate_lmtd(473.15, 367.67, 298.15, 320.0)
    assert not np.isnan(lmtd)
    assert lmtd > 0
    
    thermal = calculate_thermal_performance(473.15, 2.75, 107.66)
    assert thermal["estimated_t_hot_out_k"] < 473.15
    assert thermal["thermal_effectiveness"] >= 0

def test_anomaly_detection():
    df = load_dataset().head(100)
    df_anom = detect_anomalies_isolation_forest(df, contamination=0.05)
    assert "Anomaly_Flag" in df_anom.columns
    assert "Is_Anomaly" in df_anom.columns
