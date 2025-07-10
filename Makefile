.PHONY: help install test lint format security build clean docs serve-docs release-check

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install package in development mode
	pip install -e .
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -e .
	pip install pytest pytest-cov ruff bandit mypy build twine
	pip install mkdocs mkdocs-material mkdocstrings[python] mkdocs-jupyter

test: ## Run tests
	pytest tests/ -v

test-cov: ## Run tests with coverage
	pytest tests/ -v --cov=pydipapi --cov-report=html --cov-report=term-missing

lint: ## Run linting checks
	ruff check .

format: ## Format code
	ruff format .

format-check: ## Check code formatting
	ruff format --check .

security: ## Run security checks
	bandit -r pydipapi/ -f json -o bandit-report.json

typecheck: ## Run type checking
	mypy pydipapi/ --ignore-missing-imports

quality: lint format-check security typecheck ## Run all quality checks

build: ## Build package
	python -m build

build-check: ## Build and check package
	python -m build
	python -m twine check dist/*

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf bandit-report.json
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs: ## Build documentation
	mkdocs build

serve-docs: ## Serve documentation locally
	mkdocs serve

docs-check: ## Build docs and check for warnings
	mkdocs build --strict

release-check: clean quality test build-check docs-check ## Complete release validation
	@echo "✅ All checks passed! Ready for release."

dev-setup: install-dev ## Setup development environment
	pre-commit install
	@echo "✅ Development environment ready!"

# Git helpers
tag-version: ## Create and push version tag (usage: make tag-version VERSION=v1.0.0)
ifndef VERSION
	$(error VERSION is required. Usage: make tag-version VERSION=v1.0.0)
endif
	git tag $(VERSION)
	git push origin $(VERSION)
	@echo "✅ Tag $(VERSION) created and pushed!"

# CI simulation
ci-local: quality test build-check docs-check ## Simulate CI pipeline locally
	@echo "✅ Local CI simulation completed successfully!" 