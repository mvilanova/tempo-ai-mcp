"""
Configuration management for Tempo AI MCP Server.

This module handles loading and validation of configuration from environment variables.
"""

import os
from dataclasses import dataclass

# Try to load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv

    _ = load_dotenv()
except ImportError:
    # python-dotenv not installed, proceed without it
    pass


@dataclass
class Config:
    """Configuration settings for the Tempo AI MCP Server."""

    api_key: str
    tempo_ai_api_base_url: str
    user_agent: str


_config_instance: Config | None = None


def load_config() -> Config:
    """
    Load configuration from environment variables.

    Returns:
        Config: Configuration instance with loaded values.
    """
    api_key = os.getenv("API_KEY", "")
    tempo_ai_api_base_url = os.getenv("TEMPO_AI_API_BASE_URL", "https://api.jointempo.ai/api/v1")
    user_agent = "tempo-ai-mcp/1.0"

    return Config(
        api_key=api_key,
        tempo_ai_api_base_url=tempo_ai_api_base_url,
        user_agent=user_agent,
    )


def get_config() -> Config:
    """
    Get the configuration instance (singleton pattern).

    Returns:
        Config: The configuration instance.
    """
    global _config_instance  # noqa: PLW0603 - singleton pattern
    if _config_instance is None:
        _config_instance = load_config()
    return _config_instance
