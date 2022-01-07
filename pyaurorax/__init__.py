"""
The PyAuroraX package provides a way to interact with the
[AuroraX API](https://aurorax.space/data/api_libraries). It is intended
to provide an intuitive process for those in the space physics and related
communities to programmatically query AuroraX's vast database for conjunctions,
ephemeris or data product records, data availability information, and more.
PyAuroraX requires Python 3.6, 3.7, 3.8, or 3.9 (Python 3.10 currently not
supported).

Check out this project on [GitHub](https://github.com/aurorax-space/pyaurorax)
and explore the evolving ecosystem of visualizations, tools, and data
at [AuroraX](https://aurorax.space/).

For an overview of usage and examples, visit the
[AuroraX Documentation website](https://docs.aurorax.space/python_libraries/pyaurorax/).
Details of functionality and options are available in the
[API reference](https://docs.aurorax.space/python_libraries/pyaurorax/api_reference/aurorax/).

Installation:
```console
$ python -m pip install pyaurorax
```

Basic usage:
```python
> import pyaurorax
```
"""

# versioning info
__version__ = "0.9.0"

# documentation excludes
__pdoc__ = {"cli": False}

# pull in top level functions
from .api import AuroraXRequest
from .api import authenticate
from .api import get_api_key
from .format import FORMAT_BASIC_INFO
from .format import FORMAT_BASIC_INFO_WITH_METADATA
from .format import FORMAT_FULL_RECORD
from .format import FORMAT_IDENTIFIER_ONLY
from .format import FORMAT_DEFAULT
from .sources import SOURCE_TYPE_EVENT_LIST
from .sources import SOURCE_TYPE_GROUND
from .sources import SOURCE_TYPE_HEO
from .sources import SOURCE_TYPE_LEO
from .sources import SOURCE_TYPE_LUNAR
from .conjunctions import CONJUNCTION_TYPE_NBTRACE
from .conjunctions import CONJUNCTION_TYPE_SBTRACE

# pull in exceptions at top level
from .exceptions import AuroraXException
from .exceptions import AuroraXNotFoundException
from .exceptions import AuroraXMaxRetriesException
from .exceptions import AuroraXDuplicateException
from .exceptions import AuroraXUnexpectedContentTypeException
from .exceptions import AuroraXValidationException
from .exceptions import AuroraXBadParametersException
from .exceptions import AuroraXUnauthorizedException
from .exceptions import AuroraXConflictException
from .exceptions import AuroraXUploadException

# pull in models
from .location import Location

# pull in modules (order matters otherwise we get circular import errors)
from pyaurorax import api
from pyaurorax import requests
from pyaurorax import sources
from pyaurorax import exceptions
from pyaurorax import metadata
from pyaurorax import util
from pyaurorax import availability
from pyaurorax import conjunctions
from pyaurorax import ephemeris
from pyaurorax import data_products
from pyaurorax import format
