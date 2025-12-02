#!/usr/bin/env bash
#
# Tempo AI MCP Server Installer
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/mvilanova/tempoai-mcp-server/main/install.sh | bash
#
# This script will:
#   1. Install uv package manager if not present
#   2. Clone the repository to ~/.tempoai-mcp-server
#   3. Set up Python 3.13 virtual environment
#   4. Install dependencies
#   5. Prompt for API key
#   6. Configure Claude Desktop
#
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

INSTALL_DIR="${HOME}/.tempoai-mcp-server"
REPO_URL="https://github.com/mvilanova/tempoai-mcp-server.git"

echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           Tempo AI MCP Server Installer                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check for git
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: git is required but not installed.${NC}"
    echo "Please install git first: https://git-scm.com/downloads"
    exit 1
fi

# On macOS, verify Xcode Command Line Tools are installed
if [[ "$OSTYPE" == "darwin"* ]]; then
    if ! xcode-select -p &> /dev/null; then
        echo -e "${YELLOW}📦 Installing Xcode Command Line Tools (required for git)...${NC}"
        echo "A dialog will appear - please click 'Install' and wait for it to complete."
        xcode-select --install
        echo ""
        echo -e "${YELLOW}After installation completes, please run this script again.${NC}"
        exit 0
    fi
fi

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}📦 Installing uv package manager...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Add uv to PATH for this session (installed to ~/.local/bin)
    export PATH="$HOME/.local/bin:$PATH"
    echo -e "${GREEN}✓ uv installed successfully${NC}"
else
    echo -e "${GREEN}✓ uv is already installed${NC}"
fi

# Clone or update repository
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}📥 Updating existing installation...${NC}"
    cd "$INSTALL_DIR"

    # Check for local modifications that would block the update
    if ! git diff --quiet HEAD 2>/dev/null || [ -n "$(git ls-files --others --exclude-standard)" ]; then
        echo -e "${RED}Error: Local modifications detected in ${INSTALL_DIR}${NC}"
        echo ""
        echo "To preserve your changes, run:"
        echo -e "  ${BLUE}cd ${INSTALL_DIR} && git stash && git pull && git stash pop${NC}"
        echo ""
        echo "To discard your changes and update, run:"
        echo -e "  ${BLUE}cd ${INSTALL_DIR} && git reset --hard HEAD && git clean -fd && git pull${NC}"
        echo ""
        exit 1
    fi

    git pull origin main
    echo -e "${GREEN}✓ Repository updated${NC}"
else
    echo -e "${YELLOW}📥 Cloning repository...${NC}"
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
    echo -e "${GREEN}✓ Repository cloned${NC}"
fi

# Create virtual environment and sync dependencies
echo -e "${YELLOW}🐍 Setting up Python 3.13 environment...${NC}"
uv venv --python 3.13 --quiet
. .venv/bin/activate
uv sync --quiet
echo -e "${GREEN}✓ Python environment ready${NC}"

# Prompt for API key (skip if already configured)
if [ -f ".env" ] && grep -qE "API_KEY=.+" .env; then
    echo -e "${GREEN}✓ API key already configured${NC}"
    echo -e "  (To update your API key, edit ${INSTALL_DIR}/.env)"
else
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}🔑 API Key Setup${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "To get your API key:"
    echo "  1. Log in at https://jointempo.ai/signin"
    echo "  2. Go to Settings > Developer"
    echo "  3. Generate a new API key"
    echo ""
    read -s -p "Enter your Tempo AI API key: " API_KEY < /dev/tty
    echo

    if [ -z "$API_KEY" ]; then
        echo -e "${RED}Error: API key is required.${NC}"
        exit 1
    fi

    # Create .env file
    echo "API_KEY=${API_KEY}" > .env
    chmod 600 .env
    echo -e "${GREEN}✓ Environment configured${NC}"
fi

# Verify the server can be imported successfully
echo -e "${YELLOW}🔍 Verifying installation...${NC}"
if ! python -c "from tempoai_mcp_server.server import mcp" 2>/dev/null; then
    echo -e "${RED}Error: Server module failed to import. Please check for missing dependencies.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Server module verified${NC}"

# Configure Claude Desktop
echo -e "${YELLOW}🔧 Configuring Claude Desktop...${NC}"
if ! command -v mcp >/dev/null 2>&1; then
    echo -e "${RED}Error: 'mcp' command not found. Please ensure MCP is installed and available in your PATH.${NC}"
    exit 1
fi
if ! mcp install src/tempoai_mcp_server/server.py --name "TempoAI" --with-editable . --env-file .env; then
    echo -e "${RED}Error: Failed to configure Claude Desktop with MCP. Please check the output above for details.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Claude Desktop configured${NC}"

# Success message
echo ""
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                   Installation Complete!                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""
echo "Next steps:"
echo "  1. Restart Claude Desktop"
echo "  2. Start a new conversation and ask about your workouts!"
echo ""
echo -e "Installation location: ${YELLOW}${INSTALL_DIR}${NC}"
echo ""
echo "To update later, run this same command again or:"
echo -e "  ${BLUE}cd ${INSTALL_DIR} && git pull && uv sync && source .venv/bin/activate && mcp install src/tempoai_mcp_server/server.py --name TempoAI --with-editable . --env-file .env${NC}"
echo ""
echo "To uninstall:"
echo -e "  ${BLUE}rm -rf ${INSTALL_DIR}${NC}"
echo "  Then remove the 'TempoAI' entry from your Claude Desktop config file."
echo ""
