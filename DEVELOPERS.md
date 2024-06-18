# Development

Some common things you can do:
- `make update` Update the Python dependency libraries
- `tools/bump_version.py` Bump the version number
- `make test-pytest-unauthorized-access` Only run the authorization tests
- `make test-pytest-read` Only run the read-based tests
- `make test-pytest-create-update-delete` Only run the write-based tests
- `make docs` Generate pdoc documentation

## Setup

Clone the repository and install primary and development dependencies using Poetry.

```console
$ git clone git@github.com:aurorax-space/pyaurorax.git
$ cd pyaurorax
$ python -m pip install poetry
$ poetry install -E aacgmv2
```

## Documentation

Documentation for the PyAuroraX project is managed by a separate repository [here](https://github.com/aurorax-space/docs). However, you are still able to generate the documentation for this repo for testing/development purposes. To generate the docs, run the following:

```console
$ make docs
```

## Testing

PyAuroraX includes several test evaluations bundled into two groups: linting and functionality tests. The linting includes looking through the codebase using tools such as Flake8, PyLint, Pycodestyle, Bandit, and MyPy. The functionality tests use PyTest to test modules in the library.

When running the functionality tests using PyTest, you must have the environment variable `AURORAX_APIKEY_STAGING` set to your API key on the staging API system. Alternatively, you can specifiy your API key using the command line (see example at the bottom of this section).

There exist several makefile targets to help run these tests quicker/easier. Below are the available commands:

- `make test-linting` Run all linting tests
- `make test-pytest` Run all automated functional tests
- `make test-flake8` Run Flake8 styling tests
- `make test-pylint` Run PyLint styling tests
- `make test-pycodestyle` Run pycodestyle styling tests
- `make test-bandit` Run Bandit security test
- `make test-mypy` Run mypy type checking test
- `make test-coverage` View test coverage report (must be done after `make test-pytest` or other coverage command)

The PyTest functionality tests include several categories of tests. You can run each category separately if you want using the "markers" feature of PyTest. All markers are found in the pytest.ini file at the root of the repository.

- `poetry run pytest --markers` List all markers
- `poetry run pytest -v -m accounts` Perform only the tests for the "accounts" marker
- `poetry run pytest -v -m availability` Perform only the tests for the "availability" marker
- `poetry run pytest -v -m conjunctions` Perform only the tests for the "conjunctions" marker
- `poetry run pytest -v -m ephemeris` Perform only the tests for the "ephemeris" marker
- `poetry run pytest -v -m exceptions` Perform only the tests for the "exceptions" marker
- `poetry run pytest -v -m location` Perform only the tests for the "location" marker
- `poetry run pytest -v -m metadata` Perform only the tests for the "metadata" marker
- `poetry run pytest -v -m requests` Perform only the tests for the "request" marker
- `poetry run pytest -v -m sources` Perform only the tests for the "sources" marker
- `poetry run pytest -v -m util` Perform only the tests for the "util" marker

Below are some more commands for advanced usages of PyTest.

- `poetry run pytest -v` Run all tests in verbose mode
- `poetry run pytest --collect-only` List all available tests
- `poetry run pytest --markers` List all markers (includes builtin, plugin and per-project ones)
- `cat pytest.ini` List custom markers
- `poetry run pytest tests/test_suite/ephemeris/test_ephemeris.py::test_get_request_url -v` Run a single specific test

You can also run Pytest against a different API. By default, it runs agains the staging API, but you can alternatively tell it to run against the production API, or a local instance.

- `poetry run pytest -v --env=production` Run all tests against production API, using the AURORAX_APIKEY_PRODUCTION environment variable
- `poetry run pytest --env=local --host=http://localhost:3000` Run all tests against a local instance of the API, using the AURORAX_APIKEY_LOCAL environment variable
- `poetry run pytest -v --api-key=SOME_API_KEY` Run all tests with the specified API key (will run against the staging API since that's the default)
- `poetry run pytest --help` View usage for pytest, including the usage for custom options (see the 'custom options' section of the output)

Below are some more commands for evaluating the PyTest coverage.

- `poetry run coverage report` View test coverage report
- `poetry run coverage html` Generate an HTML page of the coverage report
- `poetry run coverage report --show-missing` View the test coverage report and include the lines deemed to be not covered by tests

Note that the coverage report only gets updated when using the Makefile pytest targets, or when running coverage manually like `coverage run -m pytest -v`. More information about usage of the `coverage` command can be found [here](https://coverage.readthedocs.io).

## Publishing new release

To publish a new release, you must set the PyPI token first within Poetry and then upload the new package:

```console
$ poetry config pypi-token.pypi <pypi token>
$ make publish
```
