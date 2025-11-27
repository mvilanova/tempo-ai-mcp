"""
Tempo AI MCP Server

This module implements a Model Context Protocol (MCP) server for connecting
Claude with the Tempo AI API. It provides read-only tools for retrieving
athlete data including workouts, events, and wellness metrics.

Main Features:
    - Workout retrieval and detailed analysis
    - Event listing and details
    - Wellness data tracking
    - Error handling with user-friendly messages
    - Configurable parameters with environment variable support

Usage:
    This server is designed to be run as a standalone script and exposes several MCP tools
    for use with Claude Desktop or other MCP-compatible clients. The server loads configuration
    from environment variables (optionally via a .env file) and communicates with the Tempo AI API.

    To run the server:
        $ python src/tempoai_mcp_server/server.py

    MCP tools provided:
        - get_workouts
        - get_workout_details
        - get_events
        - get_event_details
        - get_wellness

    See the README for more details on configuration and usage.
"""

import logging

from mcp.server.fastmcp import FastMCP

# Import API client and configuration
from tempoai_mcp_server.api.client import (
    httpx_client,  # Re-export for backward compatibility with tests
    make_tempo_ai_request,
    setup_api_client,
)
from tempoai_mcp_server.config import get_config

# Import types and validation
from tempoai_mcp_server.server_setup import setup_transport, start_server

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("tempoai_mcp_server")

# Get configuration instance
config = get_config()

# Initialize FastMCP server with custom lifespan
mcp = FastMCP("tempoai", lifespan=setup_api_client)

# Set the shared mcp instance for tool modules to use (breaks cyclic imports)
from tempoai_mcp_server import mcp_instance  # noqa: E402

mcp_instance.mcp = mcp

# Import tool modules to register them (tools register themselves via @mcp.tool() decorators)
# Import tool functions for re-export (imported after mcp instance creation)
from tempoai_mcp_server.tools.workouts import (  # noqa: E402
    get_workouts,
    get_workout_details,
)
from tempoai_mcp_server.tools.events import (  # noqa: E402
    get_events,
    get_event_details,
)
from tempoai_mcp_server.tools.wellness import get_wellness  # noqa: E402

# Re-export make_tempo_ai_request and httpx_client for backward compatibility
# This __all__ list is intentionally similar to tools/__init__.py
__all__ = [
    "make_tempo_ai_request",
    "httpx_client",  # Re-exported for test compatibility
    "get_workouts",
    "get_workout_details",
    "get_events",
    "get_event_details",
    "get_wellness",
]


# Run the server
if __name__ == "__main__":
    # Setup transport and start server
    selected_transport = setup_transport()
    start_server(mcp, selected_transport)
