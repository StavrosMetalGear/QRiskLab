"""
Entry point for running the QRiskLab API server.

Starts the FastAPI application on 127.0.0.1:8000.
"""

import uvicorn
from qrisklab.api.main import app


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )