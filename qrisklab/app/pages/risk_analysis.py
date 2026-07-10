"""
Risk Analysis Page

Provides interface for Value at Risk (VaR) and Conditional Value at Risk (CVaR) calculations.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import List

from qrisklab.finance.risk import RiskAnalyzer
from qrisklab.utils.logger import get_logger

logger = get_logger(__name__)


def show():
    """Display risk analysis page."""
    st.header("Risk Analysis")
    st.markdown("Calculate Value at Risk (VaR) and Conditional Value at Risk (CVaR)")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Single Analysis", "Multi-Level Analysis", "Loss Distribution"])
    
    with tab1:
        show_single_analysis()
    
    with tab2:
        show_multi_level_analysis()
    
    with tab3:
        show_loss_distribution()


def show_single_analysis():
    """Display single risk analysis interface."""
    st.subheader("Single Confidence Level Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        random_seed = st.number_input(
            "Random Seed",
            value=42,
            step=1,
            help="Seed for random number generation"
        )
        confidence_level = st.slider(
            "Confidence Level",
            min_value=0.80,
            max_value=0.99,
            value=0.95,
            step=0.01,
            help="Confidence level for VaR/CVaR (e.g., 0.95 for 95%)"
        )
        num_scenarios = st.number_input(
            "Number of Loss Scenarios",
            min_value=100,
            value=10000,
            step=1000,
            help="Number of simulated loss scenarios"
        )
    
    with col2:
        mean_loss = st.number_input(
            "Mean Loss",
            value=0.0,
            step=10.0,
            help="Mean of loss distribution"
        )
        std_loss = st.number_input(
            "Std Dev Loss",
            min_value=1.0,
            value=100.0,
            step=10.0,
            help="Standard deviation of loss distribution"
        )
    
    if st.button("Calculate Risk Metrics", key="single_risk"):
        try:
            # Generate synthetic loss data
            seed = int(random_seed)
            num_scenarios = int(num_scenarios)
            rng = np.random.default_rng(seed)
            losses = rng.normal(mean_loss, std_loss, num_scenarios).tolist()
            
            analyzer = RiskAnalyzer()
            result = analyzer.analyze_risk(losses, confidence_level)
            
            # Display results
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("VaR", f"${result.var:.2f}")
            col2.metric("CVaR", f"${result.cvar:.2f}")
            col3.metric("Mean Loss", f"${result.mean_loss:.2f}")
            col4.metric("Std Dev", f"${result.std_loss:.2f}")
            
            # Display statistics
            st.subheader("Loss Statistics")
            stats_df = pd.DataFrame({
                "Metric": ["Min Loss", "Max Loss", "Mean Loss", "Std Dev", "Sample Count"],
                "Value": [
                    f"${result.min_loss:.2f}",
                    f"${result.max_loss:.2f}",
                    f"${result.mean_loss:.2f}",
                    f"${result.std_loss:.2f}",
                    f"{result.sample_count:,}"
                ]
            })
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
            
            logger.info(f"Risk analysis: VaR={result.var:.2f}, CVaR={result.cvar:.2f}")
            
        except Exception as e:
            st.error(f"Error calculating risk metrics: {str(e)}")
            logger.error(f"Risk analysis error: {e}")


def show_multi_level_analysis():
    """Display multi-level risk analysis interface."""
    st.subheader("Multi-Level Confidence Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        random_seed = st.number_input(
            "Random Seed",
            value=42,
            step=1,
            key="multi_seed",
            help="Seed for random number generation"
        )
        num_scenarios = st.number_input(
            "Number of Scenarios",
            min_value=100,
            value=10000,
            step=1000,
            key="multi_scenarios"
        )
        mean_loss = st.number_input(
            "Mean Loss",
            value=0.0,
            step=10.0,
            key="multi_mean"
        )
    
    with col2:
        std_loss = st.number_input(
            "Std Dev Loss",
            min_value=1.0,
            value=100.0,
            step=10.0,
            key="multi_std"
        )
    
    # Select confidence levels
    st.markdown("**Select Confidence Levels:**")
    col1, col2, col3 = st.columns(3)
    cl_90 = col1.checkbox("90%", value=True)
    cl_95 = col2.checkbox("95%", value=True)
    cl_99 = col3.checkbox("99%", value=True)
    
    confidence_levels = []
    if cl_90:
        confidence_levels.append(0.90)
    if cl_95:
        confidence_levels.append(0.95)
    if cl_99:
        confidence_levels.append(0.99)
    
    if st.button("Run Multi-Level Analysis", key="multi_risk"):
        try:
            if not confidence_levels:
                st.warning("Please select at least one confidence level.")
                return

            # Generate synthetic loss data
            seed = int(random_seed)
            num_scenarios = int(num_scenarios)
            rng = np.random.default_rng(seed)
            losses = rng.normal(mean_loss, std_loss, num_scenarios).tolist()
            
            analyzer = RiskAnalyzer()
            results_dict = analyzer.multi_level_analysis(losses, confidence_levels)
            
            # Display results table
            results_data = []
            for cl, result in results_dict.items():
                results_data.append({
                    "Confidence Level": f"{cl:.0%}",
                    "VaR": f"${result.var:.2f}",
                    "CVaR": f"${result.cvar:.2f}",
                    "Mean Loss": f"${result.mean_loss:.2f}",
                    "Std Dev": f"${result.std_loss:.2f}",
                })
            
            results_df = pd.DataFrame(results_data)
            st.dataframe(results_df, use_container_width=True, hide_index=True)
            
            logger.info(f"Multi-level analysis: {len(results_dict)} confidence levels")
            
        except Exception as e:
            st.error(f"Error in multi-level analysis: {str(e)}")
            logger.error(f"Multi-level analysis error: {e}")


def show_loss_distribution():
    """Display loss distribution visualization."""
    st.subheader("Loss Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_scenarios = st.number_input(
            "Number of Scenarios",
            min_value=100,
            value=10000,
            step=1000,
            key="dist_scenarios"
        )
        mean_loss = st.number_input(
            "Mean Loss",
            value=0.0,
            step=10.0,
            key="dist_mean"
        )
    
    with col2:
        std_loss = st.number_input(
            "Std Dev Loss",
            min_value=1.0,
            value=100.0,
            step=10.0,
            key="dist_std"
        )
        confidence_level = st.slider(
            "Confidence Level",
            0.80,
            0.99,
            0.95,
            0.01,
            key="dist_cl"
        )
        seed = st.number_input(
            "Random Seed",
            min_value=0,
            value=42,
            step=1,
            key="dist_seed"
        )
    
    if st.button("Generate Distribution", key="dist_gen"):
        try:
            # Generate synthetic loss data
            seed = int(seed)
            num_scenarios = int(num_scenarios)
            rng = np.random.default_rng(seed)
            losses = rng.normal(mean_loss, std_loss, num_scenarios)
            
            # Calculate VaR
            analyzer = RiskAnalyzer()
            var = analyzer.calculate_var(losses.tolist(), confidence_level)
            
            st.markdown(f"**VaR at {confidence_level:.0%} confidence: ${var:.2f}**")
            
            # Display histogram
            st.bar_chart(
                pd.cut(losses, bins=50).value_counts().sort_index(),
                use_container_width=True
            )
            
            logger.info(f"Loss distribution generated: {num_scenarios} scenarios")
            
        except Exception as e:
            st.error(f"Error generating distribution: {str(e)}")
            logger.error(f"Distribution error: {e}")
