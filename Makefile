.PHONY: install test test-unit test-integration coverage clean lint all

install:
	pip install -r requirements.txt

test:
	pytest

test-unit:
	pytest -m "not integration"

test-integration:
	pytest -m integration

coverage:
	pytest --cov=src/task_manager --cov-report=html --cov-report=term-missing

clean:
	rm -rf __pycache__ .pytest_cache htmlcov .coverage
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

lint:
	python -m py_compile src/task_manager/*.py
	python -m py_compile tests/*.py

all: install lint test coverage