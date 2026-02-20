# mcp-onboarder

CLI для быстрого подключения MCP-серверов в `mcporter`:
- проверка зависимостей (`uv`, `mcporter`, `python`)
- добавление сервера по готовому шаблону
- генерация `.env` шаблона для авторизации
- запуск проверки схемы инструмента (`mcporter list <server> --schema`)

## MVP (сейчас)
Поддерживаемые шаблоны:
- `telegram-mcp` (stdio через `uv run main.py`)
- `hyperliquid-info` (read-only)
- `nocodb` (через `nocodb-mcp-server`)
- `mcp-filesystem`, `mcp-github`, `mcp-postgres`, `mcp-memory`
- `mcp-brave-search`, `mcp-slack`, `mcp-sequential-thinking`, `mcp-pdf`, `mcp-everything`
- `rentahuman` (`npx -y rentahuman-mcp` + `RENTAHUMAN_API_KEY`)
- `custom-stdio` (для любого кастомного MCP)

## Установка

```bash
cd mcp-onboarder
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Использование

### 1) Проверка окружения
```bash
mcp-onboarder doctor
```

### 2) Посмотреть доступные шаблоны
```bash
mcp-onboarder templates
```

### 3) Сгенерировать `.env` пример
```bash
mcp-onboarder env-template telegram-mcp --output /path/to/project/.env
```

### 4) Подключить сервер в `mcporter`
```bash
mcp-onboarder add telegram-mcp \
  --project-dir /Users/you/PycharmProjects/telegram-mcp \
  --name telegram-mcp
```

### 5) Проверить, что инструменты поднялись
```bash
mcp-onboarder verify telegram-mcp
```

### NocoDB: получить ссылку на проект
```bash
mcp-onboarder nocodb-link \
  --url https://app.nocodb.com \
  --workspace-id w4aizska \
  --project-id prnmw7npcrg2zzh
```

### NocoDB: создать API token (через meta API)
```bash
mcp-onboarder nocodb-create-token \
  --url https://app.nocodb.com \
  --project-id prnmw7npcrg2zzh \
  --xc-token <YOUR_XC_TOKEN> \
  --name mcp-onboarder
```

## Примечание по авторизации

`mcp-onboarder` не хранит секреты сам — ты заполняешь `.env` в проекте MCP (или передаёшь env через конфиг), после чего CLI только подключает сервер и проверяет его доступность.
