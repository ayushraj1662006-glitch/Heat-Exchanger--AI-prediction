import os
import pandas as pd
import numpy as np
from config.config import DATASET_PATH, RAW_CLEAN_COLUMNS, RAW_NOISY_COLUMNS

def load_dataset(filepath: str = DATASET_PATH) -> pd.DataFrame:
    """
    Loads raw dataset from file path with error handling.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset file not found at: {filepath}")
    
    df = pd.read_csv(filepath)
    return df

def validate_dataset(df: pd.DataFrame) -> dict:
    """
    Validates the dataset and returns a data health report dictionary.
    """
    total_rows = len(df)
    total_cols = len(df.columns)
    missing_counts = df.isnull().sum().to_dict()
    total_missing = sum(missing_counts.values())
    duplicate_count = df.duplicated().sum()
    
    # Identify clean and noisy columns
    clean_cols_present = [c for c in RAW_CLEAN_COLUMNS if c in df.columns]
    noisy_cols_present = [c for c in RAW_NOISY_COLUMNS if c in df.columns]
    
    # Numeric column validation
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
    
    # Constant columns check
    constant_cols = [col for col in df.columns if df[col].nunique() <= 1]
    
    report = {
        "status": "VALID" if total_rows > 0 and len(clean_cols_present) > 0 else "INVALID",
        "rows": total_rows,
        "cols": total_cols,
        "total_missing": total_missing,
        "missing_by_column": missing_counts,
        "duplicate_rows": int(duplicate_count),
        "clean_columns_found": len(clean_cols_present),
        "noisy_columns_found": len(noisy_cols_present),
        "numeric_columns": numeric_cols,
        "non_numeric_columns": non_numeric_cols,
        "constant_columns": constant_cols
    }
    
    return report

def get_clean_and_noisy_splits(df: pd.DataFrame):
    """
    Returns separate dataframes for clean physical data and noisy sensor data.
    """
    clean_cols = [c for c in RAW_CLEAN_COLUMNS if c in df.columns]
    noisy_cols = [c for c in RAW_NOISY_COLUMNS if c in df.columns]
    
    clean_df = df[clean_cols].copy() if clean_cols else pd.DataFrame()
    noisy_df = df[noisy_cols].copy() if noisy_cols else pd.DataFrame()
    
    return clean_df, noisy_df
