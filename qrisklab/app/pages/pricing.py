"""
Option Pricing Page

Provides an interface for European call option pricing using Monte Carlo
simulation.
"""

import pandas as pd
import streamlit as st

from qrisklab.finance.pricing import EuropeanCallPricer
from qrisklab.utils.logger import get_logger


logger = get_logger(__name__)


def show():
    """Display the option pricing page."""
    st.header("European Call Option Pricing")
    st.markdown("Price European call options using Monte Carlo simulation.")

    tab1, tab2, tab3 = st.tabs(
        ["Single Option", "Batch Pricing", "Sensitivity Analysis"]
    )

    with tab1:
        show_single_pricing()

    with tab2:
        show_batch_pricing()

    with tab3:
        show_sensitivity_analysis()


def show_single_pricing():
    """Display the single-option pricing interface."""
    st.subheader("Price Single Option")

    col1, col2 = st.columns(2)

    with col1:
        spot_price = st.number_input(
            "Spot Price (S)",
            min_value=1.0,
            value=100.0,
            step=1.0,
            help="Current stock price",
        )

        strike_price = st.number_input(
            "Strike Price (K)",
            min_value=1.0,
            value=105.0,
            step=1.0,
            help="Option strike price",
        )

        risk_free_rate = st.slider(
            "Risk-Free Rate (r)",
            min_value=0.0,
            max_value=0.2,
            value=0.05,
            step=0.01,
            help="Annual risk-free interest rate",
        )

    with col2:
        volatility = st.slider(
            "Volatility (sigma)",
            min_value=0.01,
            max_value=1.00,
            value=0.20,
            step=0.01,
            help="Annualized volatility",
        )

        maturity_years = st.number_input(
            "Maturity (T)",
            min_value=0.01,
            value=1.0,
            step=0.1,
            help="Time to maturity in years",
        )

        seed = st.number_input(
            "Random Seed",
            min_value=0,
            value=42,
            step=1,
            help="Random seed for the Monte Carlo simulation",
        )

        paths = st.number_input(
            "Monte Carlo Paths",
            min_value=100,
            value=10000,
            step=1000,
            help="Number of simulation paths",
        )

    if st.button("Calculate Price", key="single_price"):
        try:
            paths_value = int(paths)
            seed_value = int(seed)

            pricer = EuropeanCallPricer(
                default_paths=paths_value,
                default_seed=seed_value,
            )

            result = pricer.price(
                spot_price=spot_price,
                strike_price=strike_price,
                risk_free_rate=risk_free_rate,
                volatility=volatility,
                maturity_years=maturity_years,
                paths=paths_value,
                seed=seed_value,
            )

            result_col1, result_col2, result_col3 = st.columns(3)

            result_col1.metric(
                "Option Price",
                f"${result.estimated_price:.4f}",
            )
            result_col2.metric(
                "Standard Error",
                f"${result.standard_error:.6f}",
            )
            result_col3.metric(
                "Paths",
                f"{paths_value:,}",
            )

            st.subheader("Input Parameters")

            params_df = pd.DataFrame(
                {
                    "Parameter": [
                        "Spot Price",
                        "Strike Price",
                        "Risk-Free Rate",
                        "Volatility",
                        "Maturity",
                        "Random Seed",
                    ],
                    "Value": [
                        f"${spot_price:.2f}",
                        f"${strike_price:.2f}",
                        f"{risk_free_rate:.2%}",
                        f"{volatility:.2%}",
                        f"{maturity_years:.2f} years",
                        str(seed_value),
                    ],
                }
            )

            st.dataframe(
                params_df,
                use_container_width=True,
                hide_index=True,
            )

            discounted_payoffs = list(result.discounted_payoffs)

            if discounted_payoffs:
                payoffs_series = pd.Series(
                    discounted_payoffs,
                    name="Discounted Payoff",
                    dtype=float,
                )

                confidence_lower = (
                    result.estimated_price
                    - 1.96 * result.standard_error
                )
                confidence_upper = (
                    result.estimated_price
                    + 1.96 * result.standard_error
                )

                st.subheader("Payoff Statistics")

                stat_col1, stat_col2, stat_col3 = st.columns(3)

                stat_col1.metric(
                    "Mean Payoff",
                    f"${payoffs_series.mean():.4f}",
                )
                stat_col2.metric(
                    "Minimum Payoff",
                    f"${payoffs_series.min():.4f}",
                )
                stat_col3.metric(
                    "Maximum Payoff",
                    f"${payoffs_series.max():.4f}",
                )

                st.metric(
                    "95% Confidence Interval",
                    (
                        f"${confidence_lower:.4f} "
                        f"to ${confidence_upper:.4f}"
                    ),
                )

                st.subheader("Payoff Distribution")

                unique_payoffs = payoffs_series.nunique()

                if unique_payoffs > 1:
                    bin_count = min(20, unique_payoffs)

                    payoff_bins = pd.cut(
                        payoffs_series,
                        bins=bin_count,
                        include_lowest=True,
                        duplicates="drop",
                    )

                    distribution = (
                        payoff_bins.value_counts(sort=False)
                        .rename("Frequency")
                    )

                    distribution.index = distribution.index.astype(str)

                    st.bar_chart(distribution)
                else:
                    st.info(
                        "All simulated discounted payoffs have the same value."
                    )
            else:
                st.info("No discounted payoff data was returned.")

            logger.info(
                "Priced option: S=%s, K=%s, Price=%.4f",
                spot_price,
                strike_price,
                result.estimated_price,
            )

        except ValueError as error:
            st.error(f"Invalid pricing input: {error}")
            logger.warning("Invalid pricing input: %s", error)

        except Exception as error:
            st.error(f"Error calculating price: {error}")
            logger.exception("Pricing error")


