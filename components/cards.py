import streamlit as st

def metric_card(title: str, value: str, subtitle: str = "", border_color: str = ""):
    """
    Renders a styled industrial metric card with glassmorphism and left gradient border accent.
    """
    style = f"border-color: {border_color};" if border_color else ""
    val_color = f"color: {border_color}; text-shadow: 0 0 12px {border_color};" if border_color else ""
    
    html = f"""
    <div class="metric-card" style="{style}">
        <div class="metric-title">{title}</div>
        <div class="metric-value" style="{val_color}">{value}</div>
        {'<div class="metric-subtitle">' + subtitle + '</div>' if subtitle else ''}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def prediction_card(title: str, value: str, unit: str = "kW", subtitle: str = ""):
    """
    Renders a prominent glowing hero prediction output card.
    """
    html = f"""
    <div class="prediction-card">
        <div class="prediction-title">{title}</div>
        <div class="prediction-value">{value} <span style="font-size: 1.8rem; font-weight: 600; color: #00F2FE;">{unit}</span></div>
        <div style="font-size: 0.95rem; color: #94A3B8; font-weight: 500;">{subtitle}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def status_badge(status_text: str, level: str = "success"):
    """
    Renders a status badge pill. Level options: 'success', 'warning', 'danger'.
    """
    html = f'<span class="status-badge status-badge-{level}">{status_text}</span>'
    st.markdown(html, unsafe_allow_html=True)

def section_header(title: str, icon: str = "⚙️", description: str = ""):
    """
    Renders a standard section header with icon and subtle description.
    """
    st.markdown(
        f"""
        <div style="margin: 15px 0 10px 0;">
            <h2 style="font-family: 'Outfit', sans-serif; font-size: 1.5rem; font-weight: 700; color: #F8FAFC; margin: 0; display: flex; align-items: center; gap: 8px;">
                <span>{icon}</span> <span>{title}</span>
            </h2>
            {f'<p style="color: #64748B; font-size: 0.92rem; margin: 2px 0 0 0;">' + description + '</p>' if description else ''}
        </div>
        """,
        unsafe_allow_html=True
    )

def warning_card(title: str, message: str):
    """
    Renders an engineering warning card with amber neon left accent.
    """
    html = f"""
    <div style="background: linear-gradient(135deg, rgba(255, 183, 3, 0.08) 0%, rgba(255, 183, 3, 0.03) 100%); border-left: 4px solid #FFB703; border-radius: 12px; padding: 18px 20px; margin: 12px 0; border-top: 1px solid rgba(255, 183, 3, 0.2); border-right: 1px solid rgba(255, 183, 3, 0.2); border-bottom: 1px solid rgba(255, 183, 3, 0.2);">
        <strong style="color: #FFB703; font-family: 'Outfit', sans-serif; font-size: 1.05rem; font-weight: 700;">⚠️ {title}</strong>
        <div style="color: #CBD5E1; font-size: 0.95rem; margin-top: 6px; line-height: 1.5;">{message}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def info_card(title: str, message: str):
    """
    Renders an informative engineering note card with cyan neon left accent.
    """
    html = f"""
    <div style="background: linear-gradient(135deg, rgba(0, 242, 254, 0.08) 0%, rgba(79, 172, 254, 0.03) 100%); border-left: 4px solid #00F2FE; border-radius: 12px; padding: 18px 20px; margin: 12px 0; border-top: 1px solid rgba(0, 242, 254, 0.2); border-right: 1px solid rgba(0, 242, 254, 0.2); border-bottom: 1px solid rgba(0, 242, 254, 0.2);">
        <strong style="color: #00F2FE; font-family: 'Outfit', sans-serif; font-size: 1.05rem; font-weight: 700;">ℹ️ {title}</strong>
        <div style="color: #CBD5E1; font-size: 0.95rem; margin-top: 6px; line-height: 1.5;">{message}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
