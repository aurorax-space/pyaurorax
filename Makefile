.PHONY: install update test test-linting test-pycodestyle test-bandit test-pytest test-pytest-search test-coverage show-outdated docs publish

all:

poetry:
	python -m pip install poetry

install: poetry
	poetry install

update upgrade:
	python -m pip install --upgrade poetry
	poetry update

test: test-linting

test-linting: test-ruff test-pycodestyle test-pyright test-bandit

test-ruff ruff:
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

test-pyright pyright:
	@printf "Running pyright tests\n+++++++++++++++++++++++++++\n"
	pyright
	@printf "\n\n"

test-bandit bandit:
	@printf "Running bandit tests\n+++++++++++++++++++++++++++\n"
	bandit -c pyproject.toml -r -ii pyaurorax
	@printf "\n\n"

test-pytest pytest:
	pytest -n auto --cov=pyaurorax --cov-report= --maxfail=1

test-pytest-search:
	pytest -n auto -m "search_accounts or search_availability or search_conjunctions or search_data_products or search_ephemeris or search_exceptions or search_location or search_metadata or search_requests or search_sources or search_util"

test-coverage coverage:
	coverage report
	@tools/update_coverage_file.py

show-outdated:
	poetry show --outdated

docs:
	poetry run pdoc3 --html --force --output-dir docs/generated pyaurorax --config "lunr_search={'fuzziness': 1}" --template-dir docs/templates

publish:
	${MAKE} test
	poetry build
	poetry publish
	@rm -rf pyaurorax.egg-info build dist
