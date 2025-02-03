.PHONY: install update test test-linting test-pycodestyle test-bandit test-pytest test-pytest-search test-coverage show-outdated docs tool-checks publish

all:

poetry:
	python -m pip install poetry

install: poetry
	poetry install

update upgrade:
	python -m pip install --upgrade poetry
	poetry update

docs:
	poetry run pdoc3 --html --force --output-dir docs/generated pyaurorax --config "lunr_search={'fuzziness': 1}" --template-dir docs/templates

test: test-linting

test-linting: test-ruff test-pycodestyle test-pyright test-bandit

test-ruff:
	@printf "Running ruff tests\n+++++++++++++++++++++++++++\n"
	ruff check --respect-gitignore --quiet pyaurorax
	ruff check --respect-gitignore --quiet tests
	ruff check --respect-gitignore --quiet tools
	@printf "\n\n"

test-pycodestyle:
	@printf "Running pycodestyle tests\n+++++++++++++++++++++++++++\n"
	pycodestyle --config=.pycodestyle pyaurorax
	pycodestyle --config=.pycodestyle tests
	pycodestyle --config=.pycodestyle tools
	@printf "\n\n"

test-pyright:
	@printf "Running pyright tests\n+++++++++++++++++++++++++++\n"
	pyright
	@printf "\n\n"

test-bandit:
	@printf "Running bandit tests\n+++++++++++++++++++++++++++\n"
	bandit -c pyproject.toml -r -ii pyaurorax
	@printf "\n\n"

test-pytest:
	pytest -n auto --cov=pyaurorax --cov-report= --dist worksteal

test-notebooks:
	pytest -n 6 --nbmake examples/notebooks --ignore-glob=examples/notebooks/**/in_development/*.ipynb

test-coverage coverage:
	coverage report
	@tools/update_coverage_file.py

show-outdated:
	poetry show --outdated

tool-checks:
	@./tools/check_for_license.py
	@./tools/check_docstrings.py

publish:
	${MAKE} test
	${MAKE} tool-checks
	${MAKE} test-notebooks
	poetry build
	poetry publish
	@rm -rf pyaurorax.egg-info build dist
