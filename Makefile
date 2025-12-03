.PHONY: help install lint format test run dev clean sync demo

help:
	@echo "Available commands:"
	@echo "  make install    - Install the package in editable mode"
	@echo "  make sync       - Sync dependencies with uv"
	@echo "  make lint       - Run linting checks with ruff"
	@echo "  make format     - Format code with ruff"
	@echo "  make test       - Run tests with pytest"
	@echo "  make demo       - Run mock API demo"
	@echo "  make run        - Run the FastAPI application"
	@echo "  make dev        - Run the app in development mode with auto-reload"
	@echo "  make clean      - Remove Python cache files"

install:
	uv pip install -e .

sync:
	uv sync

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/
	ruff check --fix src/ tests/

test: sync
	pytest tests/ -v

demo-apis: sync
	python examples/demo_apis.py

demo-tools: sync
	python examples/demo_tool_definitions.py

demo-understanding: sync
	python examples/demo_understanding_tools.py

run: sync
	python -m uvicorn concierge.app:app --host 0.0.0.0 --port 8000

dev: sync
	python -m uvicorn concierge.app:app --host 0.0.0.0 --port 8000 --reload

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
