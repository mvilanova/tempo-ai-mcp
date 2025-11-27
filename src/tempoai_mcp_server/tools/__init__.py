"""
MCP tools registry for Tempo AI MCP Server.

This module registers all available MCP tools with the FastMCP server instance.
"""

from mcp.server.fastmcp import FastMCP

# Import all tools for re-export
# Note: Tools register themselves via @mcp.tool() decorators when imported
from tempoai_mcp_server.tools.workouts import (  # noqa: F401
    get_workouts,
    get_workout_details,
)
from tempoai_mcp_server.tools.events import (  # noqa: F401
    get_events,
    get_event_details,
)
from tempoai_mcp_server.tools.wellness import get_wellness  # noqa: F401


def register_tools(mcp_instance: FastMCP) -> None:
    """
    Register all MCP tools with the FastMCP server instance.

    This function imports all tool modules, which causes their @mcp.tool()
    decorators to register the tools. The tools need access to the mcp instance,
    so they will be imported after the mcp instance is created.

    Args:
        mcp_instance (FastMCP): The FastMCP server instance to register tools with.
    """
    # Tools are registered via decorators when modules are imported above
    # The mcp_instance parameter is kept for future use if needed
    _ = mcp_instance


__all__ = [
    "register_tools",
    "get_workouts",
    "get_workout_details",
    "get_events",
    "get_event_details",
    "get_wellness",
]
