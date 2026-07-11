"""
Portfolio Management Page

Provides interface for portfolio construction and risk analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import List, Dict

from qrisklab.finance.portfolio import Portfolio, Position
from qrisklab.utils.logger import get_logger

logger = get_logger(__name__)


def show():
    """Display portfolio management page."""
    st.header("💼 Portfolio Management")
    st.markdown("Build and analyze investment portfolios")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Build Portfolio", "Analyze Risk", "Portfolio Summary"])
    
    with tab1:
        show_build_portfolio()
    
    with tab2:
        show_analyze_risk()
    
    with tab3:
        show_portfolio_summary()


def show_build_portfolio():
    """Display portfolio construction interface."""
    st.subheader("Build Portfolio")
    
    portfolio_name = st.text_input(
        "Portfolio Name",
        value="My Portfolio",
        help="Name for your portfolio"
    )
    
    num_positions = st.number_input(
        "Number of Positions",
        min_value=1,
        max_value=20,
        value=3,
        help="Number of positions in portfolio"
    )
    
    st.markdown("**Enter Position Details:**")
    
    positions_data = []
    for i in range(num_positions):
        with st.expander(f"Position {i+1}"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input(
                    f"Position Name {i+1}",
                    value=f"Asset {i+1}",
                    key=f"pos_name_{i}"
                )
                value = st.number_input(
                    f"Position Value {i+1}",
                    min_value=0.0,
                    value=100000.0,
                    step=1000.0,
                    key=f"pos_value_{i}"
                )
            
            with col2:
                expected_return = st.slider(
                    f"Expected Return {i+1}",
                    min_value=-0.2,
                    max_value=0.5,
                    value=0.07,
                    step=0.01,
                    key=f"pos_return_{i}",
                    format="%.2%"
                )
                volatility = st.slider(
                    f"Volatility {i+1}",
                    min_value=0.01,
                    max_value=1.0,
                    value=0.15,
                    step=0.01,
                    key=f"pos_vol_{i}",
                    format="%.2%"
                )
            
            if value > 0:
                positions_data.append({
                    "name": name,
                    "value": value,
                    "expected_return": expected_return,
                    "volatility": volatility,
                })
    
    if st.button("Create Portfolio", key="create_portfolio"):
        try:
            portfolio = Portfolio(name=portfolio_name)
            
            for pos in positions_data:
                portfolio.add_position(
                    name=pos["name"],
                    value=pos["value"],
                    expected_return=pos["expected_return"],
                    volatility=pos["volatility"],
                )
            
            # Display portfolio summary
            summary = portfolio.get_summary()
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Value", f"${summary['total_value']:,.2f}")
            col2.metric("Expected Return", f"{summary['expected_return']:.2%}")
            col3.metric("Volatility", f"{summary['volatility']:.2%}")
            col4.metric("Positions", summary['position_count'])
            
            # Display position weights
            st.subheader("Position Weights")
            weights_data = []
            for pos in summary['positions']:
                weights_data.append({
                    "Position": pos['name'],
                    "Value": f"${pos['value']:,.2f}",
                    "Weight": f"{pos['weight']:.2%}",
                    "Return": f"{pos['expected_return']:.2%}",
                    "Volatility": f"{pos['volatility']:.2%}",
                })
            
            weights_df = pd.DataFrame(weights_data)
            st.dataframe(weights_df, use_container_width=True, hide_index=True)
            
            # Store portfolio in session state
            st.session_state.portfolio = portfolio
            st.success("Portfolio created successfully!")
            
            logger.info(f"Portfolio created: {portfolio_name} with {len(positions_data)} positions")
            
        except Exception as e:
            st.error(f"Error creating portfolio: {str(e)}")
            logger.error(f"Portfolio creation error: {e}")


def show_analyze_risk():
    """Display portfolio risk analysis interface."""
    st.subheader("Analyze Portfolio Risk")
    
    if "portfolio" not in st.session_state:
        st.info("Create a portfolio first in the 'Build Portfolio' tab")
        return
    
    portfolio = st.session_state.portfolio
    
    col1, col2 = st.columns(2)
    
    with col1:
        time_horizon = st.number_input(
            "Time Horizon (years)",
            min_value=0.01,
            value=1.0,
            step=0.1,
            help="Time horizon for risk analysis"
        )
        scenarios = st.number_input(
            "Simulation Scenarios",
            min_value=100,
            value=10000,
            step=1000,
            help="Number of Monte Carlo scenarios"
        )
    
    with col2:
        confidence_level = st.slider(
            "Confidence Level",
            min_value=0.80,
            max_value=0.99,
            value=0.95,
            step=0.01,
            help="Confidence level for VaR/CVaR"
        )
    
    if st.button("Analyze Risk", key="analyze_portfolio_risk"):
        try:
            with st.spinner("Analyzing portfolio risk..."):
                result = portfolio.analyze_risk(
                    time_horizon_years=time_horizon,
                    scenarios=scenarios,
                    confidence_level=confidence_level,
                )
            
            # Display results
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("VaR", f"${result.var:,.2f}")
            col2.metric("CVaR", f"${result.cvar:,.2f}")
            col3.metric("Mean Loss", f"${result.mean_loss:,.2f}")
            col4.metric("Std Dev", f"${result.std_loss:,.2f}")
            
            # Display statistics
            st.subheader("Risk Statistics")
            stats_df = pd.DataFrame({
                "Metric": ["Min Loss", "Max Loss", "Mean Loss", "Std Dev", "Scenarios"],
                "Value": [
                    f"${result.min_loss:,.2f}",
                    f"${result.max_loss:,.2f}",
                    f"${result.mean_loss:,.2f}",
                    f"${result.std_loss:,.2f}",
                    f"{result.sample_count:,}"
                ]
            })
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
            
            logger.info(f"Portfolio risk analysis: VaR={result.var:.2f}, CVaR={result.cvar:.2f}")
            
        except Exception as e:
            st.error(f"Error analyzing portfolio risk: {str(e)}")
            logger.error(f"Portfolio risk analysis error: {e}")


def show_portfolio_summary():
    """Display portfolio summary."""
    st.subheader("Portfolio Summary")
    
    if "portfolio" not in st.session_state:
        st.info("Create a portfolio first in the 'Build Portfolio' tab")
        return
    
    portfolio = st.session_state.portfolio
    summary = portfolio.get_summary()

    if portfolio.positions:
        selected_position = st.selectbox(
            "Position to Remove",
            options=[position.name for position in portfolio.positions],
            key="remove_portfolio_position",
        )
        if st.button("Remove Position", key="remove_position"):
            if portfolio.remove_position(selected_position):
                st.success(f"Removed position: {selected_position}")
                st.rerun()
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Portfolio Name", summary['name'])
    col2.metric("Total Value", f"${summary['total_value']:,.2f}")
    col3.metric("Expected Return", f"{summary['expected_return']:.2%}")
    col4.metric("Volatility", f"{summary['volatility']:.2%}")
    
    # Display positions
    st.subheader("Positions")
    positions_data = []
    for pos in summary['positions']:
        positions_data.append({
            "Position": pos['name'],
            "Value": f"${pos['value']:,.2f}",
            "Weight": f"{pos['weight']:.2%}",
            "Expected Return": f"{pos['expected_return']:.2%}",
            "Volatility": f"{pos['volatility']:.2%}",
        })
    
    positions_df = pd.DataFrame(positions_data)
    st.dataframe(positions_df, use_container_width=True, hide_index=True)
    
    # Display pie chart of weights
    st.subheader("Portfolio Allocation")
    weights = [pos['weight'] for pos in summary['positions']]
    labels = [pos['name'] for pos in summary['positions']]
    
    chart_data = pd.DataFrame({
        "Position": labels,
        "Weight": weights,
    })
    
    st.bar_chart(chart_data.set_index("Position"))
