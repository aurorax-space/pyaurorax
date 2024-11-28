<a href="https://aurorax.space/"><img alt="AuroraX" src="logo.svg" height="60"></a>

[![GitHub tests](https://github.com/aurorax-space/pyaurorax/actions/workflows/tests_default.yml/badge.svg)](https://github.com/aurorax-space/pyaurorax/actions/workflows/tests_default.yml)
[![PyPI version](https://img.shields.io/pypi/v/pyaurorax.svg)](https://pypi.python.org/pypi/pyaurorax/)
![PyPI Python versions](https://img.shields.io/pypi/pyversions/pyaurorax)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5815984.svg)](https://doi.org/10.5281/zenodo.5815984)

PyAuroraX is a Python library providing data access and analysis support for All-Sky Imager data (THEMIS, TREx, REGO, etc.), the ability to utilize the TREx Auroral Transport Model, and interact with the AuroraX Search Engine. [AuroraX](https://aurorax.space) is a project working to be the world's first and foremost data platform for auroral science. The primary objective is to enable mining and exploration of existing and future auroral data, enabling key science and enhancing the benefits of the world's investment in auroral instrumentation. We have developed key systems/standards for uniform metadata generation and search, image content analysis, interfaces to leading international tools, and a community involvement that includes more than 80% of the world's data providers.

PyAuroraX officially supports Python 3.9+.

Some links to help:
- [Example Gallery](https://data.phys.ucalgary.ca/working_with_data/index.html#python)
- [PyAuroraX API Reference](https://docs.aurorax.space/code/pyaurorax_api_reference/pyaurorax)
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

## Contributing

Bug reports, feature suggestions, and other contributions are greatly appreciated!

Templates for bug report and feature suggestions can be found when creating a Github Issue. If you have questions or issues installing PyAuroraX, we encourage that you open up a topic in the Github Discussions page.
