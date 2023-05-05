.PHONY: install update test test-linting test-flake8 test-pycodestyle test-pylint test-bandit test-mypy test-pytest test-coverage docs publish

all:

poetry:
	python -m pip install poetry

install: poetry
	poetry install -E aacgmv2

update upgrade:
	python -m pip install --upgrade poetry
	poetry update

test test-linting: test-flake8 test-pycodestyle test-pylint test-bandit test-mypy

test-all: test-linting test-pytest

test-flake8 flake8:
	@printf "Running flake8 tests\n+++++++++++++++++++++++++++\n"
	poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	poetry run flake8 . --count --ignore=W391,W503,F541,W504 --max-complexity=30 --max-line-length=129 --statistics
	@printf "\n\n"

test-pycodestyle:
	@printf "Running pycodestyle tests\n+++++++++++++++++++++++++++\n"
	poetry run pycodestyle --ignore=E501,W191,W293,E302,W291,W292,E126,E265,E226,E262,E261,W391,E121,E123,E712,E231,W605,W504,W503,E402 pyaurorax
	poetry run pycodestyle --ignore=E501,W191,W293,E302,W291,W292,E126,E265,E226,E262,E261,W391,E121,E123,E712,E231,W605,W504,W503,E402 tools
	@printf "\n\n"

test-pylint pylint:
	@printf "Running pylint tests\n+++++++++++++++++++++++++++\n"
	poetry run pylint pyaurorax
	@printf "\n\n"

test-bandit bandit:
	@printf "Running bandit tests\n+++++++++++++++++++++++++++\n"
	poetry run bandit -r -ii pyaurorax
	@printf "\n\n"

test-mypy:
	@printf "Running mypy tests\n+++++++++++++++++++++++++++\n"
	poetry run mypy --ignore-missing-imports --no-strict-optional pyaurorax
	@printf "\n\n"

test-pytest pytest:
	@printf "Running pytest tests\n+++++++++++++++++++++++++++\n"
	poetry run coverage run -m pytest -v
	@printf "\n\n"

test-pytest-unauthorized-access:
	poetry run coverage run -m pytest -v -k "test_AuroraXUnauthorizedException"

test-pytest-read:
	poetry run coverage run -m pytest -v -k "not test_AuroraXUnauthorizedException and not add and not upload and not update and not delete"

test-pytest-create-update-delete:
	poetry run coverage run -m pytest -v -k "add or upload or update or delete"

test-coverage:
	poetry run coverage report

docs:
	poetry run python3 -m pdoc --html --force --output-dir docs pyaurorax --config "lunr_search={'fuzziness': 1}"

publish:
	poetry build
	poetry publish
	@rm -rf pyaurorax.egg-info build dist
