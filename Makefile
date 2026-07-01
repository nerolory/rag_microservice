.PHONY: lint format typecheck test check fix install-local run run-local \
	docker-up docker-down docker-logs docker-rebuild docker-clean

lint:
	ruff check app tests

format:
	ruff format app tests

typecheck:
	mypy app

test:
	pytest tests -v

check: lint format typecheck test

fix:
	ruff check --fix app tests
	ruff format app tests

install-local:
	pip install torch --index-url https://download.pytorch.org/whl/cpu
	pip install -e ".[local]"

run:
	python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

run-local: install-local
	python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

docker-up:
	docker compose up -d app

docker-down:
	docker compose down --remove-orphans

docker-test:
	docker compose run --rm test

docker-test-e2e:
	docker compose --profile e2e run --rm -e RUN_E2E_TESTS=1 test-e2e

docker-free-memory:
	powershell -File scripts/docker_free_memory.ps1

docker-rebuild:
	docker compose down --remove-orphans
	docker compose build app
	docker image prune -f
	docker compose up -d app

docker-clean:
	docker compose down --remove-orphans
	docker image prune -f
	docker builder prune -f --filter "until=24h"

docker-logs:
	docker compose logs -f app
