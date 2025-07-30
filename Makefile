run:
	uv run --env-file .env main.py

sync:
	uv sync

lint:
	uv run ruff check