"""
European call option pricing module.

Provides high-level interface for option pricing with input validation,
result formatting, and sensitivity analysis.
"""

from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
import logging

from qrisklab.finance._qrisklab_core import MonteCarlo, OptionPricingResult
from qrisklab.utils.logger import get_logger
from qrisklab.utils.timing import timer, timed_block

logger = get_logger(__name__)


@dataclass
class PricingParameters:
    """Parameters for European call option pricing."""
    spot_price: float
    strike_price: float
    risk_free_rate: float
    volatility: float
    maturity_years: float
    paths: int = 10000
    seed: int = 42

    def validate(self) -> None:
        """Validate pricing parameters."""
        if self.spot_price <= 0:
            raise ValueError("Spot price must be positive")
        if self.strike_price <= 0:
            raise ValueError("Strike price must be positive")
        if self.risk_free_rate < 0:
            raise ValueError("Risk-free rate cannot be negative")
        if self.volatility <= 0:
            raise ValueError("Volatility must be positive")
        if self.maturity_years <= 0:
            raise ValueError("Maturity must be positive")
        if self.paths < 100:
            raise ValueError("Number of paths must be at least 100")


class EuropeanCallPricer:
    """
    High-level interface for European call option pricing.

    Wraps C++ MonteCarlo implementation with validation, caching, and
    sensitivity analysis capabilities.
    """

    def __init__(self, default_paths: int = 10000, default_seed: int = 42):
        """
        Initialize the pricer.

        Args:
            default_paths: Default number of Monte Carlo paths
            default_seed: Default random seed for reproducibility
        """
        self.default_paths = default_paths
        self.default_seed = default_seed
        self._cache: Dict[str, OptionPricingResult] = {}
        logger.debug(
            f"EuropeanCallPricer initialized with paths={default_paths}, seed={default_seed}"
        )

    def _cache_key(self, params: PricingParameters) -> str:
        """Generate cache key from parameters."""
        return (
            f"{params.spot_price}_{params.strike_price}_{params.risk_free_rate}_"
            f"{params.volatility}_{params.maturity_years}_{params.paths}_{params.seed}"
        )

    @timer
    def price(
        self,
        spot_price: float,
        strike_price: float,
        risk_free_rate: float,
        volatility: float,
        maturity_years: float,
        paths: Optional[int] = None,
        seed: Optional[int] = None,
        use_cache: bool = True,
    ) -> OptionPricingResult:
        """
        Price a European call option.

        Args:
            spot_price: Current stock price
            strike_price: Option strike price
            risk_free_rate: Risk-free interest rate
            volatility: Stock volatility (annualized)
            maturity_years: Time to maturity in years
            paths: Number of Monte Carlo paths (uses default if None)
            seed: Random seed (uses default if None)
            use_cache: Whether to use cached results

        Returns:
            OptionPricingResult with price and Greeks

        Raises:
            ValueError: If parameters are invalid
        """
        paths = paths or self.default_paths
        seed = seed or self.default_seed

        params = PricingParameters(
            spot_price=spot_price,
            strike_price=strike_price,
            risk_free_rate=risk_free_rate,
            volatility=volatility,
            maturity_years=maturity_years,
            paths=paths,
            seed=seed,
        )
        params.validate()

        # Check cache
        cache_key = self._cache_key(params)
        if use_cache and cache_key in self._cache:
            logger.debug(f"Cache hit for option pricing: {cache_key}")
            return self._cache[cache_key]

        # Call C++ implementation
        with timed_block("European call option pricing"):
            result = MonteCarlo.price_european_call(
                spot_price=params.spot_price,
                strike_price=params.strike_price,
                risk_free_rate=params.risk_free_rate,
                volatility=params.volatility,
                maturity_years=params.maturity_years,
                paths=params.paths,
                seed=params.seed,
            )

        # Cache result
        self._cache[cache_key] = result
        logger.info(
            f"Priced European call: S={spot_price}, K={strike_price}, "
            f"Price={result.price:.4f}"
        )

        return result

    def price_batch(
        self,
        parameters_list: List[Tuple[float, float, float, float, float]],
        paths: Optional[int] = None,
        seed: Optional[int] = None,
    ) -> List[OptionPricingResult]:
        """
        Price multiple European call options.

        Args:
            parameters_list: List of (S, K, r, σ, T) tuples
            paths: Number of Monte Carlo paths
            seed: Random seed

        Returns:
            List of OptionPricingResult objects
        """
        results = []
        for spot, strike, rate, vol, maturity in parameters_list:
            result = self.price(
                spot_price=spot,
                strike_price=strike,
                risk_free_rate=rate,
                volatility=vol,
                maturity_years=maturity,
                paths=paths,
                seed=seed,
            )
            results.append(result)
        logger.info(f"Batch priced {len(results)} options")
        return results

    def sensitivity_analysis(
        self,
        spot_price: float,
        strike_price: float,
        risk_free_rate: float,
        volatility: float,
        maturity_years: float,
        parameter: str = "spot_price",
        range_pct: float = 0.2,
        steps: int = 5,
    ) -> Dict[float, float]:
        """
        Perform sensitivity analysis on a parameter.

        Args:
            spot_price: Current stock price
            strike_price: Option strike price
            risk_free_rate: Risk-free interest rate
            volatility: Stock volatility
            maturity_years: Time to maturity
            parameter: Parameter to vary ('spot_price', 'volatility', 'risk_free_rate')
            range_pct: Range as percentage (e.g., 0.2 for ±20%)
            steps: Number of steps in the range

        Returns:
            Dictionary mapping parameter values to option prices
        """
        if parameter not in ["spot_price", "volatility", "risk_free_rate"]:
            raise ValueError(f"Unknown parameter: {parameter}")

        results = {}
        base_value = locals()[parameter]
        delta = base_value * range_pct / (steps - 1)

        for i in range(steps):
            factor = -range_pct / 2 + (i * delta / base_value)
            test_value = base_value * (1 + factor)

            params = {
                "spot_price": spot_price,
                "strike_price": strike_price,
                "risk_free_rate": risk_free_rate,
                "volatility": volatility,
                "maturity_years": maturity_years,
            }
            params[parameter] = test_value

            result = self.price(**params, use_cache=False)
            results[test_value] = result.price

        logger.info(
            f"Sensitivity analysis complete for {parameter}: "
            f"{len(results)} points"
        )
        return results

    def clear_cache(self) -> None:
        """Clear the pricing cache."""
        self._cache.clear()
        logger.debug("Pricing cache cleared")


__all__ = [
    "EuropeanCallPricer",
    "PricingParameters",
]
