# refactor-notebooks

## Set-up the repo

1. **Version Control**: Init the git repo
2. **Dependencies**:Can reuse existing environment: `conda activate analytics-training-samples`
3. **Data**: Set-up `dvc`
    - Create folder `data/01_raw`: Put the data there
    - `dvc init`
    - Set up remote storage: `dvc remote add -d storage gs://dvc-data-storage` (separate steps to set-up Google Storage and connect local machine to GCP)
    - Turn on autostaging: `dvc config core.autostage true`
    - `dvc add data/01_raw/online_retail.xlsx`
    - `dvc push`


## Overview about the refactoring process
![](./image/refactor-notebook-diagram.webp)


## Converting notebook

> Convert the notebook to script

1. Example notebook: `notebooks/Original_OnlineRetail_Cohort.ipynb`
2. Make a copy: `notebooks/Original_OnlineRetail_Cohort-Copy1.ipynb`
3. On Jupyter notebook:
    - Cell -> All Output -> Clear
    - Run All (To make sure that all cells are in right sequence)
    - Check all results
4. On Terminal, run:
```
jupyter nbconvert notebooks/Original_OnlineRetail_Cohort-Copy1.ipynb --to python
```
5. Check the script output, remove all print/notebook statements: `print(...)`, `df.head()`, `df.describe(...)`, etc.


## Identify code smells

> Read through the code, sketch out the flow, list any code smells

1. Sketch out the flow
    - Ingest & process data
    - Aggregate to have the data input for plotting
    - Plotting the reports
