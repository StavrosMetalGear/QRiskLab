"""
Pricing API endpoints.

Provides REST endpoints for European call option pricing with Monte Carlo simulation.
"""

from fastapi import APIRouter, HTTPException
from typing import List
import logging

from qrisklab.finance.pricing import EuropeanCallPricer
from qrisklab.api.models import (
    EuropeanCallRequest,
    OptionPricingResponse,
    BatchPricingRequest,
    BatchPricingResponse,
    SensitivityRequest,
    SensitivityResponse,
    ErrorResponse,
)
from qrisklab.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/pricing", tags=["pricing"])
pricer = EuropeanCallPricer()


@router.post(
    "/european-call",
    response_model=OptionPricingResponse,
    responses={400: {"model": ErrorResponse}},
    summary="Price European Call Option",
    description="Price a European call option using Monte Carlo simulation",
)
async def price_european_call(request: EuropeanCallRequest) -> OptionPricingResponse:
    """
    Price a European call option.

    Args:
        request: Pricing parameters

    Returns:
        OptionPricingResponse with estimated price and standard error

    Raises:
        HTTPException: If pricing fails
    """
    try:
        logger.info(f"Pricing European call: S={request.spot_price}, K={request.strike_price}")

        result = pricer.price(
            spot_price=request.spot_price,
            strike_price=request.strike_price,
            risk_free_rate=request.risk_free_rate,
            volatility=request.volatility,
            maturity_years=request.maturity_years,
            paths=request.paths,
            seed=request.seed,
        )

        return OptionPricingResponse(
            estimated_price=result.estimated_price,
            standard_error=result.standard_error,
            paths=request.paths,
            spot_price=request.spot_price,
            strike_price=request.strike_price,
        )

    except ValueError as e:
        logger.error(f"Pricing validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Pricing error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during pricing")


@router.post(
    "/batch",
    response_model=BatchPricingResponse,
    responses={400: {"model": ErrorResponse}},
    summary="Batch Price Options",
    description="Price multiple European call options",
)
async def batch_price(request: BatchPricingRequest) -> BatchPricingResponse:
    """
    Price multiple European call options.

    Args:
        request: Batch pricing request with list of options

    Returns:
        BatchPricingResponse with all pricing results

    Raises:
        HTTPException: If batch pricing fails
    """
    try:
        logger.info(f"Batch pricing {len(request.options)} options")

        results = []
        for option in request.options:
            result = pricer.price(
                spot_price=option.spot_price,
                strike_price=option.strike_price,
                risk_free_rate=option.risk_free_rate,
                volatility=option.volatility,
                maturity_years=option.maturity_years,
                paths=option.paths,
                seed=option.seed,
            )

            results.append(
                OptionPricingResponse(
                    estimated_price=result.estimated_price,
                    standard_error=result.standard_error,
                    paths=option.paths,
                    spot_price=option.spot_price,
                    strike_price=option.strike_price,
                )
            )

        return BatchPricingResponse(results=results, total_options=len(results))

    except ValueError as e:
        logger.error(f"Batch pricing validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Batch pricing error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during batch pricing")


@router.post(
    "/sensitivity",
    response_model=SensitivityResponse,
    responses={400: {"model": ErrorResponse}},
    summary="Sensitivity Analysis",
    description="Perform sensitivity analysis on option pricing",
)
async def sensitivity_analysis(request: SensitivityRequest) -> SensitivityResponse:
    """
    Perform sensitivity analysis on option pricing.

    Args:
        request: Sensitivity analysis parameters

    Returns:
        SensitivityResponse with parameter values and corresponding prices

    Raises:
        HTTPException: If analysis fails
    """
    try:
        logger.info(f"Sensitivity analysis for parameter: {request.parameter}")

        sensitivity_results = pricer.sensitivity_analysis(
            spot_price=request.spot_price,
            strike_price=request.strike_price,
            risk_free_rate=request.risk_free_rate,
            volatility=request.volatility,
            maturity_years=request.maturity_years,
            parameter=request.parameter,
            range_pct=request.range_pct,
            steps=request.steps,
        )

        # Calculate base price
        base_result = pricer.price(
            spot_price=request.spot_price,
            strike_price=request.strike_price,
            risk_free_rate=request.risk_free_rate,
            volatility=request.volatility,
            maturity_years=request.maturity_years,
        )

        return SensitivityResponse(
            parameter=request.parameter,
            results=sensitivity_results,
            base_price=base_result.estimated_price,
        )

    except ValueError as e:
        logger.error(f"Sensitivity analysis validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Sensitivity analysis error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during sensitivity analysis")


__all__ = ["router"]
