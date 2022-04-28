CODE = app.py main tests
TEST = poetry run pytest --verbosity=2 --showlocals --log-level=DEBUG --strict-markers $(arg) -k "$(k)"

.PHONY: install
install: ## Install dependencies
	poetry install --no-interaction --no-ansi

.PHONY: up
up: ## Run Flask
	poetry run flask run

.PHONY: test
test: ## Runs pytest with coverage
	$(TEST) --cov=main

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
	poetry run autoflake --recursive --in-place --remove-all-unused-imports $(CODE)
	poetry run isort $(CODE)
	poetry run black --line-length 79 --target-version py39 --skip-string-normalization $(CODE)
	poetry run unify --in-place --recursive $(CODE)

.PHONY: lint
lint: ## Lint code
	poetry run flake8 --jobs 4 --statistics --show-source $(CODE)
	poetry run pylint --rcfile=setup.cfg $(CODE)
	poetry run mypy $(CODE)
	poetry run black --line-length 79 --target-version py39 --skip-string-normalization --check $(CODE)
	poetry run pytest --dead-fixtures --dup-fixtures
	poetry run safety check --full-report

.PHONY: check
check: format lint test ## Format and lint code then run tests