SHELL := /bin/bash
.ONESHELL:

PY := python3.11
PIP := pip

.DEFAULT_GOAL := help

.PHONY: help venv setup fmt lint type test up down logs

help:
	@echo "Targets: setup, venv, fmt, lint, type, test, up, down, logs"

venv:
	@command -v python3 >/dev/null 2>&1 || { echo "Python3 not found"; exit 1; }
	@python3 -m venv .venv || python3 -m virtualenv .venv
	@. .venv/bin/activate && $(PIP) install -U pip

setup: venv
	@. .venv/bin/activate && pip install fastapi uvicorn pydantic httpx streamlit qdrant-client pymongo psycopg2-binary sentence-transformers langfuse python-dotenv
	@. .venv/bin/activate && pip install ruff black isort mypy pytest pytest-asyncio bandit pre-commit
	@echo "✓ Setup complete! Activate with: source .venv/bin/activate"

fmt:
	@. .venv/bin/activate && ruff check --fix . || true
	@. .venv/bin/activate && black .
	@. .venv/bin/activate && isort .

lint:
	@. .venv/bin/activate && ruff check .

type:
	@. .venv/bin/activate && mypy apps services

test:
	@. .venv/bin/activate && pytest -q

up:
	cd infra/compose && docker compose up -d

down:
	cd infra/compose && docker compose down -v

logs:
	cd infra/compose && docker compose logs -f --tail=200
