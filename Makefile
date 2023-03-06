setup:
	@echo "Installing dependencies..."
	poetry install
	@echo "Set-up pre-commit hooks..."
	poetry run pre-commit install
	@echo "Pull data from DVC..."
	poetry run dvc pull
	@echo "Activating virtual environment..."
	poetry shell

dvc_check:
	[ -d ./.dvc ] && poetry run dvc status || dvc init

docs_view:
	@echo View API documentation...
	pdoc src/. --http localhost:8080

docs_build:
	@echo Build API documentation...
	pdoc src/. --output-dir docs/api

## Delete all compiled Python files
clean:
	@echo "Clean compiled Python files..."
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache

run_pipeline:
	@echo "Run pipeline..."
	poetry run python src/pipeline.py
