"""
QRiskLab App module

Provides Streamlit dashboard and interactive applications for visualization
and analysis of quantum and classical risk metrics.

Includes dashboard pages for option pricing, risk analysis, quantum algorithms,
and portfolio management.
"""

from qrisklab.app import dashboard, pages, utils

__all__ = ["dashboard", "pages", "utils"]
