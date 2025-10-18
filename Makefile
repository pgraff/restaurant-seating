.PHONY: help install install-dev test test-cov lint format clean run dev docs docker-up docker-down docker-build migrate

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements-dev.txt
	pre-commit install

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=backend --cov=app --cov-report=html --cov-report=term

lint: ## Run linting
	flake8 backend/ app/
	mypy backend/ app/
	bandit -r backend/ app/

format: ## Format code
	black backend/ app/
	isort backend/ app/

clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

run: ## Run the application
	cd backend && python main.py

dev: ## Run the application in development mode
	cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

docs: ## Build documentation
	mkdocs build

docs-serve: ## Serve documentation locally
	mkdocs serve

check: ## Run all checks (lint, test, format check)
	black --check backend/ app/
	isort --check-only backend/ app/
	flake8 backend/ app/
	mypy backend/ app/
	pytest

docker-up: ## Start Docker services
	docker-compose up -d

docker-down: ## Stop Docker services
	docker-compose down

docker-build: ## Build Docker images
	docker-compose build

docker-logs: ## Show Docker logs
	docker-compose logs -f

migrate: ## Run database migrations
	cd backend && alembic upgrade head

migrate-create: ## Create a new migration
	cd backend && alembic revision --autogenerate -m "$(msg)"

setup: install-dev ## Set up development environment
	@echo "Development environment set up successfully!"
	@echo "Run 'make dev' to start the development server"
