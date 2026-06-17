"""
Risk analysis API endpoints.

Provides REST endpoints for Value at Risk (VaR) and Conditional Value at Risk (CVaR) calculations.
"""

from fastapi import APIRouter, HTTPException
import logging

from qrisklab.finance.risk import RiskAnalyzer
from qrisklab.api.models import (
    RiskAnalysisRequest,
    RiskMetricsResponse,
    MultiLevelRiskRequest,
    MultiLevelRiskResponse,
    ErrorResponse,
)
from qrisklab.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/risk", tags=["risk"])
analyzer = RiskAnalyzer()


@router.post(
    "/analyze",
    response_model=RiskMetricsResponse,
    responses={400: {"model": ErrorResponse}},
    summary="Analyze Risk Metrics",
    description="Calculate VaR and CVaR for portfolio losses",
)
async def analyze_risk(request: RiskAnalysisRequest) -> RiskMetricsResponse:
    """
    Analyze risk metrics for portfolio losses.

    Args:
        request: Risk analysis request with losses and confidence level

    Returns:
        RiskMetricsResponse with VaR, CVaR, and statistics

    Raises:
        HTTPException: If analysis fails
    """
    try:
        logger.info(
            f"Risk analysis: {len(request.losses)} losses, "
            f"confidence_level={request.confidence_level}"
        )

        result = analyzer.analyze_risk(
            losses=request.losses,
            confidence_level=request.confidence_level,
        )

        return RiskMetricsResponse(
            var=result.var,
            cvar=result.cvar,
            confidence_level=result.confidence_level,
            sample_count=result.sample_count,
            min_loss=result.min_loss,
            max_loss=result.max_loss,
            mean_loss=result.mean_loss,
            std_loss=result.std_loss,
        )

    except ValueError as e:
        logger.error(f"Risk analysis validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Risk analysis error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during risk analysis")


@router.post(
    "/var",
    response_model=float,
    responses={400: {"model": ErrorResponse}},
    summary="Calculate Value at Risk",
    description="Calculate Value at Risk (VaR) for portfolio losses",
)
async def calculate_var(request: RiskAnalysisRequest) -> float:
    """
    Calculate Value at Risk (VaR).

    Args:
        request: Risk analysis request

    Returns:
        Value at Risk at the specified confidence level

    Raises:
        HTTPException: If calculation fails
    """
    try:
        logger.info(f"VaR calculation: confidence_level={request.confidence_level}")

        var = analyzer.calculate_var(
            losses=request.losses,
            confidence_level=request.confidence_level,
        )

        return var

    except ValueError as e:
        logger.error(f"VaR calculation validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"VaR calculation error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during VaR calculation")


@router.post(
    "/cvar",
    response_model=float,
    responses={400: {"model": ErrorResponse}},
    summary="Calculate Conditional Value at Risk",
    description="Calculate Conditional Value at Risk (CVaR / Expected Shortfall)",
)
async def calculate_cvar(request: RiskAnalysisRequest) -> float:
    """
    Calculate Conditional Value at Risk (CVaR).

    Args:
        request: Risk analysis request

    Returns:
        Conditional Value at Risk at the specified confidence level

    Raises:
        HTTPException: If calculation fails
    """
    try:
        logger.info(f"CVaR calculation: confidence_level={request.confidence_level}")

        cvar = analyzer.calculate_cvar(
            losses=request.losses,
            confidence_level=request.confidence_level,
        )

        return cvar

    except ValueError as e:
        logger.error(f"CVaR calculation validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"CVaR calculation error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during CVaR calculation")


@router.post(
    "/multi-level",
    response_model=MultiLevelRiskResponse,
    responses={400: {"model": ErrorResponse}},
    summary="Multi-Level Risk Analysis",
    description="Analyze risk at multiple confidence levels",
)
async def multi_level_analysis(request: MultiLevelRiskRequest) -> MultiLevelRiskResponse:
    """
    Perform risk analysis at multiple confidence levels.

    Args:
        request: Multi-level risk analysis request

    Returns:
        MultiLevelRiskResponse with results at each confidence level

    Raises:
        HTTPException: If analysis fails
    """
    try:
        confidence_levels = request.confidence_levels or [0.90, 0.95, 0.99]
        logger.info(f"Multi-level risk analysis: {len(confidence_levels)} confidence levels")

        results_dict = analyzer.multi_level_analysis(
            losses=request.losses,
            confidence_levels=confidence_levels,
        )

        # Convert to response format
        response_results = {}
        for cl, result in results_dict.items():
            response_results[cl] = RiskMetricsResponse(
                var=result.var,
                cvar=result.cvar,
                confidence_level=result.confidence_level,
                sample_count=result.sample_count,
                min_loss=result.min_loss,
                max_loss=result.max_loss,
                mean_loss=result.mean_loss,
                std_loss=result.std_loss,
            )

        return MultiLevelRiskResponse(results=response_results)

    except ValueError as e:
        logger.error(f"Multi-level analysis validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Multi-level analysis error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during multi-level analysis")


__all__ = ["router"]
