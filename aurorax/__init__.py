__version__ = "0.3.0"

# classes to be found at the top level
from .api import AuroraXRequest, AuroraXRawRequest, AuroraXResponse
from .location import Location

# pull in exceptions
from aurorax import exceptions

# pull in core modules
from aurorax import api
from aurorax import ephemeris
from aurorax import conjunctions
from aurorax import data_products
from aurorax import availability
from aurorax import requests
from aurorax import sources
from aurorax import location
from aurorax import metadata
from aurorax import util
