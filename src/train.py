import os
import sys

# Ensure root directory is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import json
import joblib
import numpy as np
import pandas as pd
from datetime import datetime

from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import (
    RandomForestRegressor,
    ExtraTreesRegressor,
    GradientBoostingRegressor,
    HistGradientBoostingRegressor
)

# Optional ML libraries
try:
    from xgboost import XGBRegressor
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

try:
    from lightgbm import LGBMRegressor
    HAS_LGB = True
except ImportError:
    HAS_LGB = False

try:
    from catboost import CatBoostRegressor
    HAS_CAT = True
except ImportError:
    HAS_CAT = False

from config.config import (
    DATASET_PATH,
    MODEL_PATH,
    PIPELINE_PATH,
    METADATA_PATH,
    PRIMARY_TARGET
)
from src.data_loader import load_dataset
from src.feature_engineering import create_engineering_features, get_feature_names
from src.preprocessing import build_preprocessing_pipeline
from src.evaluate import evaluate_regression_model

def get_candidate_models(random_state: int = 42) -> dict:
    """
    Instantiates candidate traditional ML models.
    """
    models = {
        "Baseline (Dummy)": DummyRegressor(strategy="mean"),
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(alpha=1.0, random_state=random_state),
        "Random Forest": RandomForestRegressor(n_estimators=100, max_depth=15, random_state=random_state, n_jobs=-1),
        "Extra Trees": ExtraTreesRegressor(n_estimators=100, max_depth=15, random_state=random_state, n_jobs=-1),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=random_state),
        "HistGradientBoosting": HistGradientBoostingRegressor(max_iter=100, learning_rate=0.1, max_depth=8, random_state=random_state)
    }
    
    if HAS_XGB:
        models["XGBoost"] = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=6, random_state=random_state, n_jobs=-1)
    
    if HAS_LGB:
        models["LightGBM"] = LGBMRegressor(n_estimators=100, learning_rate=0.1, max_depth=6, random_state=random_state, verbose=-1, n_jobs=-1)
        
    if HAS_CAT:
        models["CatBoost"] = CatBoostRegressor(iterations=100, learning_rate=0.1, depth=6, random_seed=random_state, verbose=0)
        
    return models

def train_and_evaluate_all(is_noisy: bool = False, random_state: int = 42) -> dict:
    """
    Full pipeline training and model selection.
    """
    df_raw = load_dataset(DATASET_PATH)
    df_feat = create_engineering_features(df_raw, is_noisy=is_noisy)
    
    feature_cols = get_feature_names(is_noisy=is_noisy)
    target_col = PRIMARY_TARGET + ("_noisy" if is_noisy else "")
    
    # Ensure target and features are present
    feature_cols = [c for c in feature_cols if c in df_feat.columns]
    
    X = df_feat[feature_cols].copy()
    y = df_feat[target_col].copy()
    
    # Train / Test split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)
    
    # Fit preprocessing pipeline ONLY on training data
    pipeline = build_preprocessing_pipeline()
    X_train_scaled = pipeline.fit_transform(X_train)
    X_test_scaled = pipeline.transform(X_test)
    
    candidate_models = get_candidate_models(random_state=random_state)
    results = {}
    best_model_name = None
    best_r2 = -float("inf")
    best_trained_model = None
    
    kf = KFold(n_splits=5, shuffle=True, random_state=random_state)
    
    for name, model in candidate_models.items():
        # Fit model
        model.fit(X_train_scaled, y_train)
        
        # Test evaluation
        y_pred = model.predict(X_test_scaled)
        metrics = evaluate_regression_model(y_test, y_pred)
        
        # 5-Fold Cross Validation R2
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=kf, scoring='r2', n_jobs=-1 if name not in ["CatBoost"] else 1)
        metrics["CV_R2_Mean"] = round(float(np.mean(cv_scores)), 4)
        metrics["CV_R2_Std"] = round(float(np.std(cv_scores)), 4)
        
        results[name] = {
            "metrics": metrics,
            "model_obj": model
        }
        
        # Select best model based on Test R2 and CV R2 stability
        if metrics["R2"] > best_r2:
            best_r2 = metrics["R2"]
            best_model_name = name
            best_trained_model = model

    # Save trained model & pipeline
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(best_trained_model, MODEL_PATH)
    joblib.dump(pipeline, PIPELINE_PATH)
    
    # Summary results table for metadata
    summary_metrics = {name: res["metrics"] for name, res in results.items()}
    
    metadata = {
        "best_model_name": best_model_name,
        "is_noisy_mode": is_noisy,
        "target_col": target_col,
        "features": feature_cols,
        "num_train_samples": len(X_train),
        "num_test_samples": len(X_test),
        "training_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "best_model_metrics": results[best_model_name]["metrics"],
        "all_model_metrics": summary_metrics
    }
    
    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=4)
        
    return {
        "results": summary_metrics,
        "best_model_name": best_model_name,
        "metadata": metadata,
        "X_test": X_test,
        "y_test": y_test,
        "feature_names": feature_cols
    }

if __name__ == "__main__":
    print("Training models...")
    res = train_and_evaluate_all()
    print(f"Training completed! Best Model: {res['best_model_name']}")
    print(f"Metrics: {res['metadata']['best_model_metrics']}")
