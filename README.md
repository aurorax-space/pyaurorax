# PyAuroraX

[![Github Actions - Tests](https://github.com/ucalgary-aurora/pyaurorax/workflows/tests/badge.svg)](https://github.com/ucalgary-aurora/pyaurorax/actions?query=workflow%3Atests)
[![PyPI version](https://img.shields.io/pypi/v/pyaurorax.svg)](https://pypi.python.org/pypi/pyaurorax/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![PyPI Python versions](https://img.shields.io/pypi/pyversions/pyaurorax.svg)](https://pypi.python.org/pypi/pyaurorax/)
[![Bandit Security](https://img.shields.io/badge/security-bandit-lightgrey.svg)](https://github.com/PyCQA/bandit)

Python library for interacting with the AuroraX API.

## Installing Requests and Supported Versions

Pyurorax is available on PyPI:

```console
$ python -m pip install pyaurorax
```

PyAuroraX officially supports Python 3.5+.

## Usage

```python
import aurorax
````

## Development

```console
$ git clone https://github.com/ucalgary-aurora/pyaurorax.git
$ cd pyaurorax
$ make install
```

## Testing

```console
$ make test
```

## Additional Testing for Development Environments

```console
$ make test-dev
```
