.PHONY: install update test test-linting test-flake8 test-pycodestyle test-pylint test-bandit test-mypy test-pytest test-additional clean publish

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

test-linting: test-flake8 test-pycodestyle test-pylint test-bandit test-mypy

test-flake8 flake8:
	@printf "Running flake8 tests\n+++++++++++++++++++++++++++\n"
	poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	poetry run flake8 . --count --ignore=W391,W503,F541 --max-complexity=20 --max-line-length=127 --statistics
	@printf "\n\n"

test-pycodestyle:
	@printf "Running pycodestyle tests\n+++++++++++++++++++++++++++\n"
	pycodestyle --ignore=E501,W191,W293,E302,W291,W292,E126,E265,E226,E262,E261,W391,E121,E123,E712,E231,W605,W504,W503 pyaurorax
	pycodestyle --ignore=E501,W191,W293,E302,W291,W292,E126,E265,E226,E262,E261,W391,E121,E123,E712,E231,W605,W504,W503 tools
	@printf "\n\n"

test-pylint pylint:
	@printf "Running pylint tests\n+++++++++++++++++++++++++++\n"
	poetry run pylint pyaurorax
	@printf "\n\n"

test-bandit bandit:
	@printf "Running bandit tests\n+++++++++++++++++++++++++++\n"
	poetry run bandit -r pyaurorax
	@printf "\n\n"

test-mypy:
	@printf "Running mypy tests\n+++++++++++++++++++++++++++\n"
	poetry run mypy --ignore-missing-imports --no-strict-optional pyaurorax
	@printf "\n\n"

test-pytest pytest:
	@printf "Running pytest tests\n+++++++++++++++++++++++++++\n"
	poetry run pytest -v
	@printf "\n\n"

test-pytest-unauthorized-access:
	poetry run pytest -v -k "test_AuroraXUnauthorizedException"

test-pytest-read:
	poetry run pytest -v -k "not test_AuroraXUnauthorizedException and not add and not upload and not update and not delete"

test-pytest-create-update-delete:
	poetry run pytest -v -k "add or upload or update or delete"

test-additional:
	@echo "Test coverage ...\n============================="
	-poetry run coverage report

publish:
	poetry build
	poetry publish
	${MAKE} clean
