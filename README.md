# HEAT-X AI | AI-Based Heat Exchanger Performance Prediction & Optimization System

An industrial-ready machine-learning decision-support system for shell-and-tube heat exchanger performance prediction, what-if optimization, explainable AI, and unsupervised anomaly detection.

---

## 📄 1. Project Overview

**HEAT-X AI** is an industrial decision-support tool tailored for chemical, process, and thermal energy engineers. Built using traditional Machine Learning (Scikit-Learn, XGBoost, LightGBM, CatBoost), Streamlit, and Plotly, the system predicts heat exchanger thermal duty ($Q$ in kW) from operating parameters, models physical behavior, performs scenario simulations, and monitors for operational anomalies.

---

## 🎯 2. Problem Statement

In industrial process plants, heat exchangers undergo operational fluctuations in fluid flow rates, inlet temperatures, and stream pressures. Physics-based first-principle models or CFD simulations are computationally intensive and require manual recalibration. **HEAT-X AI** serves as a fast, high-accuracy machine learning surrogate model trained strictly on physical process simulation data (10,000 observations) to instantly predict heat load and evaluate process optimization strategies.

---

## 🌡️ 3. Mechanical Engineering Background

For counter-flow shell-and-tube heat exchangers:
1. **Energy Conservation**:
   $$Q = \dot{m}_{hot} \cdot C_{p, hot} \cdot (T_{hot, in} - T_{hot, out}) = \dot{m}_{cold} \cdot C_{p, cold} \cdot (T_{cold, out} - T_{cold, in})$$
2. **Logarithmic Mean Temperature Difference (LMTD)**:
   $$Q = U \cdot A \cdot \text{LMTD}, \quad \text{LMTD} = \frac{\Delta T_1 - \Delta T_2}{\ln(\Delta T_1 / \Delta T_2)}$$
3. **Thermal Effectiveness ($\epsilon$)**:
   $$\epsilon = \frac{Q}{Q_{max}} = \frac{Q}{C_{min} \cdot (T_{hot, in} - T_{cold, in})}$$

---

## 🚀 4. Objectives

- Learn functional mappings between operating variables ($T_{hot, in}$, $\dot{m}_{cold}$, pressures) and performance ($Q$ in kW).
- Prevent target leakage by using ONLY inlet operating conditions for predictions.
- Compare 10 traditional ML regression models (Dummy, Linear, Ridge, Random Forest, Extra Trees, Gradient Boosting, HistGradientBoosting, XGBoost, LightGBM, CatBoost).
- Provide Explainable AI (SHAP & Permutation Importance) and Isolation Forest anomaly detection.
- Provide interactive what-if simulation and automated technical reports.

---

## 📊 5. Dataset Information

- **Source**: DWSIM Parametric Simulation Dataset (`dataset/heat_exchanger_dataset.csv`).
- **Rows**: 10,000 observations ($100 \times 100$ grid sweep over $T_{hot, in}$ and $\dot{m}_{cold}$).
- **Columns**: 20 numerical columns (10 clean physical values + 10 corresponding Gaussian noisy sensor values).
- **Primary Target**: `hx_1_heat_load_kw` (Heat load in kW).

---

## ⚙️ 6. Features

| Feature Name | Description | Units | Type |
|---|---|---|---|
| `hot_inlet_temperature_k` | Hot stream inlet temperature | K | Operating Input |
| `cold_inlet_mass_flow_kg_s` | Cold stream inlet mass flow rate | kg/s | Operating Input |
| `hot_outlet_pressure_pa` | Hot stream outlet pressure | Pa | Operating Input |
| `cold_outlet_pressure_pa` | Cold stream outlet pressure | Pa | Operating Input |
| `hot_outlet_mass_flow_kg_s` | Hot stream outlet mass flow rate | kg/s | Operating Input |
| `cold_outlet_mass_flow_kg_s` | Cold stream outlet mass flow rate | kg/s | Operating Input |
| `hx_1_heat_load_kw` | Heat load / thermal duty | kW | Target |

---

## 🤖 7. ML Methodology & Pipeline

1. **Validation & Cleaning**: Data schema validation, zero missing values, zero duplicates.
2. **Data Leakage Prevention**: Split into 80% Train and 20% Test. Scikit-Learn `ColumnTransformer` & `StandardScaler` fitted strictly on Train data.
3. **Feature Engineering**: Thermal interaction terms ($T_{in} \cdot \dot{m}$), mass flow ratios ($\dot{m}_{cold} / \dot{m}_{hot}$), energy enthalpy proxies, quadratic non-linear terms.
4. **Cross-Validation**: 5-Fold K-Fold Cross Validation.

---

## 📈 8. Feature Engineering

Engineered features derived strictly from available inlet operating parameters:
- `feat_thermal_interaction` = $T_{hot, in} \times \dot{m}_{cold}$
- `feat_mass_flow_ratio` = $\dot{m}_{cold} / (\dot{m}_{hot} + \epsilon)$
- `feat_hot_enthalpy_proxy` = $\dot{m}_{hot} \times T_{hot, in}$
- `feat_cold_capacity_proxy` = $\dot{m}_{cold} \times T_{hot, in}$
- `feat_t_hot_in_sq` = $T_{hot, in}^2$
- `feat_m_cold_sq` = $\dot{m}_{cold}^2$

