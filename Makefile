.PHONY: install update get-test-data docs test test-linting test-pycodestyle test-bandit test-pytest test-pytest test-pytest-search-rw test-pytest-notebooks test-coverage show-outdated tool-checks publish

all:

install:
	pip install poetry
	poetry install
	${MAKE} get-test-data

update upgrade:
	 pip install --upgrade poetry
	poetry update

get-test-data:
	mkdir -p tests/test_data
	cd tests/test_data && rm -rf *
	cd tests/test_data && wget -O test_data.tar.gz https://aurora.phys.ucalgary.ca/public/github_tests/pyaurorax_test_data.tar.gz
	cd tests/test_data && tar -zxvf test_data.tar.gz && rm test_data.tar.gz

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
	COVERAGE_FILE=.coverage_main pytest -n 8 --cov=pyaurorax --cov-report= --cov-append --do-search-tasks --do-tools-tasks -m "not search_rw"

test-pytest-search-rw:
	COVERAGE_FILE=.coverage_search_rw pytest -n 4 --cov=pyaurorax --cov-report= --cov-append --do-search-tasks -m "search_rw"

test-pytest-notebooks test-notebooks:
	pytest -n 6 --nbmake examples/notebooks --ignore-glob=examples/notebooks/**/in_development/*.ipynb

test-pytest-clear:
	rm .coverage_main
	rm .coverage_search_rw

test-coverage coverage:
	coverage combine --keep .coverage_main .coverage_search_rw
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
	poetry build
	poetry publish
	@rm -rf pyaurorax.egg-info build dist
