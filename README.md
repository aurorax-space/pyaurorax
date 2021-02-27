# PyAuroraX

[![Github Actions - Tests](https://github.com/ucalgary-aurora/pyaurorax/workflows/tests/badge.svg)](https://github.com/ucalgary-aurora/pyaurorax/actions?query=workflow%3Atests)
[![PyPI version](https://img.shields.io/pypi/v/pyaurorax.svg)](https://pypi.python.org/pypi/pyaurorax/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![PyPI Python versions](https://img.shields.io/pypi/pyversions/pyaurorax.svg)](https://pypi.python.org/pypi/pyaurorax/)

Python library for interacting with the AuroraX API.

## Installing PyAuroraX

PyAuroraX is available on PyPI:

```console
$ python -m pip install pyaurorax
```

## Supported Python Versions

PyAuroraX officially supports Python 3.6+.

## Usage

```python
>>> import aurorax
```

## Development

Clone the repository and install dependencies using Poetry.

```console
$ git clone https://github.com/ucalgary-aurora/pyaurorax.git
$ cd pyaurorax
$ make install
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

## Additional Testing for Development Environments

To run additional tests that are not integrated into the CI pipeline, run the following:

```console
$ make test-additional
```
