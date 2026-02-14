[tool.poetry]
name = "magician-system"
version = "0.1.0"
description = ""
authors = ["You <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "0.109.0"
uvicorn = { version = "0.27.0", extras = ["standard"] }
pydantic = "2.5.3"
python-multipart = "0.0.6"
pyyaml = "6.0.1"
requests = "2.31.0"
aiohttp = "3.9.2"
asyncio = "3.4.3"
python-dotenv = "1.0.0"

[tool.poetry.dev-dependencies]
pytest = "7.4.3"
pytest-asyncio = "0.21.1"
pytest-cov = "4.1.0"
httpx = "0.26.0"