2. List code smells & [Clean code](https://github.com/davified/clean-code-ml) enhancements
3. Leave `# TODO` comments for things to change


## Write / Test / Local module

> Convert codes into DRY functions, write tests, and create local module (which could be imported to notebooks)

1. Create the `src` folder to keep all source codes
2. Create `tests` folder to keep tests for source codes
3. Write/Test follows the Test-driven Development (TDD) approach
    - `tests/test_*.py`: Write the test first, then write the code
    - `pytest`: Run the test, make sure it fails
    - Write the code, make sure it passes
    - Refactor the code, make sure it still passes
4. Structures within source code:
    - `src/`: All source codes
        - `__init__.py`: Empty file to make `src` a module
        - `utils.py`: Utility functions
        - `ingest.py`: All functions to process/clean data
        - `process.py`: All functions to aggregate data
        - `plot.py`: All functions to plot data
    - `tests/`: All tests
        - `__init__.py`: Empty file to make `tests` a module
        - `test_utils.py`: Utility functions for tests
        - `test_ingest.py`: Test for `ingest.py`
        - `test_process.py`: Test for `process.py`
        - `test_plot.py`: Test for `plot.py`
    - Within each test file:
        - Import the functions from local modules (`src` folder)
        - Tests for each function could be organized by `Class` with each test cases as methods (naming corresponding to the function name)
5. Write the code until passing the tests
6. Reformat with `black`
7. Commit to git
8. Pull request to merge to `main` branch

## Import and use new functions on notebook

We refactor codes from the Original noteboks as local modules, and import them to the new notebooks. This will enforce the TDD approach, and reusable of functions across notebooks.

If you reuse local module a lot, consider to convert them to proper Python pkg with `pip` manager

> See: `notebooks/Refactored_OnlineRetail_Cohort.ipynb`


# Other topics
## Structure a DS project

After refactoring the notebook into a project with structured and scripts, we could use further tools to support our work even more conveniently.

- `Poetry`: Python dependency management tool (alternative to pip)
- `Hydra`: Python config management tool (manage parameters of all data pipelines, manage the catalog of data path)
- `pdoc`: Python documentation generator (generate documentation from source code)
- `pre-commit`: Python pre-commit hooks (automate code formatting, linting, testing, etc)
- `Makefile`: Python Makefile (automate the workflow)

## Poetry

- Python dependency management tool (alternative to pip)
    - Separate main dependencies and sub-dependencies
    - Remove unused sub-dependencies
    - Avoid installing new packages conflicts with existing one
    - Package your project in several lines of code

### Install

Install `poetry`: [https://python-poetry.org/docs/](https://python-poetry.org/docs/)

In Linux, Mac:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Add `export PATH="/Users/anhdang/.local/bin:$PATH"` to your shell configuration file.

1. Open the shell config file: `open ~/.bash_profile`
2. Add the line `export PATH="/Users/anhdang/.local/bin:$PATH"`
3. Run the config: `source ~/.bash_profile`
4. Test: `poetry --version`

### Usages

> You have know about `requirements.txt` and `pip install -r src/requirements.txt` as one way to manage the dependencies. Now, we will introduce a relatively “better” tool to handle it
>

#### New repo

1. Init poetry: `poetry init`, this will create file `pyproject.toml` (main dependencies file, in replace for `requirements.txt`
2. Follow an interactive step-by-step

#### Repo with existing poetry

1. `poetry install` (install every dependencies in `pyproject.toml`
2. Add new library: `poetry add <name-of-pkg>` (install and update the dependencies file)
3. Remove: `poetry remove <name-of-pkg>`
4. Can use as the virtual env (similar to conda): `poetry shell` (auto detect the `pyproject.toml`)

## Hydra

> Hydra is the python framework that enable us to manage the config files. [https://hydra.cc/docs/intro/](https://hydra.cc/docs/intro/)
>

**Use case**: Now, we will combine all steps (python functions) into 1 pipeline, with parameters centralized in a config `YAML` file, and the whole pipeline could be run as a python script.

1. Install: `poetry add hydra-core`
2. On the repo create: `config/pipeline.yaml`

```bash
raw:
  path: data/01_raw/online_retail.xlsx

processed:
  path: data/02_processed/clean_retail.csv
  config:
    null_cols:
      - 'CustomerID'
    outlier_policies:
      UnitPrice: [0, 10]
      Quantity: [0, 50]
```

1. Create the python script: `src/pipeline.py`

```bash
"""This is the demo pipeline, that collect
all scripts and combine with config file to run the pipeline."""
import hydra
from omegaconf import DictConfig
from hydra.utils import to_absolute_path as abspath
import pandas as pd
from src.ingest import process_data # Import steps from ingest
import os

@hydra.main(config_path="../config", config_name="pipeline")
def run_pipeline(config: DictConfig):
    """This is the demo pipeline, that collect all scripts and combine with config file to run the pipeline.
    TO use:
    - Modify the config file in config/pipeline.yaml
    - Run the pipeline with command: python src/pipeline.py
    - This file is supposed run as script, not import to other scripts
    """
    raw_data_path = abspath(config.raw.path)
    processed_data_path = abspath(config.processed.path)
    process_config = config.processed.config

    print(f'Loading raw data from: {raw_data_path}')
    # TODO: feed the configs loaded by hydra into process_data function
    # YOUR-CODE-HERE

    # If not exist, create
    if not os.path.exists(os.path.dirname(processed_data_path)):
        os.makedirs(os.path.dirname(processed_data_path))

    # Write output
    df.to_csv(processed_data_path, index=False)
    print(f'Write output data to: {raw_data_path}')

# This is the block to make sure that this file is run as a script
# rather than import to other scripts
if __name__ == "__main__":
    run_pipeline()
```

1. Run the script: `python src/pipeline.py` (Be prepare for any issue, try to solve it!)
2. Once you run it successfully, the new output csv should be in `02_processed/clean_retail.csv`
3. Hydra generate the folder `outputs/` to store all logs, and settings of each run → Put it into the `.gitignore`
4. New outputs add it to `dvc`

```bash
dvc add data/02_processed/clean_retail.csv
```

## pdoc

> `pdoc` auto-generates API documentation that follows your project's Python module hierarchy
>
1. `poetry add pdoc`
2. Open the API docs on [localhost](http://localhost) browser: `pdoc src/.`
3. Output to the `/docs` as html file: `pdoc src/. -o docs`


## Pre-commit hook

> Source: [https://www.architecture-performance.fr/ap_blog/some-pre-commit-git-hooks-for-python/](https://www.architecture-performance.fr/ap_blog/some-pre-commit-git-hooks-for-python/)
>

Tools to help auto double-check and clean code before commit to git.

1. Install: `poetry add pre-commit`
2. Check: `pre-comit --version`
3. Create in the repo file: `.pre-commit-config.yaml`, this file will keep the “checklist” before allowing you to commit to git

```yaml
repos:
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v3.2.0
  hooks:
  - id: trailing-whitespace
  - id: end-of-file-fixer
  - id: check-added-large-files
  - id: detect-private-key
- repo: https://github.com/psf/black
  rev: 22.10.0
  hooks:
  - id: black
- repo: https://github.com/hadialqattan/pycln
  rev: v0.0.1-beta.3
  hooks:
  - id: pycln
    args: [--config=pyproject.toml]
- repo: https://github.com/pycqa/isort
  rev: 5.5.4
  hooks:
  - id: isort
    files: "\\.(py)$"
    args: [--settings-path=pyproject.toml]
```

1. Further config the settings of this tool in `pyproject.toml` (created before by `poetry`)

```toml
[tool.black]
line-length = 79

[tool.pycln]
all = true

[tool.isort]
line_length = 79
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
```

1. Check its effect: `pre-commit run --all-files` (check if everything satisfied the checklist)
2. “Register” the hook into git (whenever you run `git commit`, the hook of pre-commit checks will be triggered: `pre-commit install`
3. Now, try create some “dirty” format code, and `git commit` (If it fails any check, it would be corrected, but you need to run the commit again)

```toml
git status
git add .
git commit -m "Some message"
```

## Makefile

> We use `Makefile`to power up the ML project CLI usage, and provide some handy CLI for anyone to access/reuse the repo
>

Create the `Makefile` put this:

```toml
setup:
	@echo "Installing dependencies..."
	poetry install
	@echo "Set-up pre-commit hooks..."
	poetry run pre-commit install
	@echo "Pull data from DVC..."
	poetry run dvc pull

dvc_check:
	[ -d ./.dvc ] && poetry run dvc status || dvc init

activate_venv:
	@echo "Activating virtual environment..."
	poetry shell

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

pipeline:
	@echo "Run pipeline..."
	poetry run python src/pipeline.py
```

Then, try to run:

1. `make activate_venv`
2. `make docs_view`
3. `make pipeline`
