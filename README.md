<a href="https://aurorax.space/"><img alt="AuroraX" src="logo.svg" height="60"></a>

[![GitHub tests](https://github.com/aurorax-space/pyaurorax/actions/workflows/test_standard.yml/badge.svg)](https://github.com/aurorax-space/pyaurorax/actions/workflows/test_standard.yml)
[![PyPI version](https://img.shields.io/pypi/v/pyaurorax.svg)](https://pypi.python.org/pypi/pyaurorax/)
[![PyPI Python versions](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue)](https://pypi.python.org/pypi/pyaurorax/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.12532077.svg)](https://doi.org/10.5281/zenodo.12532077)

PyAuroraX is a Python library for interacting with [AuroraX](https://aurorax.space), a project working to be the world's first and foremost data platform for auroral science. The primary objective of AuroraX is to enable mining and exploration of existing and future auroral data, enabling key science and enhancing the benefits of the world's investment in auroral instrumentation. This will be accomplished with the development of key systems/standards for uniform metadata generation and search, image content analysis, interfaces to leading international tools, and a community involvement that includes more than 80% of the world's data providers.

PyAuroraX officially supports Python 3.9+.

Some links to help:
- [PyAuroraX documentation](https://docs.aurorax.space/code/overview)
- [PyAuroraX API Reference](https://docs.aurorax.space/code/pyaurorax_api_reference/pyaurorax)
- [Jupyter notebook examples](https://github.com/aurorax-space/pyaurorax/tree/main/examples/notebooks)
- [AuroraX main website](https://aurorax.space)

## Installation

PyAuroraX is available on PyPI so pip can be used to install it:

```console
$ pip install pyaurorax
```

Futhermore, if you want the most bleeding edge version of PyAuroraX, you can install it directly from the Github repository:

```console
$ git clone https://github.com/aurorax-space/pyaurorax.git
$ cd pyaurorax
$ pip install .
```

## Usage

There are two things you can use as part of the PyAuroraX library: the main library, and the command line tool.

You can import the library using the following statement:

```python
>>> import pyaurorax
>>> aurorax = pyaurorax.PyAuroraX()
```

The program `aurorax-cli` is included in the PyAuroraX package as a command line tool. Try it out using:

```
$ aurorax-cli --help
```

## Migrating from V0 to V1

A significant upgrade was released for PyAuroraX for version 1.0.0. A major code reorganization and addition of many new features is part of version 1.x, and therefore includes breaking changes. The existing codebase from v0.13.3 and earlier has remained mostly unchanged, but, has been reorganized and some classes
were renamed. Simply changing the names of imports, function calls, and/or class instantiations should suffice in most cases. 

Please refer to the `RELEASE_NOTES.md` file for a full breakdown of what was changed, the [documentation](https://docs.aurorax.space/code/overview), and the [API Reference](https://docs.aurorax.space/code/pyaurorax_api_reference/pyaurorax) to help adjust your code.
