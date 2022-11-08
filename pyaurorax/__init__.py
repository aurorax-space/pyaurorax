"""
The PyAuroraX package provides a way to interact with the
[AuroraX API](https://aurorax.space/data/apiLibraries). It is intended
to provide an intuitive process for those in the space physics and related
communities to programmatically query AuroraX's vast database for conjunctions,
ephemeris or data product records, data availability information, and more.
PyAuroraX requires Python 3.6, 3.7, 3.8, or 3.9 (Python 3.10 currently not
supported).

Check out this project on [GitHub](https://github.com/aurorax-space/pyaurorax)
and explore the evolving ecosystem of visualizations, tools, and data
at [AuroraX](https://aurorax.space/).

For an overview of usage and examples, visit the
[AuroraX Documentation website](https://docs.aurorax.space/code/overview).
Details of functionality and options are available in the
[API reference](https://docs.aurorax.space/code/pyaurorax_api_reference/pyaurorax/).

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
__version__ = "0.13.0"

# documentation excludes
__pdoc__ = {"cli": False}

# pull in top level functions
from .api import (AuroraXRequest,
                  authenticate,
                  get_api_key)
from .sources import (FORMAT_BASIC_INFO,
                      FORMAT_BASIC_INFO_WITH_METADATA,
                      FORMAT_FULL_RECORD,
                      FORMAT_IDENTIFIER_ONLY,
                      FORMAT_DEFAULT,
                      SOURCE_TYPE_EVENT_LIST,
                      SOURCE_TYPE_GROUND,
                      SOURCE_TYPE_HEO,
                      SOURCE_TYPE_LEO,
                      SOURCE_TYPE_LUNAR)
from .conjunctions import (CONJUNCTION_TYPE_NBTRACE,
                           CONJUNCTION_TYPE_SBTRACE)
from .data_products import (DATA_PRODUCT_TYPE_KEOGRAM,
                            DATA_PRODUCT_TYPE_MONTAGE,
                            DATA_PRODUCT_TYPE_MOVIE,
                            DATA_PRODUCT_TYPE_SUMMARY_PLOT,
                            DATA_PRODUCT_TYPE_DATA_AVAILABILITY)

# pull in exceptions at top level
from .exceptions import (AuroraXException,
                         AuroraXNotFoundException,
                         AuroraXMaxRetriesException,
                         AuroraXDuplicateException,
                         AuroraXUnexpectedContentTypeException,
                         AuroraXValidationException,
                         AuroraXBadParametersException,
                         AuroraXUnauthorizedException,
                         AuroraXConflictException,
                         AuroraXUploadException,
                         AuroraXUnexpectedEmptyResponse,
                         AuroraXDataRetrievalException,
                         AuroraXTimeoutException)

# pull in models
from .location import Location

# pull in modules (order matters otherwise we get circular import errors)
from pyaurorax import requests
from pyaurorax import api
from pyaurorax import sources
from pyaurorax import exceptions
from pyaurorax import metadata
from pyaurorax import util
from pyaurorax import availability
from pyaurorax import conjunctions
from pyaurorax import ephemeris
from pyaurorax import data_products
