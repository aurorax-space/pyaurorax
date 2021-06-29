.PHONY: install update test test-flake8 test-pylint test-bandit test-pytest test-additional clean publish

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

test: test-flake8 test-pylint test-bandit test-pytest

test-flake8 flake8:
	poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	poetry run flake8 . --count --ignore=W391 --max-complexity=20 --max-line-length=127 --statistics
	
test-pylint pylint:
	poetry run pylint aurorax

test-bandit bandit:
	poetry run bandit -r aurorax

test-pytest pytest:
	poetry run pytest

test-pytest-read:
	poetry run pytest -k "not add and not upload and not update and not delete"

test-pytest-create-update-delete:
	poetry run pytest -k "add or upload or update or delete"

test-additional:
	@echo "Type-checking ...\n============================="
	-poetry run mypy aurorax
	@echo "\n\n"
	@echo "Test coverage ...\n============================="
	-poetry run coverage report

publish:
	${MAKE} test
	poetry build
	poetry publish
	${MAKE} clean
