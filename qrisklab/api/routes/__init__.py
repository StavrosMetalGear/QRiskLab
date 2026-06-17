"""
QRiskLab API routes package.

Provides REST API endpoints for pricing, risk analysis, and quantum algorithms.
"""

from qrisklab.api.routes import pricing, risk, quantum

__all__ = ["pricing", "risk", "quantum"]
