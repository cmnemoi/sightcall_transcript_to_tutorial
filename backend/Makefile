all: setup-env-variables install check test 

check: check-format check-lint check-types

check-format:
	uv run ruff format . --diff

check-lint:
	uv run ruff check .

check-types:
	uv run mypy .

install:
	uv lock --locked
	uv sync --locked --group dev --group lint --group test

lint:
	uv run ruff format .
	uv run ruff check . --fix

test:
	uv run pytest -v --cov=sightcall_transcript_to_tutorial --cov-report=xml

upgrade-dependencies:
	uv lock --upgrade

.PHONY: setup-env-variables
setup-env-variables:
	cp .env.example .env

.PHONY: all check check-format check-lint check-types install lint test upgrade-dependencies