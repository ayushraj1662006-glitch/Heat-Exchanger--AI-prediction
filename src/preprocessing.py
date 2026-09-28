import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

class PhysicsOutlierCapper(BaseEstimator, TransformerMixin):
    """
    Custom transformer that caps physical outliers using IQR limits
    fitted ONLY on training data to prevent data leakage.
    """
    def __init__(self, iqr_multiplier=3.0):
        self.iqr_multiplier = iqr_multiplier
        self.lower_bounds_ = {}
        self.upper_bounds_ = {}

    def fit(self, X, y=None):
        X_df = pd.DataFrame(X)
        for col in X_df.columns:
            q25 = X_df[col].quantile(0.25)
            q75 = X_df[col].quantile(0.75)
            iqr = q75 - q25
            self.lower_bounds_[col] = q25 - self.iqr_multiplier * iqr
            self.upper_bounds_[col] = q75 + self.iqr_multiplier * iqr
        return self

    def transform(self, X):
        X_df = pd.DataFrame(X).copy()
        for col in X_df.columns:
            if col in self.lower_bounds_ and col in self.upper_bounds_:
                lb = self.lower_bounds_[col]
                ub = self.upper_bounds_[col]
                X_df[col] = np.clip(X_df[col], lb, ub)
        return X_df.values

def build_preprocessing_pipeline(scaler_type: str = "standard") -> Pipeline:
    """
    Constructs a robust Scikit-Learn preprocessing pipeline.
    """
    scaler = StandardScaler() if scaler_type == "standard" else RobustScaler()
    
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('capper', PhysicsOutlierCapper(iqr_multiplier=3.5)),
        ('scaler', scaler)
    ])
    
    return pipeline
