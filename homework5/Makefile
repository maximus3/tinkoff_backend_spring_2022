CODE = app config database
CODE_FORMAT = $(CODE) tests

VENV = .venv
ifeq ($(OS),Windows_NT)
	PYTHON_EXECUTABLE = python
	VENV_BIN = $(VENV)/Scripts
else
    PYTHON_EXECUTABLE = python3
    VENV_BIN = $(VENV)/bin
endif

POETRY_VERSION=1.1.13
POETRY_RUN = poetry run

TEST = $(POETRY_RUN) pytest --verbosity=2 --showlocals --log-level=DEBUG


.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: venv
venv: ## Create virtual environment, no need in docker
	$(PYTHON_EXECUTABLE) -m venv $(VENV)
	$(VENV_BIN)/python -m pip install --upgrade pip
	$(VENV_BIN)/python -m pip install poetry==$(POETRY_VERSION)
	$(VENV_BIN)/poetry config virtualenvs.create true
	$(VENV_BIN)/poetry config virtualenvs.in-project true
	$(VENV_BIN)/poetry install --no-interaction --no-ansi

.PHONY: install
install: ## Install dependencies
	poetry install --no-interaction --no-ansi

.PHONY: up
up: ## Run App
	$(POETRY_RUN) python -m app

.PHONY: test
test: ## Runs pytest with coverage
	$(TEST) --cov

.PHONY: test-fast
test-fast: ## Runs pytest with exitfirst
	$(TEST) --exitfirst

.PHONY: test-failed
test-failed: ## Runs pytest from last-failed
	$(TEST) --last-failed

.PHONY: test-cov
test-cov: ## Runs pytest with coverage report
	$(TEST) --cov --cov-report html

.PHONY: format
format: ## Formats all files
	$(POETRY_RUN) autoflake --recursive --in-place --remove-all-unused-imports $(CODE_FORMAT)
	$(POETRY_RUN) isort $(CODE_FORMAT)
	$(POETRY_RUN) black --line-length 79 --target-version py39 --skip-string-normalization $(CODE_FORMAT)
	$(POETRY_RUN) unify --in-place --recursive $(CODE_FORMAT)

.PHONY: lint
lint: ## Lint code
	$(POETRY_RUN) flake8 --jobs 4 --statistics --show-source $(CODE)
	$(POETRY_RUN) pylint --rcfile=setup.cfg $(CODE)
	$(POETRY_RUN) mypy $(CODE)
	$(POETRY_RUN) black --line-length 79 --target-version py39 --skip-string-normalization --check $(CODE)
	$(POETRY_RUN) pytest --dead-fixtures --dup-fixtures
	$(POETRY_RUN) safety check --full-report

.PHONY: check
check: format lint test ## Format and lint code then run tests

.PHONY: docker-up
docker-up: ## Docker up
	docker-compose up

.PHONY: docker-up-d
docker-up-d: ## Docker up detach
	docker-compose up -d

.PHONY: docker-build
docker-build: ## Docker build
	docker-compose build

.PHONY: docker-down
docker-down: ## Docker down
	docker-compose down

.PHONY: docker-clean
docker-clean: ## Docker prune -f
	docker image prune -f

.PHONY: docker
docker: docker-clean docker-build docker-up docker-clean ## Docker prune, up, run and prune
