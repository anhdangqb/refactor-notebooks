init_setup:
	@echo "Install poetry"
	curl -sSL https://install.python-poetry.org | python3 -
	@echo "Test poetry install succesfully"
	poetry --version
	@echo "Installing dependencies..."
	poetry install
	@echo "Set-up pre-commit hooks..."
	poetry run pre-commit install
	@echo "Set-up gcp project"
	gcloud auth application-default set-quota-project analytics-training-hub
	@echo "Pull data from DVC..."
	poetry run dvc pull
	@echo "Activating virtual environment..."
	poetry shell

gcloud_setup:
	@echo "Download gcloud cli. When finish, please start a new Terminal"
	curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-420.0.0-linux-x86_64.tar.gz
	@echo "Unzip gcloud cli"
	tar -xf google-cloud-cli-420.0.0-linux-x86_64.tar.gz
	@echo "Install gcloud"
	./google-cloud-sdk/install.sh

gcloud_auth:
	@echo "Set up GCP auth"
	gcloud auth application-default login --no-launch-browser

dvc_check:
	[ -d ./.dvc ] && poetry run dvc status || dvc init

docs_view:
	@echo View API documentation...
	pdoc src/. 

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
