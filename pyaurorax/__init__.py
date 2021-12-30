"""
The PyAuroraX package provides a way to interact with the [AuroraX REST API](https://aurorax.space/data/api_libraries).
It is intended to provide an intuitive process for those in the space physics and citizen science communities to
programmatically query AuroraX's vast database for conjunctions, ephemeris or data product records, data availability, and
statistics. Requires Python3.6+.

Check out this project on [GitHub](https://github.com/aurorax-space/pyaurorax) and explore the evolving ecosystem of
visualizations, tools, and data at [AuroraX](https://aurorax.space/).

For an overview of intended usage and examples, visit the
[AuroraX Documentation website](https://docs.aurorax.space/python_libraries/pyaurorax/).
Details of functionality and options are available in the
[API reference](https://docs.aurorax.space/python_libraries/pyaurorax/api_reference/aurorax/).

Installation:
```console
$ pip install pyaurorax
```

Basic usage:
```python
> import pyaurorax
```
"""
__version__ = "0.8.0"

# pull in top level functions
from .api import AuroraXRequest
from .api import authenticate
from .api import get_api_key

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
from .models import Location

# pull in modules
from pyaurorax import requests
from pyaurorax import exceptions
from pyaurorax import api
from pyaurorax import sources
from pyaurorax import metadata
from pyaurorax import availability
from pyaurorax import ephemeris
from pyaurorax import data_products
from pyaurorax import conjunctions
from pyaurorax import util
