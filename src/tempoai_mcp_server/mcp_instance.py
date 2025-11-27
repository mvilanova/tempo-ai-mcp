"""
Shared MCP instance module.

This module provides a shared FastMCP instance that can be imported by both
the server module and tool modules without creating cyclic imports.
"""

from mcp.server.fastmcp import FastMCP

# This will be initialized by server.py after creating the FastMCP instance
mcp: FastMCP | None = None  # This is a module-level variable, not a constant
