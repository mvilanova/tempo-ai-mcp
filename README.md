# Tempo AI MCP Server

Model Context Protocol (MCP) server for connecting Claude and ChatGPT with the Tempo AI API. It provides tools for authentication and data retrieval for workouts, events, and wellness data.

Tempo AI allows you to train hard without burning out. Join the beta at https://jointempo.ai/.

## Requirements

- Python 3.13 or higher
- [Model Context Protocol (MCP) Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- httpx
- python-dotenv

## Setup

### 1. Install uv (recommended)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone this repository

```bash
git clone https://github.com/mvilanova/tempoai-mcp-server.git
cd tempoai-mcp-server
```

### 3. Create and activate a virtual environment

```bash
# Create virtual environment with Python 3.13
uv venv --python 3.13

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 4. Sync project dependencies

```bash
uv sync
```

### 5. Set up environment variables

Make a copy of `.env.example` and name it `.env` by running the following command:

```bash
cp .env.example .env
```

Then edit the `.env` file and set your Tempo AI API key:

```
API_KEY=your_tempoai_api_key_here
```

#### Getting your Tempo AI API Key

1. Log in to your Tempo AI account at https://jointempo.ai/signin
2. Go to Settings > Developer
3. Generate a new API key

## Updating

This project is actively developed, with new features and fixes added regularly. To stay up to date, follow these steps:

### 1. Pull the latest changes from `main`

> ⚠️ Make sure you don’t have uncommitted changes before running this command.

```bash
git checkout main && git pull
```

### 2. Update Python dependencies

Activate your virtual environment and sync dependencies:

```bash
source .venv/bin/activate
uv sync
```

### Troubleshooting

If Claude Desktop fails due to configuration changes, follow these steps:

1. Delete the existing entry in claude_desktop_config.json.
2. Reconfigure Claude Desktop from the tempoai_mcp_server directory:

```bash
mcp install src/tempoai_mcp_server/server.py --name "TempoAI" --with-editable . --env-file .env
```

## Usage with Claude

### 1. Configure Claude Desktop

To use this server with Claude Desktop, you need to add it to your Claude Desktop configuration.

1. Run the following from the `tempoai_mcp_server` directory to configure Claude Desktop:

```bash
mcp install src/tempoai_mcp_server/server.py --name "TempoAI" --with-editable . --env-file .env
```

2. If you open your Claude Desktop App configuration file `claude_desktop_config.json`, it should look like this:

```json
{
  "mcpServers": {
    "TempoAI": {
      "command": "/Users/<USERNAME>/.cargo/bin/uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "--with-editable",
        "/path/to/tempoai-mcp-server",
        "mcp",
        "run",
        "/path/to/tempoai-mcp-server/src/tempoai_mcp_server/server.py"
      ],
      "env": {
        "API_KEY": "<YOUR_API_KEY>"
      }
    }
  }
}
```

Where `/path/to/` is the path to the `tempoai-mcp-server` code folder in your system.

If you observe the following error messages when you open Claude Desktop, include the full path to `uv` in the command key in the `claude_desktop_config.json` configuration file. You can get the full path by running `which uv` in the terminal.

```
2025-04-28T10:21:11.462Z [info] [Tempo AI MCP Server] Initializing server...
2025-04-28T10:21:11.477Z [error] [Tempo AI MCP Server] spawn uv ENOENT
2025-04-28T10:21:11.477Z [error] [Tempo AI MCP Server] spawn uv ENOENT
2025-04-28T10:21:11.481Z [info] [Tempo AI MCP Server] Server transport closed
2025-04-28T10:21:11.481Z [info] [Tempo AI MCP Server] Client transport closed
```

3. Restart Claude Desktop.

### 2. Use the MCP server with Claude

Once the server is running and Claude Desktop is configured, you can use the following tools to ask questions about your past and future activities, events, and wellness data.

- `get_workouts`: List workouts
- `get_workout_details`: Get workout details
- `get_wellness`: List wellness data
- `get_events`: List events
- `get_event_details`: Get event details

## Usage with ChatGPT

ChatGPT’s beta MCP connectors can also talk to this server over the SSE transport.

1. Start the server in SSE mode so it exposes the `/sse` and `/messages/` endpoints:

   ```bash
   export FASTMCP_HOST=127.0.0.1 FASTMCP_PORT=8765 MCP_TRANSPORT=sse FASTMCP_LOG_LEVEL=INFO
   python src/tempoai_mcp_server/server.py
   ```

   The startup log prints the full URLs (for example `http://127.0.0.1:8765/sse`). ChatGPT needs that public URL, so forward the port with a tool such as `ngrok http 8765` if you are not exposing the server directly.

2. In ChatGPT, open **Settings → Features → Custom MCP Connectors** and click **Add**. Fill in:
   - **Name**: `TempoAI`
   - **MCP Server URL**: `https://<your-public-host>/sse`
   - **Authentication**: leave as *No authentication* unless you have protected your tunnel.

   You can reuse the same `ngrok http 8765` tunnel URL here; just ensure it forwards to the host/port you exported above.

3. Save the connector and open a new chat. ChatGPT will keep the SSE connection open and POST follow-up requests to the `/messages/` endpoint announced by the server. If you restart the MCP server or tunnel, rerun the SSE command and update the connector URL if it changes.

## Development and testing

Install development dependencies and run the test suite with:

```bash
uv sync --all-extras
pytest -v tests
```

### Running the server locally

To start the server manually (useful when developing or testing), run:

```bash
mcp run src/tempoai_mcp_server/server.py
```

## License

The GNU General Public License v3.0
