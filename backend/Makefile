all: setup-env-variables install check test 

check: check-format check-lint check-types

check-format:
	uv run ruff format . --diff

check-lint:
	uv run ruff check .

check-types:
	uv run mypy . --exclude=tests

.PHONY: db-diff
db-diff:
	docker compose exec backend python -m alembic revision --autogenerate -m "Update DB schema"

install:
	uv lock --locked
	uv sync --locked --group dev --group lint --group test

lint:
	uv run ruff format .
	uv run ruff check . --fix

.PHONY: migrate-up
migrate-up:
	docker compose exec backend python -m alembic upgrade head

.PHONY: migrate-down
migrate-down:
	docker compose exec backend python -m alembic downgrade -1

.PHONY: setup-env-variables
setup-env-variables:
	cp .env.example .env

test:
	uv run pytest -v --cov=sightcall_transcript_to_tutorial --cov-report=xml tests/unit tests/integration tests/e2e

upgrade-dependencies:
	uv lock --upgrade

.PHONY: all check check-format check-lint check-types install lint test upgrade-dependencies