def show_batch_pricing():
    """Display the batch-pricing interface."""
    st.subheader("Batch Pricing")
    st.markdown("Upload or enter multiple options to price.")

    input_method = st.radio(
        "Input method:",
        ["Manual Entry", "CSV Upload"],
    )

    if input_method == "Manual Entry":
        st.markdown("Enter option parameters below:")

        num_options = st.number_input(
            "Number of options",
            min_value=1,
            max_value=10,
            value=2,
            step=1,
        )

        options_data = []

        for index in range(int(num_options)):
            with st.expander(f"Option {index + 1}"):
                col1, col2 = st.columns(2)

                with col1:
                    spot = st.number_input(
                        f"Spot Price {index + 1}",
                        min_value=1.0,
                        value=100.0,
                        step=1.0,
                        key=f"s_{index}",
                    )

                    strike = st.number_input(
                        f"Strike Price {index + 1}",
                        min_value=1.0,
                        value=105.0,
                        step=1.0,
                        key=f"k_{index}",
                    )

                    rate = st.slider(
                        f"Rate {index + 1}",
                        min_value=0.0,
                        max_value=0.2,
                        value=0.05,
                        step=0.01,
                        key=f"r_{index}",
                    )

                with col2:
                    volatility = st.slider(
                        f"Volatility {index + 1}",
                        min_value=0.01,
                        max_value=1.0,
                        value=0.2,
                        step=0.01,
                        key=f"v_{index}",
                    )

                    maturity = st.number_input(
                        f"Maturity {index + 1}",
                        min_value=0.01,
                        max_value=10.0,
                        value=1.0,
                        step=0.1,
                        key=f"t_{index}",
                    )

                options_data.append(
                    (
                        spot,
                        strike,
                        rate,
                        volatility,
                        maturity,
                    )
                )

        if st.button("Price Batch", key="batch_price"):
            try:
                pricer = EuropeanCallPricer()
                results = []

                for spot, strike, rate, volatility, maturity in options_data:
                    result = pricer.price(
                        spot_price=spot,
                        strike_price=strike,
                        risk_free_rate=rate,
                        volatility=volatility,
                        maturity_years=maturity,
                    )

                    results.append(
                        {
                            "Spot": f"${spot:.2f}",
                            "Strike": f"${strike:.2f}",
                            "Price": f"${result.estimated_price:.4f}",
                            "Standard Error": (
                                f"${result.standard_error:.6f}"
                            ),
                        }
                    )

                results_df = pd.DataFrame(results)

                st.dataframe(
                    results_df,
                    use_container_width=True,
                    hide_index=True,
                )

                logger.info("Batch priced %s options", len(results))

            except ValueError as error:
                st.error(f"Invalid batch-pricing input: {error}")
                logger.warning("Invalid batch-pricing input: %s", error)

            except Exception as error:
                st.error(f"Error in batch pricing: {error}")
                logger.exception("Batch-pricing error")

    else:
        uploaded_file = st.file_uploader(
            "Upload a CSV file",
            type=["csv"],
            help=(
                "CSV support will be connected to the pricing engine "
                "in a later phase."
            ),
        )

        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_csv(uploaded_file)
                st.dataframe(uploaded_df, use_container_width=True)
                st.info(
                    "CSV preview loaded. Automated CSV pricing is not "
                    "implemented yet."
                )

            except Exception as error:
                st.error(f"Could not read the CSV file: {error}")


