from dataclasses import dataclass
from pathlib import Path


@dataclass
class Template:
    key: str
    command: str
    args: list[str]
    env_template: str


def get_templates(project_dir: str) -> dict[str, Template]:
    p = Path(project_dir).expanduser().resolve()
    return {
        # Local/project servers
        "telegram-mcp": Template(
            key="telegram-mcp",
            command="/Users/stepanmulin/.local/bin/uv",
            args=["--directory", str(p), "run", "main.py"],
            env_template=(
                "# Telegram API credentials\n"
                "TELEGRAM_API_ID=\n"
                "TELEGRAM_API_HASH=\n"
                "TELEGRAM_PHONE=\n"
                "TELEGRAM_SESSION_NAME=./telegram_session\n"
            ),
        ),
        "hyperliquid-info": Template(
            key="hyperliquid-info",
            command="/Users/stepanmulin/.local/bin/uv",
            args=["--directory", str(p), "run", "main.py"],
            env_template=(
                "# Usually no auth required for read-only info server\n"
                "# HYPERLIQUID_NETWORK=mainnet\n"
            ),
        ),
        "nocodb": Template(
            key="nocodb",
            command="npx",
            args=["-y", "nocodb-mcp-server", "${NOCODB_URL}", "${NOCODB_PROJECT_ID}", "${NOCODB_API_TOKEN}"],
            env_template=(
                "# NocoDB MCP credentials\n"
                "NOCODB_URL=https://app.nocodb.com\n"
                "NOCODB_PROJECT_ID=\n"
                "NOCODB_API_TOKEN=\n"
                "# Optional workspace id for direct UI links\n"
                "NOCODB_WORKSPACE_ID=\n"
            ),
        ),

        # Official @modelcontextprotocol servers
        "mcp-filesystem": Template(
            key="mcp-filesystem",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", "${MCP_FILESYSTEM_ROOT}"],
            env_template=(
                "# Filesystem root that MCP server can access\n"
                f"MCP_FILESYSTEM_ROOT={str(p)}\n"
            ),
        ),
        "mcp-github": Template(
            key="mcp-github",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
            env_template=(
                "# GitHub Personal Access Token\n"
                "GITHUB_PERSONAL_ACCESS_TOKEN=\n"
            ),
        ),
        "mcp-postgres": Template(
            key="mcp-postgres",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-postgres", "${POSTGRES_URL}"],
            env_template=(
                "# Example: postgresql://user:pass@host:5432/dbname\n"
                "POSTGRES_URL=\n"
            ),
        ),
        "mcp-memory": Template(
            key="mcp-memory",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-memory"],
            env_template=(
                "# Optional memory storage path\n"
                "# MEMORY_FILE_PATH=./memory.json\n"
            ),
        ),
        "mcp-brave-search": Template(
            key="mcp-brave-search",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-brave-search"],
            env_template=(
                "# Brave API key\n"
                "BRAVE_API_KEY=\n"
            ),
        ),
        "mcp-slack": Template(
            key="mcp-slack",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-slack"],
            env_template=(
                "# Slack bot token + app token\n"
                "SLACK_BOT_TOKEN=\n"
                "SLACK_APP_TOKEN=\n"
            ),
        ),
        "mcp-sequential-thinking": Template(
            key="mcp-sequential-thinking",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-sequential-thinking"],
            env_template="# No extra env required\n",
        ),
        "mcp-pdf": Template(
            key="mcp-pdf",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-pdf"],
            env_template="# No extra env required\n",
        ),
        "mcp-everything": Template(
            key="mcp-everything",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-everything"],
            env_template="# Dev/testing server\n",
        ),

        # Catch-all custom template (including HumanRent/custom MCP)
        "custom-stdio": Template(
            key="custom-stdio",
            command="${MCP_COMMAND}",
            args=["${MCP_ARG1}", "${MCP_ARG2}", "${MCP_ARG3}"],
            env_template=(
                "# Put your custom MCP server command/args here\n"
                "MCP_COMMAND=\n"
                "MCP_ARG1=\n"
                "MCP_ARG2=\n"
                "MCP_ARG3=\n"
            ),
        ),
    }
