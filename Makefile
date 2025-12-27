.PHONY: migrate migrate-gen

migrate:
	cd backend && uv run alembic upgrade head

migrate-gen:
	cd backend && uv run alembic revision --autogenerate