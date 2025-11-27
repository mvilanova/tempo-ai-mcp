"""
Workout-related MCP tools for Tempo AI.

This module contains tools for retrieving athlete workouts from the Tempo AI API.
"""

from typing import Any

from tempoai_mcp_server.api.client import make_tempo_ai_request
from tempoai_mcp_server.utils.formatting import format_workout_summary, format_workout_details
from tempoai_mcp_server.utils.validation import resolve_date_params

# Import mcp instance from shared module for tool registration
from tempoai_mcp_server.mcp_instance import mcp  # noqa: F401

# Assert mcp is not None for type checking (initialized by server.py before tools are used)
assert mcp is not None, "MCP instance must be initialized before importing tools"


def _format_workouts_response(
    workouts: list[dict[str, Any]],
    total: int,
) -> str:
    """Format the workouts response."""
    if not workouts:
        return "No workouts found in the specified date range."

    response = f"Workouts ({len(workouts)} of {total} total):\n\n"
    for workout in workouts:
        if isinstance(workout, dict):
            response += format_workout_summary(workout) + "\n"
        else:
            response += f"Invalid workout format: {workout}\n\n"

    return response


@mcp.tool()
async def get_workouts(
    start_date: str | None = None,
    end_date: str | None = None,
    limit: int = 50,
    offset: int = 0,
    api_key: str | None = None,
) -> str:
    """Get a list of workouts from Tempo AI.

    Args:
        start_date: Start date in YYYY-MM-DD format (optional, defaults to 30 days ago)
        end_date: End date in YYYY-MM-DD format (optional, defaults to today)
        limit: Maximum number of workouts to return (1-250, defaults to 50)
        offset: Number of workouts to skip for pagination (defaults to 0)
        api_key: The Tempo AI API key (optional, will use API_KEY from .env if not provided)
    """
    # Resolve date parameters
    start_date, end_date = resolve_date_params(start_date, end_date)

    # Build query parameters
    params: dict[str, Any] = {
        "limit": min(max(limit, 1), 250),
        "offset": max(offset, 0),
    }
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date

    # Call the Tempo AI API
    result = await make_tempo_ai_request(
        url="/mcp/workouts",
        api_key=api_key,
        params=params,
    )

    # Check for error
    if isinstance(result, dict) and "error" in result:
        error_message = result.get("message", "Unknown error")
        return f"Error fetching workouts: {error_message}"

    # Handle paginated response
    if isinstance(result, dict):
        workouts = result.get("workouts", [])
        total = result.get("total", len(workouts))
    else:
        workouts = result if isinstance(result, list) else []
        total = len(workouts)

    return _format_workouts_response(workouts, total)


@mcp.tool()
async def get_workout_details(
    workout_id: int,
    api_key: str | None = None,
) -> str:
    """Get detailed information for a specific workout from Tempo AI.

    Args:
        workout_id: The Tempo AI workout ID
        api_key: The Tempo AI API key (optional, will use API_KEY from .env if not provided)
    """
    # Call the Tempo AI API
    result = await make_tempo_ai_request(
        url=f"/mcp/workouts/{workout_id}",
        api_key=api_key,
    )

    # Check for error
    if isinstance(result, dict) and "error" in result:
        error_message = result.get("message", "Unknown error")
        return f"Error fetching workout details: {error_message}"

    if not result:
        return f"No details found for workout {workout_id}."

    if not isinstance(result, dict):
        return f"Invalid workout format for workout {workout_id}."

    return format_workout_details(result)
