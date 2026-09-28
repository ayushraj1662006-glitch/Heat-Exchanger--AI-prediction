import os
import sys
import pandas as pd
import numpy as np

def format_number(val: float, precision: int = 2, unit: str = "") -> str:
    """
    Formats a numeric value with given precision and physical unit.
    """
    if pd.isna(val):
        return "N/A"
    
    formatted = f"{val:,.{precision}f}"
    if unit:
        return f"{formatted} {unit}"
    return formatted

def generate_csv_report(df: pd.DataFrame, filename: str = "performance_report.csv") -> str:
    """
    Exports dataframe to CSV for downloadable report.
    """
    os.makedirs("reports", exist_ok=True)
    filepath = os.path.join("reports", filename)
    df.to_csv(filepath, index=False)
    return filepath
