# Copyright 2024 University of Calgary
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Interact with the AuroraX search engine. This includes finding data sources, searching 
for conjunctions or ephemeris data, and uploading/managing your own data in the AuroraX platform.
"""

# pull in classes
from .location import Location
from .sources.classes.data_source import DataSource
from .availability.classes.availability_result import AvailabilityResult
from .ephemeris.classes.ephemeris import EphemerisData
from .ephemeris.classes.search import EphemerisSearch
from .data_products.classes.data_product import DataProductData
from .data_products.classes.search import DataProductSearch
from .conjunctions.classes.conjunction import Conjunction
from .conjunctions.classes.search import ConjunctionSearch

# pull in constants
from .sources.classes.data_source import (
    FORMAT_BASIC_INFO,
    FORMAT_BASIC_INFO_WITH_METADATA,
    FORMAT_FULL_RECORD,
    FORMAT_IDENTIFIER_ONLY,
    FORMAT_DEFAULT,
    SOURCE_TYPE_EVENT_LIST,
    SOURCE_TYPE_GROUND,
    SOURCE_TYPE_HEO,
    SOURCE_TYPE_LEO,
    SOURCE_TYPE_LUNAR,
)
from .data_products.classes.data_product import (
    DATA_PRODUCT_TYPE_KEOGRAM,
    DATA_PRODUCT_TYPE_MONTAGE,
    DATA_PRODUCT_TYPE_MOVIE,
    DATA_PRODUCT_TYPE_SUMMARY_PLOT,
    DATA_PRODUCT_TYPE_DATA_AVAILABILITY,
)
from .conjunctions.classes.conjunction import CONJUNCTION_TYPE_NBTRACE, CONJUNCTION_TYPE_SBTRACE

# imports for this file
from . import api as module_api
from .util import UtilManager
from .sources import SourcesManager
from .availability import AvailabilityManager
from .metadata import MetadataManager
from .requests import RequestsManager
from .ephemeris import EphemerisManager
from .data_products import DataProductsManager
from .conjunctions import ConjunctionsManager

__all__ = [
    "SearchManager",
    "FORMAT_BASIC_INFO",
    "FORMAT_BASIC_INFO_WITH_METADATA",
    "FORMAT_FULL_RECORD",
    "FORMAT_IDENTIFIER_ONLY",
    "FORMAT_DEFAULT",
    "SOURCE_TYPE_EVENT_LIST",
    "SOURCE_TYPE_GROUND",
    "SOURCE_TYPE_HEO",
    "SOURCE_TYPE_LEO",
    "SOURCE_TYPE_LUNAR",
    "DATA_PRODUCT_TYPE_KEOGRAM",
    "DATA_PRODUCT_TYPE_MONTAGE",
    "DATA_PRODUCT_TYPE_MOVIE",
    "DATA_PRODUCT_TYPE_SUMMARY_PLOT",
    "DATA_PRODUCT_TYPE_DATA_AVAILABILITY",
    "CONJUNCTION_TYPE_NBTRACE",
    "CONJUNCTION_TYPE_SBTRACE",
    "DataSource",
    "Location",
    "AvailabilityResult",
    "EphemerisData",
    "EphemerisSearch",
    "DataProductData",
    "DataProductSearch",
    "Conjunction",
    "ConjunctionSearch",
]


class SearchManager:
    """
    The SearchManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    def __init__(self, aurorax_obj):
        self.__aurorax_obj = aurorax_obj

        # initialize sub-modules
        self.__util = UtilManager()
        self.__api = module_api
        self.__sources = SourcesManager(self.__aurorax_obj)
        self.__availability = AvailabilityManager(self.__aurorax_obj)
        self.__metadata = MetadataManager(self.__aurorax_obj)
        self.__requests = RequestsManager(self.__aurorax_obj)
        self.__ephemeris = EphemerisManager(self.__aurorax_obj)
        self.__data_products = DataProductsManager(self.__aurorax_obj)
        self.__conjunctions = ConjunctionsManager(self.__aurorax_obj)

    # ------------------------------------------
    # properties for submodule managers
    # ------------------------------------------
    @property
    def util(self):
        """
        Access to the `util` submodule from within a PyAuroraX object.
        """
        return self.__util

    @property
    def api(self):
        """
        Access to the `api` submodule from within a PyAuroraX object.
        """
        return self.__api

    @property
    def sources(self):
        """
        Access to the `sources` submodule from within a PyAuroraX object.
        """
        return self.__sources

    @property
    def availability(self):
        """
        Access to the `availability` submodule from within a PyAuroraX object.
        """
        return self.__availability

    @property
    def metadata(self):
        """
        Access to the `metadata` submodule from within a PyAuroraX object.
        """
        return self.__metadata

    @property
    def requests(self):
        """
        Access to the `requests` submodule from within a PyAuroraX object.
        """
        return self.__requests

    @property
    def ephemeris(self):
        """
        Access to the `ephemeris` submodule from within a PyAuroraX object.
        """
        return self.__ephemeris

    @property
    def data_products(self):
        """
        Access to the `data_products` submodule from within a PyAuroraX object.
        """
        return self.__data_products

    @property
    def conjunctions(self):
        """
        Access to the `conjunctions` submodule from within a PyAuroraX object.
        """
        return self.__conjunctions