def show_sensitivity_analysis():
    """Display the sensitivity-analysis interface."""
    st.subheader("Sensitivity Analysis")

    col1, col2 = st.columns(2)

    with col1:
        spot_price = st.number_input(
            "Spot Price",
            min_value=1.0,
            value=100.0,
            step=1.0,
            key="sens_s",
        )

        strike_price = st.number_input(
            "Strike Price",
            min_value=1.0,
            value=105.0,
            step=1.0,
            key="sens_k",
        )

        risk_free_rate = st.slider(
            "Risk-Free Rate",
            min_value=0.0,
            max_value=0.2,
            value=0.05,
            step=0.01,
            key="sens_r",
        )

    with col2:
        volatility = st.slider(
            "Volatility",
            min_value=0.01,
            max_value=1.0,
            value=0.2,
            step=0.01,
            key="sens_v",
        )

        maturity_years = st.number_input(
            "Maturity",
            min_value=0.01,
            max_value=10.0,
            value=1.0,
            step=0.1,
            key="sens_t",
        )

    parameter = st.selectbox(
        "Parameter to vary:",
        ["spot_price", "volatility", "risk_free_rate"],
        help="Select the parameter for sensitivity analysis.",
    )

    range_col, steps_col = st.columns(2)

    with range_col:
        range_pct = (
            st.slider(
                "Range (%)",
                min_value=5,
                max_value=50,
                value=20,
                step=5,
            )
            / 100.0
        )

    with steps_col:
        steps = st.slider(
            "Steps",
            min_value=3,
            max_value=20,
            value=5,
            step=1,
        )

    if st.button("Run Sensitivity Analysis", key="sensitivity"):
        try:
            pricer = EuropeanCallPricer()

            results = pricer.sensitivity_analysis(
                spot_price=spot_price,
                strike_price=strike_price,
                risk_free_rate=risk_free_rate,
                volatility=volatility,
                maturity_years=maturity_years,
                parameter=parameter,
                range_pct=range_pct,
                steps=steps,
            )

            results_df = pd.DataFrame(
                {
                    "Parameter Value": list(results.keys()),
                    "Option Price": list(results.values()),
                }
            )

            st.line_chart(
                results_df.set_index("Parameter Value")
            )

            st.dataframe(
                results_df,
                use_container_width=True,
                hide_index=True,
            )

            logger.info(
                "Sensitivity analysis completed for %s",
                parameter,
            )

        except ValueError as error:
            st.error(f"Invalid sensitivity-analysis input: {error}")
            logger.warning(
                "Invalid sensitivity-analysis input: %s",
                error,
            )

        except Exception as error:
            st.error(f"Error in sensitivity analysis: {error}")
            logger.exception("Sensitivity-analysis error")
