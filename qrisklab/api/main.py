"""
FastAPI application for QRiskLab.

Provides REST API for quantum and classical risk analysis with automatic
documentation, error handling, and CORS support.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from qrisklab import __version__
from qrisklab.api.models import HealthResponse, ErrorResponse
from qrisklab.api.routes import pricing, risk, quantum
from qrisklab.utils.logger import get_logger, setup_logging
from qrisklab.config import config

logger = get_logger(__name__)


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    # Setup logging
    setup_logging(
        level=config.LOG_LEVEL,
        log_file=config.LOG_FILE,
        console_output=True,
    )

    # Create FastAPI app
    app = FastAPI(
        title="QRiskLab Pro API",
        description="Hybrid Quantum-Classical Risk Analysis Framework",
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add error handling middleware
    @app.middleware("http")
    async def error_handling_middleware(request: Request, call_next):
        """Middleware for global error handling."""
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Unhandled exception: {e}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={
                    "error": "InternalServerError",
                    "message": "An unexpected error occurred",
                },
            )

    # Health check endpoint
    @app.get(
        "/health",
        response_model=HealthResponse,
        summary="Health Check",
        description="Check API health status",
    )
    async def health_check() -> HealthResponse:
        """
        Health check endpoint.

        Returns:
            HealthResponse with service status
        """
        return HealthResponse(
            status="healthy",
            version=__version__,
            message="QRiskLab API is running",
        )

    # Root endpoint
    @app.get(
        "/",
        summary="API Root",
        description="QRiskLab API root endpoint",
    )
    async def root():
        """Root endpoint with API information."""
        return {
            "name": "QRiskLab Pro API",
            "version": __version__,
            "description": "Hybrid Quantum-Classical Risk Analysis Framework",
            "docs": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json",
        }

    # Include routers
    app.include_router(pricing.router)
    app.include_router(risk.router)
    app.include_router(quantum.router)

    logger.info(f"FastAPI application created (version {__version__})")

    return app


# Create application instance
app = create_app()


__all__ = ["app", "create_app"]
