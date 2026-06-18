"""
QRiskLab Streamlit Dashboard

Main dashboard application for quantum and classical risk analysis.
Provides interactive interface for option pricing, risk metrics, quantum algorithms,
and portfolio management.
"""

import streamlit as st
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="QRiskLab Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    """Main dashboard application."""
    st.title("🚀 QRiskLab Pro")
    st.markdown("### Hybrid Quantum-Classical Risk Analysis Framework")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select a page:",
        [
            "Home",
            "Option Pricing",
            "Risk Analysis",
            "Quantum Algorithms",
            "Portfolio Management",
        ],
    )
    
    # Display selected page
    if page == "Home":
        show_home()
    elif page == "Option Pricing":
        from qrisklab.app.pages import pricing
        pricing.show()
    elif page == "Risk Analysis":
        from qrisklab.app.pages import risk_analysis
        risk_analysis.show()
    elif page == "Quantum Algorithms":
        from qrisklab.app.pages import quantum
        quantum.show()
    elif page == "Portfolio Management":
        from qrisklab.app.pages import portfolio
        portfolio.show()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "**QRiskLab Pro v0.1.0**\n\n"
        "Quantum-Classical Risk Analysis\n\n"
        "[Documentation](https://github.com/qrisklab/qrisklab) | "
        "[GitHub](https://github.com/qrisklab/qrisklab)"
    )


def show_home():
    """Display home page."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Welcome to QRiskLab Pro")
        st.markdown("""
        QRiskLab Pro is a hybrid quantum-classical framework for financial risk analysis.
        
        **Features:**
        - 📈 European Call Option Pricing (Monte Carlo)
        - 📊 Value at Risk (VaR) & Conditional VaR (CVaR)
        - 🔬 Quantum Algorithms (Amplitude Estimation, VQE, QPE)
        - 💼 Portfolio Risk Management
        - 🎯 Multi-backend Quantum Support
        
        **Get Started:**
        1. Select a page from the sidebar
        2. Input your parameters
        3. View results and visualizations
        """)
    
    with col2:
        st.info("""
        ### Quick Links
        
        **Pricing Module**
        - Price European call options
        - Sensitivity analysis
        - Batch pricing
        
        **Risk Module**
        - Calculate VaR and CVaR
        - Multi-level analysis
        - Risk reporting
        
        **Quantum Module**
        - Run quantum algorithms
        - Select quantum backend
        - View quantum results
        
        **Portfolio Module**
        - Build portfolios
        - Analyze risk metrics
        - Optimize positions
        """)
    
    st.markdown("---")
    st.subheader("System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        from qrisklab.core import QuantumState
        col1.metric("C++ Bindings", "✅ Ready", "QuantumState")
    except ImportError:
        col1.metric("C++ Bindings", "❌ Not Available", "Install with: pip install -e .")
    
    try:
        from qrisklab.finance import EuropeanCallPricer
        col2.metric("Finance Module", "✅ Ready", "Pricing & Risk")
    except ImportError:
        col2.metric("Finance Module", "❌ Not Available", "")
    
    try:
        from qrisklab.quantum import QuantumStateWrapper
        col3.metric("Quantum Module", "✅ Ready", "Algorithms")
    except ImportError:
        col3.metric("Quantum Module", "❌ Not Available", "")
    
    try:
        from qrisklab.api import app
        col4.metric("API Backend", "✅ Ready", "FastAPI")
    except ImportError:
        col4.metric("API Backend", "❌ Not Available", "")


if __name__ == "__main__":
    main()
