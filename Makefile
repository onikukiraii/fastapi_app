include .env
.EXPORT_ALL_VARIABLES:

.PHONY: migrate migrate-gen lint format

migrate:
	cd backend && uv run alembic upgrade head

migrate-gen:
	@read -p "Migration message: " msg; \
	cd backend && uv run alembic revision --autogenerate -m "$$msg"

lint:
	cd backend && uv run ruff check . && uv run ruff format --check . && uv run mypy .

format:
	cd backend && uv run ruff check --fix . && uv run ruff format .