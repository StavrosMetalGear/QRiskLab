"""
Streamlit Dashboard Utilities

Provides helper functions for the Streamlit dashboard.
"""

import streamlit as st
from functools import wraps
from typing import Callable, Any
import logging

from qrisklab.utils.logger import get_logger

logger = get_logger(__name__)


def cache_data(ttl: int = 3600):
    """
    Decorator to cache data with TTL.
    
    Args:
        ttl: Time to live in seconds
    
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        @st.cache_data(ttl=ttl)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)
        return wrapper
    return decorator


def cache_resource():
    """
    Decorator to cache resources (expensive objects).
    
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        @st.cache_resource
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)
        return wrapper
    return decorator


def format_currency(value: float, decimals: int = 2) -> str:
    """
    Format value as currency.
    
    Args:
        value: Value to format
        decimals: Number of decimal places
    
    Returns:
        Formatted currency string
    """
    return f"${value:.{decimals}f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format value as percentage.
    
    Args:
        value: Value to format (0-1)
        decimals: Number of decimal places
    
    Returns:
        Formatted percentage string
    """
    return f"{value * 100:.{decimals}f}%"


def show_error(title: str, message: str) -> None:
    """
    Display error message.
    
    Args:
        title: Error title
        message: Error message
    """
    st.error(f"**{title}**\n\n{message}")
    logger.error(f"{title}: {message}")


def show_warning(title: str, message: str) -> None:
    """
    Display warning message.
    
    Args:
        title: Warning title
        message: Warning message
    """
    st.warning(f"**{title}**\n\n{message}")
    logger.warning(f"{title}: {message}")


def show_info(title: str, message: str) -> None:
    """
    Display info message.
    
    Args:
        title: Info title
        message: Info message
    """
    st.info(f"**{title}**\n\n{message}")
    logger.info(f"{title}: {message}")


def show_success(title: str, message: str) -> None:
    """
    Display success message.
    
    Args:
        title: Success title
        message: Success message
    """
    st.success(f"**{title}**\n\n{message}")
    logger.info(f"{title}: {message}")


def create_metric_row(metrics: dict) -> None:
    """
    Create a row of metrics.
    
    Args:
        metrics: Dictionary of metric_name -> metric_value
    """
    cols = st.columns(len(metrics))
    for col, (name, value) in zip(cols, metrics.items()):
        col.metric(name, value)


def create_two_column_input(
    left_label: str,
    left_value: Any,
    right_label: str,
    right_value: Any,
    **kwargs: Any
) -> tuple:
    """
    Create two-column input layout.
    
    Args:
        left_label: Left column label
        left_value: Left column default value
        right_label: Right column label
        right_value: Right column default value
        **kwargs: Additional arguments for input widgets
    
    Returns:
        Tuple of (left_result, right_result)
    """
    col1, col2 = st.columns(2)
    
    with col1:
        left_result = st.number_input(left_label, value=left_value, **kwargs)
    
    with col2:
        right_result = st.number_input(right_label, value=right_value, **kwargs)
    
    return left_result, right_result


__all__ = [
    "cache_data",
    "cache_resource",
    "format_currency",
    "format_percentage",
    "show_error",
    "show_warning",
    "show_info",
    "show_success",
    "create_metric_row",
    "create_two_column_input",
]
