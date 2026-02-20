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
    }
