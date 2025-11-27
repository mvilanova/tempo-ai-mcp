"""
Wellness-related MCP tools for Tempo AI.

This module contains tools for retrieving athlete wellness data from the Tempo AI API.
"""

from typing import Any

from tempoai_mcp_server.api.client import make_tempo_ai_request
from tempoai_mcp_server.utils.formatting import format_wellness_entry
from tempoai_mcp_server.utils.validation import resolve_date_params

# Import mcp instance from shared module for tool registration
from tempoai_mcp_server.mcp_instance import mcp  # noqa: F401

# Assert mcp is not None for type checking (initialized by server.py before tools are used)
assert mcp is not None, "MCP instance must be initialized before importing tools"


def _format_wellness_response(
    wellness_data: list[dict[str, Any]],
    total: int,
) -> str:
    """Format the wellness response."""
    if not wellness_data:
        return "No wellness data found in the specified date range."

    response = f"Wellness Data ({len(wellness_data)} of {total} total):\n\n"
    for entry in wellness_data:
        if isinstance(entry, dict):
            response += format_wellness_entry(entry) + "\n\n"
        else:
            response += f"Invalid wellness entry format: {entry}\n\n"

    return response


@mcp.tool()
async def get_wellness(
    start_date: str | None = None,
    end_date: str | None = None,
    api_key: str | None = None,
) -> str:
    """Get wellness data from Tempo AI.

    Args:
        start_date: Start date in YYYY-MM-DD format (optional, defaults to 30 days ago)
        end_date: End date in YYYY-MM-DD format (optional, defaults to today)
        api_key: The Tempo AI API key (optional, will use API_KEY from .env if not provided)
    """
    # Resolve date parameters
    start_date, end_date = resolve_date_params(start_date, end_date)

    # Build query parameters
    params: dict[str, Any] = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date

    # Call the Tempo AI API
    result = await make_tempo_ai_request(
        url="/mcp/wellness",
        api_key=api_key,
        params=params,
    )

    # Check for error
    if isinstance(result, dict) and "error" in result:
        error_message = result.get("message", "Unknown error")
        return f"Error fetching wellness data: {error_message}"

    # Handle paginated response
    if isinstance(result, dict):
        wellness_data = result.get("wellness", [])
        total = result.get("total", len(wellness_data))
    else:
        wellness_data = result if isinstance(result, list) else []
        total = len(wellness_data)

    return _format_wellness_response(wellness_data, total)
