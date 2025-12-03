"""
Tempo AI MCP Server CLI.

This module provides a command-line interface for installing and managing
the Tempo AI MCP Server. It uses Click for command handling.

Usage:
    tempo-ai-mcp install
    tempo-ai-mcp install --api-key YOUR_API_KEY
"""

import subprocess
from pathlib import Path

import click


def get_package_dir() -> Path:
    """Get the package installation directory."""
    return Path(__file__).parent.parent.parent


def create_env_file(api_key: str, package_dir: Path) -> Path:
    """Create .env file with the API key.

    Args:
        api_key: The Tempo AI API key.
        package_dir: The package installation directory.

    Returns:
        Path to the created .env file.
    """
    env_file = package_dir / ".env"
    env_file.write_text(f"API_KEY={api_key}\n")
    env_file.chmod(0o600)
    return env_file


def run_mcp_install(server_path: Path, package_dir: Path, env_file: Path) -> None:
    """Run the mcp install command to configure Claude Desktop.

    Args:
        server_path: Path to the server.py file.
        package_dir: Path to the package directory.
        env_file: Path to the .env file.

    Raises:
        click.ClickException: If the mcp install command fails.
    """
    cmd = [
        "mcp",
        "install",
        str(server_path),
        "--name",
        "TempoAI",
        "--with-editable",
        str(package_dir),
        "--env-file",
        str(env_file),
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except FileNotFoundError as err:
        raise click.ClickException(
            "The 'mcp' command was not found. "
            "Please ensure mcp[cli] is installed: pip install 'mcp[cli]'"
        ) from err
    except subprocess.CalledProcessError:
        raise click.ClickException(
            "Failed to configure Claude Desktop. Please check your configuration and try again."
        ) from None


@click.group()
@click.version_option(package_name="tempo-ai-mcp")
def cli() -> None:
    """Tempo AI MCP Server - Connect Claude with your Tempo AI data."""
    ...


@cli.command()
@click.option(
    "--api-key",
    envvar="TEMPO_API_KEY",
    help="Tempo AI API key. Will prompt if not provided.",
)
def install(api_key: str | None) -> None:
    """Install and configure Tempo AI MCP Server for Claude Desktop.

    This command will:
    1. Prompt for your Tempo AI API key (if not provided)
    2. Create the necessary configuration
    3. Register the MCP server with Claude Desktop

    After running this command, restart Claude Desktop to start using
    the Tempo AI tools.
    """
    click.echo()
    click.secho("╔══════════════════════════════════════════════════════════════╗", fg="green")
    click.secho("║              Tempo AI MCP Server Setup                       ║", fg="green")
    click.secho("╚══════════════════════════════════════════════════════════════╝", fg="green")
    click.echo()

    # Prompt for API key if not provided
    if not api_key:
        click.secho("🔑 API Key Setup", fg="yellow", bold=True)
        click.echo()
        click.echo("To get your API key:")
        click.echo("  1. Log in at https://jointempo.ai/signin")
        click.echo("  2. Go to Settings > Developer")
        click.echo("  3. Generate a new API key")
        click.echo()
        api_key = click.prompt("Enter your Tempo AI API key", hide_input=True)

    if not api_key or not api_key.strip():
        raise click.ClickException("API key is required.")

    api_key = api_key.strip()

    # Get paths
    package_dir = get_package_dir()
    server_path = package_dir / "src" / "tempoai_mcp_server" / "server.py"

    # Verify server.py exists
    if not server_path.exists():
        raise click.ClickException(
            f"Server file not found at {server_path}. "
            "Please ensure the package is installed correctly."
        )

    # Create .env file
    click.echo()
    click.secho("📝 Creating environment configuration...", fg="yellow")
    env_file = create_env_file(api_key, package_dir)
    click.secho("✓ Environment configured", fg="green")

    # Configure Claude Desktop
    click.secho("🔧 Configuring Claude Desktop...", fg="yellow")
    run_mcp_install(server_path, package_dir, env_file)
    click.secho("✓ Claude Desktop configured", fg="green")

    # Success message
    click.echo()
    click.secho("╔══════════════════════════════════════════════════════════════╗", fg="green")
    click.secho("║                  Installation Complete!                      ║", fg="green")
    click.secho("╚══════════════════════════════════════════════════════════════╝", fg="green")
    click.echo()
    click.echo("Next steps:")
    click.echo("  1. Restart Claude Desktop")
    click.echo("  2. Start a new conversation and ask about your workouts!")
    click.echo()


if __name__ == "__main__":
    cli()
