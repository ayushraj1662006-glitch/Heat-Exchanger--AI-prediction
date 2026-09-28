import os

# Project Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "heat_exchanger_dataset.csv")
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "cleaned_dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "best_model.joblib")
PIPELINE_PATH = os.path.join(MODEL_DIR, "pipeline.joblib")
METADATA_PATH = os.path.join(MODEL_DIR, "model_metadata.json")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
HERO_IMAGE_PATH = os.path.join(ASSETS_DIR, "images", "heat_exchanger_hero.jpg")
PROCESS_IMAGE_PATH = os.path.join(ASSETS_DIR, "images", "process_overview.jpg")

# Data Columns
RAW_CLEAN_COLUMNS = [
    "hot_inlet_temperature_k",
    "cold_inlet_mass_flow_kg_s",
    "hot_outlet_temperature_k",
    "cold_outlet_temperature_k",
    "hx_1_heat_load_kw",
    "hot_outlet_pressure_pa",
    "cold_outlet_pressure_pa",
    "hot_outlet_mass_flow_kg_s",
    "cold_outlet_mass_flow_kg_s",
    "hx_1_logarithmic_mean_temperature_difference_lmtd_k"
]

RAW_NOISY_COLUMNS = [c + "_noisy" for c in RAW_CLEAN_COLUMNS]

# Primary Target Variable
PRIMARY_TARGET = "hx_1_heat_load_kw"

# Input Operating Variables for Prediction (Avoiding Target Leakage)
# Outlet temperatures & LMTD are outputs of the process, so for performance prediction we use operating inputs:
INPUT_FEATURES_CLEAN = [
    "hot_inlet_temperature_k",
    "cold_inlet_mass_flow_kg_s",
    "hot_outlet_pressure_pa",
    "cold_outlet_pressure_pa",
    "hot_outlet_mass_flow_kg_s",
    "cold_outlet_mass_flow_kg_s"
]

INPUT_FEATURES_NOISY = [
    "hot_inlet_temperature_k_noisy",
    "cold_inlet_mass_flow_kg_s_noisy",
    "hot_outlet_pressure_pa_noisy",
    "cold_outlet_pressure_pa_noisy",
    "hot_outlet_mass_flow_kg_s_noisy",
    "cold_outlet_mass_flow_kg_s_noisy"
]

# Physical Constants (Air / Thermal fluid approximations for engineering validation)
DEFAULT_CP_HOT = 1.005  # kJ/(kg.K) (Approximate specific heat capacity)
DEFAULT_CP_COLD = 4.184 # kJ/(kg.K) (Water / reference coolant specific heat)

# App UI Settings
APP_TITLE = "HEAT-X AI | Performance Prediction & Optimization System"
THEME_DARK = {
    "bg_color": "#0E1117",
    "card_bg": "#1E222D",
    "text_color": "#E0E6ED",
    "primary": "#00D2FF",
    "secondary": "#3A7BD5",
    "accent": "#00F2FE",
    "warning": "#FFB703",
    "danger": "#EF476F",
    "success": "#06D6A0"
}
