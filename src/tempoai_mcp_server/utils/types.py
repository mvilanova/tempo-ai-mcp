"""
Type definitions for Tempo AI MCP Server.

This module contains enums for server configuration.
"""

from enum import StrEnum


__all__ = [
    "TransportAliases",
]


class TransportAliases(StrEnum):
    """Enumeration of supported MCP transport types."""

    STDIO = "stdio"
    SSE = "sse"
    HTTP = "http"
    STREAMABLE_HTTP = "streamable-http"
