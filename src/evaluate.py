import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    mean_absolute_percentage_error,
    explained_variance_score
)

def evaluate_regression_model(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """
    Computes regression evaluation metrics.
    """
    mae = float(mean_absolute_error(y_true, y_pred))
    mse = float(mean_squared_error(y_true, y_pred))
    rmse = float(np.sqrt(mse))
    r2 = float(r2_score(y_true, y_pred))
    
    # Handle MAPE safely avoiding zero division
    try:
        mape = float(mean_absolute_percentage_error(y_true, y_pred)) * 100.0
    except Exception:
        mape = float(np.mean(np.abs((y_true - y_pred) / np.clip(y_true, 1e-6, None)))) * 100.0
        
    evs = float(explained_variance_score(y_true, y_pred))
    
    return {
        "MAE": round(mae, 4),
        "MSE": round(mse, 4),
        "RMSE": round(rmse, 4),
        "R2": round(r2, 4),
        "MAPE_pct": round(mape, 4),
        "Explained_Variance": round(evs, 4)
    }

def calculate_residuals(y_true: np.ndarray, y_pred: np.ndarray) -> pd.DataFrame:
    """
    Generates dataframe of actual, predicted, and residual values for plotting.
    """
    residuals = y_true - y_pred
    pct_residuals = (residuals / np.clip(y_true, 1e-6, None)) * 100.0
    
    return pd.DataFrame({
        "Actual": y_true,
        "Predicted": y_pred,
        "Residual": residuals,
        "Percentage_Residual": pct_residuals
    })
