# PyAuroraX

[![Github Actions - Tests](https://github.com/aurorax-space/pyaurorax/workflows/tests/badge.svg)](https://github.com/aurorax-space/pyaurorax/actions?query=workflow%3Atests)
[![PyPI version](https://img.shields.io/pypi/v/pyaurorax.svg)](https://pypi.python.org/pypi/pyaurorax/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![PyPI Python versions](https://img.shields.io/pypi/pyversions/pyaurorax.svg)](https://pypi.python.org/pypi/pyaurorax/)

PyAuroraX is a Python library for interacting with [AuroraX](https://aurorax.space), a project working to be the world's first and foremost data platform for auroral science. The primary objective of AuroraX is to enable mining and exploration of existing and future auroral data, enabling key science and enhancing the benefits of the world's investment in auroral instrumentation. This will be accomplished with the development of key systems/standards for uniform metadata generation and search, image content analysis, interfaces to leading international tools, and a community involvement that includes more than 80% of the world's data providers.

Documentation can be found at [here](https://docs.aurorax.space/python_libraries/pyaurorax/overview)

PyAuroraX officially supports Python 3.6+.

## Installation

PyAuroraX is available on PyPI:

```console
$ python -m pip install pyaurorax
```

Alternatively, you can install the latest development version from the Github repository
```console
$ git clone https://github.com/aurorax-space/pyaurorax.git
$ cd pyaurorax
$ python -m pip install .
```

## Usage

```python
>>> import pyaurorax
```

## CLI Program

The program `aurorax-cli` is included in the PyAuroraX package as a command line tool.

```
aurorax-cli --help
```

## Development

Some things you can do include:
- `make update` Update the Python dependency libraries
- `tools/bump_version.py` Bump the version number
- `make test-pytest-unauthorized-access` Only run the authorization tests
- `test-pytest-read` Only run the read-based tests
- `test-pytest-create-update-delete` Only run the write-based tests

### Setup

Clone the repository and install dependencies using Poetry.

```console
$ git clone git@github.com:aurorax-space/pyaurorax.git
$ cd pyaurorax
$ make install
```

### Testing

PyAuroraX includes several test evaluations bundled into two groups: linting and functionality tests. The linting includes looking through the codebase using tools such as Flake8, PyLint, Bandit, and Pycodestyle. The functionality tests use PyTest to test each function in the library.

There exist several makefile targets to help run these tests easier. Below are the available commands:

- `make test-linting` Run all linting tests
- `make test-pytest` Run all automated functional tests
- `make test-flake8` Run Flake8 tests
- `make test-pylint` Run PyLint tests
- `make test-pycodestyle` Run pycodestyle test
- `make test-bandit` Run Bandit test

The PyTest functionality tests include several categories of tests. You can run each category separately if you want using the "markers" functionality of PyTest. All markers are found in the pytest.ini file at the root of the repository. 

- `poetry run pytest --markers` List all markers
- `poetry run pytest -v -m accounts` Perform only the tests for the "accounts" marker
- `poetry run pytest -v -m availability` Perform only the tests for the "availability" marker
- `poetry run pytest -v -m conjunctions` Perform only the tests for the "conjunctions" marker
- `poetry run pytest -v -m ephemeris` Perform only the tests for the "ephemeris" marker

Below are some more commands for advanced usages of PyTest.

- `poetry run pytest -v` Run all tests in verbose mode
- `poetry run pytest --collect-only` List all available tests
- `poetry run pytest --markers` List all markers (includes builtin, plugin and per-project ones)
- `cat pytest.ini` List custom markers

### Additional Testing

To run additional tests that are not integrated into the CI pipeline, run the following:

```console
$ make test-additional
```
