"""
Validation utilities for Tempo AI MCP Server

This module contains validation functions for input parameters.
"""

from datetime import datetime

from tempoai_mcp_server.utils.dates import parse_date_range


def validate_date(date_str: str) -> str:
    """Validate that a date string is in YYYY-MM-DD format.

    Args:
        date_str: The date string to validate.

    Returns:
        The validated date string if valid.

    Raises:
        ValueError: If the date string is not in YYYY-MM-DD format.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError as exc:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.") from exc


def resolve_date_params(
    start_date: str | None,
    end_date: str | None,
    default_start_days_ago: int = 30,
) -> tuple[str, str]:
    """Resolve start and end date parameters with defaults.

    Args:
        start_date: Optional start date in YYYY-MM-DD format.
        end_date: Optional end date in YYYY-MM-DD format.
        default_start_days_ago: Number of days ago for default start date. Defaults to 30.

    Returns:
        Tuple of (start_date, end_date) as strings in YYYY-MM-DD format.
    """
    return parse_date_range(start_date, end_date, default_start_days_ago)
