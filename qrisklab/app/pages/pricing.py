"""
Option Pricing Page

Provides interface for European call option pricing with Monte Carlo simulation.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Tuple

from qrisklab.finance.pricing import EuropeanCallPricer
import random
from qrisklab.utils.logger import get_logger

logger = get_logger(__name__)


def show():
    """Display option pricing page."""
    st.header("📈 European Call Option Pricing")
    st.markdown("Price European call options using Monte Carlo simulation")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Single Option", "Batch Pricing", "Sensitivity Analysis"])
    
    with tab1:
        show_single_pricing()
    
    with tab2:
        show_batch_pricing()
    
    with tab3:
        show_sensitivity_analysis()


def show_single_pricing():
    """Display single option pricing interface."""
    st.subheader("Price Single Option")
    
    col1, col2 = st.columns(2)
    
    with col1:
        spot_price = st.number_input(
            "Spot Price (S)",
            min_value=1.0,
            value=100.0,
            step=1.0,
            help="Current stock price"
        )
        strike_price = st.number_input(
            "Strike Price (K)",
            min_value=1.0,
            value=105.0,
            step=1.0,
            help="Option strike price"
        )
        risk_free_rate = st.slider(
            "Risk-Free Rate (r)",
            min_value=0.0,
            max_value=0.2,
            value=0.05,
            step=0.01,
            help="Annual risk-free interest rate"
        )
    
    with col2:
        volatility = st.slider(
            "Volatility (σ)",
            min_value=0.01,
            max_value=1.0,
            value=0.2,
            step=0.01,
            help="Annual volatility"
        )
        maturity_years = st.number_input(
            "Maturity (T)",
            min_value=0.01,
            value=1.0,
            step=0.1,
            help="Time to maturity in years"
        )
        paths = st.number_input(
            "Monte Carlo Paths",
            min_value=100,
            value=10000,
            step=1000,
            help="Number of simulation paths"
        )
    
    if st.button("Calculate Price", key="single_price"):
        try:
            seed = random.randint(0, 2**32 - 1)  # Generate a random seed
            pricer = EuropeanCallPricer(default_paths=paths, default_seed=seed)
            result = pricer.price(
                spot_price=spot_price,
                strike_price=strike_price,
                risk_free_rate=risk_free_rate,
                volatility=volatility,
                maturity_years=maturity_years,
                paths=paths,
                seed=seed,
            )
            
            # Display results
            col1, col2, col3 = st.columns(3)
            col1.metric("Option Price", f"${result.estimated_price:.4f}")
            col2.metric("Standard Error", f"${result.standard_error:.6f}")
            col3.metric("Paths", f"{paths:,}")
            
            # Display input parameters
            st.subheader("Input Parameters")
            params_df = pd.DataFrame({
                "Parameter": ["Spot Price", "Strike Price", "Risk-Free Rate", "Volatility", "Maturity"],
                "Value": [f"${spot_price:.2f}", f"${strike_price:.2f}", f"{risk_free_rate:.2%}", f"{volatility:.2%}", f"{maturity_years:.2f} years"]
            })
            st.dataframe(params_df, use_container_width=True, hide_index=True)
            
            logger.info(f"Priced option: S={spot_price}, K={strike_price}, Price={result.estimated_price:.4f}")
            
        except ValueError as ve:
            st.error(f"Value error: {str(ve)}")
            
        except Exception as e:
        except Exception as e:
            st.error(f"Error calculating price: {str(e)}")
            logger.error(f"Pricing error: {e}")


def show_batch_pricing():
    """Display batch pricing interface."""
    st.subheader("Batch Pricing")
    
    st.markdown("Upload or enter multiple options to price")
    
    # Option to upload CSV or enter manually
    input_method = st.radio("Input method:", ["Manual Entry", "CSV Upload"])
    
    if input_method == "Manual Entry":
        st.markdown("Enter option parameters below:")
        
        num_options = st.number_input("Number of options", min_value=1, max_value=10, value=2)
        
        options_data = []
        for i in range(num_options):
            with st.expander(f"Option {i+1}"):
                col1, col2 = st.columns(2)
                with col1:
                    s = st.number_input(f"Spot Price {i+1}", value=100.0, key=f"s_{i}")
                    k = st.number_input(f"Strike Price {i+1}", value=105.0, key=f"k_{i}")
                    r = st.slider(f"Rate {i+1}", 0.0, 0.2, 0.05, key=f"r_{i}")
                with col2:
                    v = st.slider(f"Volatility {i+1}", 0.01, 1.0, 0.2, key=f"v_{i}")
                    t = st.number_input(f"Maturity {i+1}", 0.01, 10.0, 1.0, key=f"t_{i}")
                
                options_data.append((s, k, r, v, t))
        
        if st.button("Price Batch", key="batch_price"):
            try:
                pricer = EuropeanCallPricer()
                results = []
                
                for s, k, r, v, t in options_data:
                    result = pricer.price(s, k, r, v, t)
                    results.append({
                        "Spot": f"${s:.2f}",
                        "Strike": f"${k:.2f}",
                        "Price": f"${result.estimated_price:.4f}",
                        "Std Error": f"${result.standard_error:.6f}",
                    })
                
                results_df = pd.DataFrame(results)
                st.dataframe(results_df, use_container_width=True, hide_index=True)
                
                logger.info(f"Batch priced {len(results)} options")
                
            except Exception as e:
                st.error(f"Error in batch pricing: {str(e)}")
                logger.error(f"Batch pricing error: {e}")


def show_sensitivity_analysis():
    """Display sensitivity analysis interface."""
    st.subheader("Sensitivity Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        spot_price = st.number_input("Spot Price", value=100.0, key="sens_s")
        strike_price = st.number_input("Strike Price", value=105.0, key="sens_k")
        risk_free_rate = st.slider("Risk-Free Rate", 0.0, 0.2, 0.05, key="sens_r")
    
    with col2:
        volatility = st.slider("Volatility", 0.01, 1.0, 0.2, key="sens_v")
        maturity_years = st.number_input("Maturity", 0.01, 10.0, 1.0, key="sens_t")
    
    parameter = st.selectbox(
        "Parameter to vary:",
        ["spot_price", "volatility", "risk_free_rate"],
        help="Which parameter to perform sensitivity analysis on"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        range_pct = st.slider("Range (%)", 5, 50, 20) / 100.0
    with col2:
        steps = st.slider("Steps", 3, 20, 5)
    
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
            
            # Convert to DataFrame for visualization
            df = pd.DataFrame({
                "Parameter Value": list(results.keys()),
                "Option Price": list(results.values()),
            })
            
            # Display chart
            st.line_chart(df.set_index("Parameter Value"))
            
            # Display table
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            logger.info(f"Sensitivity analysis complete for {parameter}")
            
        except Exception as e:
            st.error(f"Error in sensitivity analysis: {str(e)}")
            logger.error(f"Sensitivity analysis error: {e}")
