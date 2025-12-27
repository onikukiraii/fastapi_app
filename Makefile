include .env
.EXPORT_ALL_VARIABLES:

.PHONY: migrate migrate-gen

migrate:
	cd backend && uv run alembic upgrade head

migrate-gen:
	@read -p "Migration message: " msg; \
	cd backend && uv run alembic revision --autogenerate -m "$$msg"