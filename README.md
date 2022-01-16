<a href="https://aurorax.space/"><img alt="AuroraX" src="logo.svg" height="60"></a>

[![Github Actions - Tests](https://github.com/aurorax-space/pyaurorax/workflows/tests/badge.svg)](https://github.com/aurorax-space/pyaurorax/actions?query=workflow%3Atests)
[![PyPI version](https://img.shields.io/pypi/v/pyaurorax.svg)](https://pypi.python.org/pypi/pyaurorax/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![PyPI Python versions](https://img.shields.io/pypi/pyversions/pyaurorax.svg)](https://pypi.python.org/pypi/pyaurorax/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5815985.svg)](https://doi.org/10.5281/zenodo.5815985)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Faurorax-space%2Fpyaurorax.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Faurorax-space%2Fpyaurorax?ref=badge_shield)

PyAuroraX is a Python library for interacting with [AuroraX](https://aurorax.space), a project working to be the world's first and foremost data platform for auroral science. The primary objective of AuroraX is to enable mining and exploration of existing and future auroral data, enabling key science and enhancing the benefits of the world's investment in auroral instrumentation. This will be accomplished with the development of key systems/standards for uniform metadata generation and search, image content analysis, interfaces to leading international tools, and a community involvement that includes more than 80% of the world's data providers.

PyAuroraX officially supports Python 3.6, 3.7, 3.8, and 3.9 (Python 3.10 not currently supported).

Some links to help:
- [AuroraX main website](https://aurorax.space)
- [PyAuroraX documentation](https://docs.aurorax.space/python_libraries/pyaurorax/overview)
- [PyAuroraX API Reference](https://docs.aurorax.space/python_libraries/pyaurorax/api_reference/pyaurorax)

## Installation

PyAuroraX is available on PyPI so pip can be used to install it:

```console
$ python -m pip install pyaurorax
```

To get full functionality, you can also install PyAuroraX with the aacgmv2 dependency. Note that without this, the calculate_btrace methods in the util module will show warning messages. All other functionality will work without this dependency.

```console
$ python -m pip install pyaurorax[aacgmv2]
```

Futhermore, if you want the most bleeding edge version of PyAuroraX, you can install it directly from the Github repository:

```console
$ git clone https://github.com/aurorax-space/pyaurorax.git
$ cd pyaurorax
$ python -m pip install .
[ or with the aacgmv2 extra ]
$ python -m pip install .[aacgmv2]
```

## Usage

There are two things you can use as part of the PyAuroraX library: the main library, and the command line tool.

### Library import

You can import the library using the following statement:

```python
>>> import pyaurorax
```

### CLI program

The program `aurorax-cli` is included in the PyAuroraX package as a command line tool. Try it out using:

```
$ aurorax-cli --help
```

## Development

Some common things you can do:
- `make update` Update the Python dependency libraries
- `tools/bump_version.py` Bump the version number
- `make test-pytest-unauthorized-access` Only run the authorization tests
- `make test-pytest-read` Only run the read-based tests
- `make test-pytest-create-update-delete` Only run the write-based tests
- `make docs` Generate pdoc documentation

### Setup

Clone the repository and install primary and development dependencies using Poetry.

```console
$ git clone git@github.com:aurorax-space/pyaurorax.git
$ cd pyaurorax
$ make install
```

### Documentation

Documentation for the PyAuroraX project is managed by a separate repository [here](https://github.com/aurorax-space/docs). However, you are still able to generate the documentation for this repo for testing/development purposes. To generate the docs, run the following:

```console
$ make docs
```

### Testing

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


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Faurorax-space%2Fpyaurorax.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Faurorax-space%2Fpyaurorax?ref=badge_large)