import pandas as pd
import numpy as np

df = pd.read_csv("dataset/heat_exchanger_dataset.csv")

# Q = m_dot_hot * Cp_hot * (T_hot_in - T_hot_out)
# Let's check if Cp_hot is constant or function of temperature
# Q (in kW) = m_dot_hot (kg/s) * Cp_hot (kJ/kg.K) * (T_hot_in - T_hot_out)

m_hot = df['hot_outlet_mass_flow_kg_s'] # 1.0 kg/s
dT_hot = df['hot_inlet_temperature_k'] - df['hot_outlet_temperature_k']
Q_kw = df['hx_1_heat_load_kw']

# Estimate implicit Cp_hot
Cp_hot_estimated = Q_kw / (m_hot * dT_hot)

print("=== Implicit Cp_hot Estimation (kW / (kg/s * K)) ===")
print(Cp_hot_estimated.describe())

# Check LMTD equation:
# LMTD = ((T_hot_in - T_cold_out) - (T_hot_out - T_cold_in)) / ln((T_hot_in - T_cold_out)/(T_hot_out - T_cold_in))
# Let's see if cold inlet temperature was omitted or constant in DWSIM simulation
print("\n=== LMTD vs Q ===")
print(df[['hx_1_heat_load_kw', 'hx_1_logarithmic_mean_temperature_difference_lmtd_k']].head(10))

