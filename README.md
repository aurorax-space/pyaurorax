# PyAuroraX

[![Github Actions - Tests](https://github.com/ucalgary-aurora/pyaurorax/workflows/tests/badge.svg)](https://github.com/ucalgary-aurora/pyaurorax/actions?query=workflow%3Atests)
[![PyPI version](https://img.shields.io/pypi/v/pyaurorax.svg)](https://pypi.python.org/pypi/pyaurorax/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![PyPI Python versions](https://img.shields.io/pypi/pyversions/pyaurorax.svg)](https://pypi.python.org/pypi/pyaurorax/)

PyAuroraX is a Python library for interacting with the AuroraX API. Information about AuroraX can be found [here](https://aurorax.space){:target="_blank"} and all documentation for PyAuroraX can be found [here](https://docs.aurorax.space){:target="_blank"}.

## Installing PyAuroraX

PyAuroraX is available on PyPI and officially supports Python 3.6+.

```console
$ python -m pip install pyaurorax
```

## Usage

Check out the [documentation](https://docs.aurorax.space){:target="_blank"} for more information and examples.

```python
>>> import aurorax
```

## Development

### Editing core codebase locally

Clone the repository and install dependencies using Poetry.

Note: if you have issues with Poetry installation, consult their documentation [here](https://python-poetry.org/docs/#installation){:target="_blank"}.

```console
$ git clone https://github.com/ucalgary-aurora/pyaurorax.git
$ cd pyaurorax
$ make install
```

### Editing documentation

Installation:
```console
$ git clone https://github.com/ucalgary-aurora/pyaurorax.git
$ cd pyaurorax
$ make docs-install
```

Serving a local version for editing:
```console
$ make docs-serve
```

## Testing

```console
$ make test
[ or do each test separately ]
$ make test-flake8
$ make test-pylint
$ make test-bandit
$ make test-pytest
```

To run additional tests that are not integrated into the CI pipeline, run the following:

```console
$ make test-additional
```
