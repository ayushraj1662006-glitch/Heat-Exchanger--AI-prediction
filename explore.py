import pandas as pd
import numpy as np
import json

df = pd.read_csv("dataset/heat_exchanger_dataset.csv")

print("=== DATASET OVERVIEW ===")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
print("\nColumns:")
for col in df.columns:
    print(f" - {col} ({df[col].dtype})")

print("\n=== MISSING VALUES ===")
print(df.isnull().sum())

print("\n=== DUPLICATE ROWS ===")
print(f"Duplicates: {df.duplicated().sum()}")

print("\n=== DESCRIPTIVE STATISTICS (Clean Columns) ===")
clean_cols = [c for c in df.columns if not c.endswith('_noisy')]
print(df[clean_cols].describe().T[['mean', 'std', 'min', '50%', 'max']])

print("\n=== DESCRIPTIVE STATISTICS (Noisy Columns) ===")
noisy_cols = [c for c in df.columns if c.endswith('_noisy')]
print(df[noisy_cols].describe().T[['mean', 'std', 'min', '50%', 'max']])

print("\n=== CORRELATION MATRIX (Target: hx_1_heat_load_kw) ===")
corr = df.corr()['hx_1_heat_load_kw'].sort_values(ascending=False)
print(corr)
