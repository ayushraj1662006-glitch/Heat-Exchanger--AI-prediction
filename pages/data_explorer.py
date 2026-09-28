import streamlit as st
import pandas as pd
import plotly.express as px

from config.config import DATASET_PATH
from src.data_loader import load_dataset, validate_dataset
from components.cards import section_header, metric_card

def render_page(is_noisy: bool):
    st.title("📊 Data Explorer")
    st.markdown("<p style='color: #8892B0;'>Exploratory data analysis, distributions, correlations, and dataset diagnostics.</p>", unsafe_allow_html=True)
    
    try:
        df = load_dataset(DATASET_PATH)
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return
        
    val_report = validate_dataset(df)
    
    # Overview Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Total Rows", f"{val_report['rows']:,}")
    with c2:
        metric_card("Total Columns", f"{val_report['cols']}")
    with c3:
        metric_card("Missing Values", f"{val_report['total_missing']}")
    with c4:
        metric_card("Duplicates", f"{val_report['duplicate_rows']}")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Dataset Preview & Descriptive Statistics
    tab_data, tab_stats, tab_plots, tab_corr = st.tabs(["📋 Raw Dataset Preview", "📈 Descriptive Statistics", "🎨 Interactive Plots", "🔥 Correlation Heatmap"])
    
    with tab_data:
        st.markdown("### Dataset Preview")
        rows_to_show = st.slider("Select number of rows to display", 5, 500, 20)
        st.dataframe(df.head(rows_to_show), use_container_width=True)
        
    with tab_stats:
        st.markdown("### Summary Statistics")
        st.dataframe(df.describe().T.style.format("{:.3f}"), use_container_width=True)
        
    with tab_plots:
        st.markdown("### Feature Distribution & Scatter Analysis")
        col_x, col_y, col_type = st.columns(3)
        num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        
        with col_x:
            var_x = st.selectbox("Select X Axis Variable", num_cols, index=0)
        with col_y:
            var_y = st.selectbox("Select Y Axis Variable", num_cols, index=4 if len(num_cols)>4 else 1)
        with col_type:
            chart_type = st.selectbox("Chart Type", ["Scatter Plot", "Histogram / Distribution", "Box Plot"])
            
        if chart_type == "Scatter Plot":
            fig = px.scatter(df, x=var_x, y=var_y, color=var_y, title=f"{var_y} vs {var_x}", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        elif chart_type == "Histogram / Distribution":
            fig = px.histogram(df, x=var_x, marginal="box", title=f"Distribution of {var_x}", template="plotly_dark", color_discrete_sequence=["#00D2FF"])
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig = px.box(df, y=var_x, title=f"Boxplot of {var_x}", template="plotly_dark", color_discrete_sequence=["#3A7BD5"])
            st.plotly_chart(fig, use_container_width=True)
            
    with tab_corr:
        st.markdown("### Correlation Matrix Heatmap")
        corr = df.corr()
        fig_corr = px.imshow(
            corr,
            text_auto=".2f",
            aspect="auto",
            title="Full Correlation Heatmap",
            color_continuous_scale="RdBu_r",
            template="plotly_dark"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
