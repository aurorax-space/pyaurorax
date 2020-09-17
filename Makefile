.PHONY: install update test test-dev clean publish

all:

poetry:
	python -m pip install poetry

install: poetry
	poetry install

update:
	python -m pip install --upgrade poetry
	poetry update

clean:
	@rm -rf pyaurorax.egg-info build dist

test:
	find . -type f -name '*.py' -exec sed -i -e "s/\r//g" {} \;
	poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	poetry run flake8 . --count --ignore=W391 --exit-zero --max-complexity=20 --max-line-length=127 --statistics
	poetry run pylint aurorax
	poetry run bandit -r aurorax
	poetry run pytest

test-dev:
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
