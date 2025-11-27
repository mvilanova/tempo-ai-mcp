"""
Event-related MCP tools for Tempo AI.

This module contains read-only tools for retrieving athlete events from the Tempo AI API.
"""

from typing import Any

from tempoai_mcp_server.api.client import make_tempo_ai_request
from tempoai_mcp_server.utils.formatting import format_event_details, format_event_summary
from tempoai_mcp_server.utils.validation import resolve_date_params

# Import mcp instance from shared module for tool registration
from tempoai_mcp_server.mcp_instance import mcp  # noqa: F401

# Assert mcp is not None for type checking (initialized by server.py before tools are used)
assert mcp is not None, "MCP instance must be initialized before importing tools"


def _format_events_response(
    events: list[dict[str, Any]],
    total: int,
) -> str:
    """Format the events response."""
    if not events:
        return "No events found in the specified date range."

    response = f"Events ({len(events)} of {total} total):\n\n"
    for event in events:
        if isinstance(event, dict):
            response += format_event_summary(event) + "\n\n"
        else:
            response += f"Invalid event format: {event}\n\n"

    return response


@mcp.tool()
async def get_events(
    start_date: str | None = None,
    end_date: str | None = None,
    limit: int = 50,
    offset: int = 0,
    api_key: str | None = None,
) -> str:
    """Get a list of events from Tempo AI.

    Args:
        start_date: Start date in YYYY-MM-DD format (optional, defaults to 30 days ago)
        end_date: End date in YYYY-MM-DD format (optional, defaults to today)
        limit: Maximum number of events to return (1-250, defaults to 50)
        offset: Number of events to skip for pagination (defaults to 0)
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
        url="/mcp/events",
        api_key=api_key,
        params=params,
    )

    # Check for error
    if isinstance(result, dict) and "error" in result:
        error_message = result.get("message", "Unknown error")
        return f"Error fetching events: {error_message}"

    # Handle paginated response
    if isinstance(result, dict):
        events = result.get("events", [])
        total = result.get("total", len(events))
    else:
        events = result if isinstance(result, list) else []
        total = len(events)

    return _format_events_response(events, total)


@mcp.tool()
async def get_event_details(
    event_id: int,
    api_key: str | None = None,
) -> str:
    """Get detailed information for a specific event from Tempo AI.

    Args:
        event_id: The Tempo AI event ID
        api_key: The Tempo AI API key (optional, will use API_KEY from .env if not provided)
    """
    # Call the Tempo AI API
    result = await make_tempo_ai_request(
        url=f"/mcp/events/{event_id}",
        api_key=api_key,
    )

    # Check for error
    if isinstance(result, dict) and "error" in result:
        error_message = result.get("message", "Unknown error")
        return f"Error fetching event details: {error_message}"

    if not result:
        return f"No details found for event {event_id}."

    if not isinstance(result, dict):
        return f"Invalid event format for event {event_id}."

    return format_event_details(result)
