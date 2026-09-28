import pandas as pd
import numpy as np

df = pd.read_csv("dataset/heat_exchanger_dataset.csv")

print("=== CHECK CONSTANT COLUMNS IN CLEAN DATA ===")
for col in df.columns:
    std = df[col].std()
    nunique = df[col].nunique()
    print(f"{col:<65} | Unique: {nunique:<6} | Min: {df[col].min():<10.2f} | Max: {df[col].max():<10.2f} | Std: {std:<10.4f}")

print("\n=== ARE hx_1_heat_load_kw AND LMTD IDENTICAL IN CLEAN DATA? ===")
diff = (df['hx_1_heat_load_kw'] - df['hx_1_logarithmic_mean_temperature_difference_lmtd_k']).abs().max()
print(f"Max absolute difference: {diff}")

print("\n=== NOISE LEVEL ESTIMATION ===")
clean_cols = [c for c in df.columns if not c.endswith('_noisy')]
for col in clean_cols:
    noisy_col = col + "_noisy"
    if noisy_col in df.columns:
        diff_noise = df[noisy_col] - df[col]
        print(f"{col:<55} | Noise Mean: {diff_noise.mean():.4f} | Noise Std: {diff_noise.std():.4f}")

