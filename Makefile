.PHONY: install update test test-linting test-flake8 test-pylint test-bandit test-pytest test-additional clean publish

all:

poetry:
	python -m pip install poetry

install: poetry
	poetry install

update upgrade:
	python -m pip install --upgrade poetry
	poetry update

clean:
	@rm -rf pyaurorax.egg-info build dist

test: test-linting test-pytest

test-linting: test-flake8 test-pylint test-bandit

test-flake8 flake8:
	poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	poetry run flake8 . --count --ignore=W391,W503 --max-complexity=20 --max-line-length=127 --statistics
	
test-pylint pylint:
	poetry run pylint pyaurorax

test-bandit bandit:
	poetry run bandit -r pyaurorax

test-pytest pytest:
	poetry run pytest -v

test-pytest-unauthorized-access:
	poetry run pytest -v -k "test_AuroraXUnauthorizedException"

test-pytest-read:
	poetry run pytest -v -k "not test_AuroraXUnauthorizedException and not add and not upload and not update and not delete"

test-pytest-create-update-delete:
	poetry run pytest -v -k "add or upload or update or delete"

test-additional:
	@echo "Type-checking ...\n============================="
	-poetry run mypy pyaurorax
	@echo "\n\n"
	@echo "Test coverage ...\n============================="
	-poetry run coverage report

publish:
	poetry build
	poetry publish
	${MAKE} clean