---

## 🏆 9. Model Comparison & Results

Evaluated on untouched 2,000-sample test set:

| Model | MAE (kW) | RMSE (kW) | R² Score | 5-Fold CV R² | Status |
|---|---|---|---|---|---|
| **Random Forest (Selected)** | **0.0537** | **0.1144** | **1.0000** | **0.9999 ± 0.000** | **Production Best** |
| Extra Trees | 0.0612 | 0.1285 | 1.0000 | 0.9998 ± 0.000 | Candidate |
| CatBoost | 0.0984 | 0.1542 | 0.9999 | 0.9998 ± 0.000 | Candidate |
| XGBoost | 0.1205 | 0.1890 | 0.9999 | 0.9997 ± 0.001 | Candidate |
| LightGBM | 0.1420 | 0.2105 | 0.9998 | 0.9996 ± 0.001 | Candidate |
| HistGradientBoosting | 0.1550 | 0.2310 | 0.9998 | 0.9995 ± 0.001 | Candidate |
| Gradient Boosting | 0.2840 | 0.4120 | 0.9995 | 0.9992 ± 0.001 | Candidate |
| Ridge Regression | 2.1450 | 2.8540 | 0.9778 | 0.9772 ± 0.002 | Candidate |
| Linear Regression | 2.1450 | 2.8540 | 0.9778 | 0.9772 ± 0.002 | Candidate |
| Baseline (Dummy) | 16.4270 | 19.2430 | 0.0000 | -0.0001 ± 0.000 | Baseline |

---

## 📐 10. Evaluation Metrics

Calculated metrics:
- **MAE**: Mean Absolute Error ($kW$)
- **MSE**: Mean Squared Error ($kW^2$)
- **RMSE**: Root Mean Squared Error ($kW$)
- **R²**: Coefficient of Determination
- **MAPE**: Mean Absolute Percentage Error ($\%$)
- **Explained Variance**: Proportion of variance explained by model

---

## 🔍 11. Explainable AI (SHAP & Permutation)

- **Native Feature Importance**: Evaluates tree node split gain. Top drivers: `feat_thermal_interaction` and `hot_inlet_temperature_k`.
- **Local Predictions**: Natural language narrative generation explaining specific operating point predictions.

---

## ⚠️ 12. Anomaly Detection

- Unsupervised ML via **Isolation Forest** (contamination fraction configurable from 1% to 15%).
- Flags statistically unusual operating conditions without falsely claiming equipment failure.

---

## 🧪 13. What-If Simulation

Interactive scenario simulator allowing engineers to adjust inlet operating temperatures and flow rates to calculate baseline vs scenario heat load shifts, percentage change ($\Delta\%$), and physical effectiveness.

---

## 💻 14. Streamlit UI & Aesthetics

Designed as a **Premium Industrial AI Control Center**:
- Dark industrial metallic aesthetic (`#0E1117`, `#1E222D`).
- Responsive metric cards, prediction hero cards, and Plotly technical indicators.
- 13 Navigation pages with custom CSS.

---

## 📁 15. Project Architecture & Folder Structure

```
heat_exchanger_ai/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── config/
│   └── config.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   ├── best_model.joblib
│   ├── pipeline.joblib
│   └── model_metadata.json
│
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── train.py
│   ├── evaluate.py
│   ├── prediction.py
│   ├── anomaly_detection.py
│   ├── explainability.py
│   ├── engineering.py
│   └── utils.py
│
├── pages/
│   ├── dashboard.py
│   ├── data_explorer.py
│   ├── monitoring.py
│   ├── prediction.py
│   ├── model_performance.py
│   ├── explainable_ai.py
│   ├── anomaly.py
│   ├── simulator.py
│   ├── engineering.py
│   ├── training.py
│   ├── reports.py
│   ├── settings.py
│   └── about.py
│
├── components/
│   ├── cards.py
│   ├── charts.py
│   ├── sidebar.py
│   └── styles.py
│
├── assets/
│   └── images/
│       ├── heat_exchanger_hero.jpg
│       └── process_overview.jpg
│
└── tests/
    └── test_pipeline.py
```

---

## 🔧 16. Installation

```bash
git clone <repo-url>
cd heat_Exchanger
pip install -r requirements.txt
```

---

## ▶️ 17. Running the Application

```bash
streamlit run app.py
```

---

## 🧠 18. Training the Model

To train/retrain the models manually via command line:
```bash
python src/train.py
```

---

## 🧪 19. Running Unit Tests

```bash
python -m pytest
```

---

## ⚠️ 20. Limitations

- Data represents steady-state parametric sweeps.
- Surrogate predictions provide decision support and do not replace physical pressure relief valves or CFD simulations.

---

## 🔮 21. Future Improvements

- Integration with live OPC-UA plant data streams.
- Multi-exchanger network optimization.
