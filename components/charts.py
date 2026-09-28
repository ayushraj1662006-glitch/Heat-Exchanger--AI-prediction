import plotly.express as px
import plotly.graph_objects as gg
import pandas as pd
import numpy as np

DARK_TEMPLATE = "plotly_dark"
COLOR_PRIMARY = "#00F2FE"
COLOR_SECONDARY = "#4FACFE"
COLOR_ACCENT = "#00F5A0"
COLOR_WARN = "#FFB703"

def _apply_custom_chart_layout(fig: gg.Figure, title: str = "") -> gg.Figure:
    """
    Applies consistent cyberpunk dark engineering aesthetic to Plotly figures.
    """
    fig.update_layout(
        template=DARK_TEMPLATE,
        paper_bgcolor="rgba(15, 23, 42, 0.6)",
        plot_bgcolor="rgba(15, 23, 42, 0.6)",
        font=dict(family="Outfit, sans-serif", color="#CBD5E1", size=13),
        title=dict(
            text=title,
            font=dict(family="Outfit, sans-serif", size=17, color="#F8FAFC", weight=700)
        ) if title else None,
        xaxis=dict(gridcolor="rgba(255, 255, 255, 0.08)", zerolinecolor="rgba(255, 255, 255, 0.15)"),
        yaxis=dict(gridcolor="rgba(255, 255, 255, 0.08)", zerolinecolor="rgba(255, 255, 255, 0.15)"),
        margin=dict(l=25, r=25, t=50, b=30)
    )
    return fig

def plot_actual_vs_predicted(df_res: pd.DataFrame) -> gg.Figure:
    """
    Renders actual vs predicted scatter plot with 45-degree reference line.
    """
    fig = px.scatter(
        df_res,
        x="Actual",
        y="Predicted",
        hover_data=["Residual"],
        color_discrete_sequence=[COLOR_PRIMARY]
    )
    
    min_val = min(df_res["Actual"].min(), df_res["Predicted"].min())
    max_val = max(df_res["Actual"].max(), df_res["Predicted"].max())
    
    fig.add_trace(
        gg.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode="lines",
            name="Ideal Prediction (1:1)",
            line=dict(color=COLOR_WARN, dash="dash", width=2)
        )
    )
    
    fig.update_layout(xaxis_title="Actual Heat Load (kW)", yaxis_title="Predicted Heat Load (kW)")
    return _apply_custom_chart_layout(fig, "Actual vs Predicted Heat Duty (kW)")

def plot_residuals(df_res: pd.DataFrame) -> gg.Figure:
    """
    Renders Residuals vs Predicted plot.
    """
    fig = px.scatter(
        df_res,
        x="Predicted",
        y="Residual",
        color_discrete_sequence=["#EF476F"]
    )
    
    fig.add_hline(y=0, line_dash="dash", line_color=COLOR_ACCENT, annotation_text="Zero Error Line")
    fig.update_layout(xaxis_title="Predicted Heat Load (kW)", yaxis_title="Residual Error (kW)")
    return _apply_custom_chart_layout(fig, "Residual Errors (Actual - Predicted) vs Predicted Heat Load")

def plot_feature_importance(df_imp: pd.DataFrame, top_n: int = 10) -> gg.Figure:
    """
    Renders horizontal bar chart of feature importances.
    """
    df_top = df_imp.head(top_n).sort_values(by="Importance", ascending=True)
    
    fig = px.bar(
        df_top,
        x="Importance",
        y="Feature",
        orientation="h",
        color="Importance",
        color_continuous_scale=["#103260", "#00F2FE", "#00F5A0"]
    )
    return _apply_custom_chart_layout(fig, f"Top {top_n} Predictive Feature Importances")

def plot_gauge_chart(value: float, min_val: float, max_val: float, title: str, unit: str = "") -> gg.Figure:
    """
    Renders Plotly industrial indicator gauge chart with neon styling.
    """
    fig = gg.Figure(gg.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 15, 'color': '#E2E8F0', 'family': 'Outfit'}},
        number={'suffix': f" {unit}", 'font': {'color': '#00F2FE', 'size': 26, 'family': 'Outfit'}},
        gauge={
            'axis': {'range': [min_val, max_val], 'tickwidth': 1, 'tickcolor': "#475569"},
            'bar': {'color': COLOR_PRIMARY, 'thickness': 0.3},
            'bgcolor': "rgba(15, 23, 42, 0.8)",
            'borderwidth': 1,
            'bordercolor': "#334155",
            'steps': [
                {'range': [min_val, min_val + (max_val - min_val) * 0.6], 'color': 'rgba(0, 245, 160, 0.15)'},
                {'range': [min_val + (max_val - min_val) * 0.6, min_val + (max_val - min_val) * 0.85], 'color': 'rgba(255, 183, 3, 0.15)'},
                {'range': [min_val + (max_val - min_val) * 0.85, max_val], 'color': 'rgba(239, 71, 111, 0.15)'}
            ]
        }
    ))
    fig.update_layout(
        template=DARK_TEMPLATE,
        paper_bgcolor="rgba(15, 23, 42, 0.6)",
        font=dict(family="Outfit, sans-serif"),
        height=220,
        margin=dict(l=25, r=25, t=45, b=25)
    )
    return fig

def plot_model_comparison_bar(df_metrics: pd.DataFrame, metric_col: str = "R2") -> gg.Figure:
    """
    Renders model comparison bar chart sorted by selected metric.
    """
    df_sorted = df_metrics.sort_values(by=metric_col, ascending=(metric_col in ["MAE", "RMSE", "MSE"]))
    
    fig = px.bar(
        df_sorted,
        x="Model",
        y=metric_col,
        color=metric_col,
        color_continuous_scale=["#0F172A", "#00F2FE", "#00F5A0"]
    )
    fig.update_layout(xaxis_tickangle=-45)
    return _apply_custom_chart_layout(fig, f"Model Benchmark Comparison by {metric_col}")

def plot_what_if_comparison(baseline_val: float, scenario_val: float, unit: str = "kW") -> gg.Figure:
    """
    Renders side-by-side comparison bar chart for What-If simulator.
    """
    df_comp = pd.DataFrame({
        "Condition": ["Baseline Prediction", "Modified Scenario"],
        "Predicted Heat Load": [baseline_val, scenario_val]
    })
    
    fig = px.bar(
        df_comp,
        x="Condition",
        y="Predicted Heat Load",
        text_auto=".2f",
        color="Condition",
        color_discrete_map={"Baseline Prediction": "#4FACFE", "Modified Scenario": "#00F2FE"}
    )
    return _apply_custom_chart_layout(fig, f"Scenario Heat Duty Comparison ({unit})")
