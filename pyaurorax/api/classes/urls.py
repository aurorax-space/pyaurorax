"""
This class provides the URL endpoints for different AuroraX
API requests. It is contained in a special class so that we
can use different base URLs if desired.
"""

from typing import Dict
from ...api import DEFAULT_BASE_URL

# pdoc init
__pdoc__: Dict = {}


class URLs:
    __DEFAULT_URL_DATA_SOURCES = "/api/v1/data_sources"
    __DEFAULT_URL_DATA_SOURCES_SEARCH = "/api/v1/data_sources/search"
    __DEFAULT_URL_EPHEMERIS_AVAILABILITY = "/api/v1/availability/ephemeris"
    __DEFAULT_URL_EPHEMERIS_UPLOAD = "/api/v1/data_sources/{}/ephemeris"
    __DEFAULT_URL_EPHEMERIS_SEARCH = "/api/v1/ephemeris/search"
    __DEFAULT_URL_EPHEMERIS_REQUEST = "/api/v1/ephemeris/requests/{}"
    __DEFAULT_URL_DATA_PRODUCTS_AVAILABILITY = "/api/v1/availability/data_products"
    __DEFAULT_URL_DATA_PRODUCTS_UPLOAD = "/api/v1/data_sources/{}/data_products"
    __DEFAULT_URL_DATA_PRODUCTS_SEARCH = "/api/v1/data_products/search"
    __DEFAULT_URL_DATA_PRODUCTS_REQUEST = "/api/v1/data_products/requests/{}"
    __DEFAULT_URL_CONJUNCTION_SEARCH = "/api/v1/conjunctions/search"
    __DEFAULT_URL_CONJUNCTION_REQUEST = "/api/v1/conjunctions/requests/{}"
    __DEFAULT_URL_DESCRIBE_CONJUNCTION_QUERY = "/api/v1/utils/describe/query/conjunction"
    __DEFAULT_URL_DESCRIBE_DATA_PRODUCTS_QUERY = "/api/v1/utils/describe/query/data_products"
    __DEFAULT_URL_DESCRIBE_EPHEMERIS_QUERY = "/api/v1/utils/describe/query/ephemeris"
    __DEFAULT_URL_LIST_REQUESTS = "/api/v1/utils/admin/search_requests"
    __DEFAULT_URL_DELETE_REQUESTS = "/api/v1/utils/admin/search_requests/{}"

    def __init__(self, base_url: str = DEFAULT_BASE_URL) -> None:
        self.__base = base_url
        self.__data_sources = self.__DEFAULT_URL_DATA_SOURCES
        self.__data_sources_search = self.__DEFAULT_URL_DATA_SOURCES_SEARCH
        self.__ephemeris_availability = self.__DEFAULT_URL_EPHEMERIS_AVAILABILITY
        self.__ephemeris_search = self.__DEFAULT_URL_EPHEMERIS_SEARCH
        self.__ephemeris_upload = self.__DEFAULT_URL_EPHEMERIS_UPLOAD
        self.__ephemeris_request = self.__DEFAULT_URL_EPHEMERIS_REQUEST
        self.__data_products_availability = self.__DEFAULT_URL_DATA_PRODUCTS_AVAILABILITY
        self.__data_products_search = self.__DEFAULT_URL_DATA_PRODUCTS_SEARCH
        self.__data_products_upload = self.__DEFAULT_URL_DATA_PRODUCTS_UPLOAD
        self.__data_products_request = self.__DEFAULT_URL_DATA_PRODUCTS_REQUEST
        self.__conjunction_search = self.__DEFAULT_URL_CONJUNCTION_SEARCH
        self.__conjunction_request = self.__DEFAULT_URL_CONJUNCTION_REQUEST
        self.__describe_conjunction_query_url = self.__DEFAULT_URL_DESCRIBE_CONJUNCTION_QUERY
        self.__describe_data_products_query_url = self.__DEFAULT_URL_DESCRIBE_DATA_PRODUCTS_QUERY
        self.__describe_ephemeris_query_url = self.__DEFAULT_URL_DESCRIBE_EPHEMERIS_QUERY
        self.__list_requests_url = self.__DEFAULT_URL_LIST_REQUESTS
        self.__delete_requests_url = self.__DEFAULT_URL_DELETE_REQUESTS

    @property
    def base_url(self) -> str:
        return self.__base

    @base_url.setter
    def base_url(self, value: str) -> None:
        self.__base = value

    # data sources
    # -------------------
    @property
    def data_sources_url(self) -> str:
        return f"{self.__base}{self.__data_sources}"

    @property
    def data_sources_search_url(self) -> str:
        return f"{self.__base}{self.__data_sources_search}"

    # availability
    # -------------------
    @property
    def ephemeris_availability_url(self) -> str:
        return f"{self.__base}{self.__ephemeris_availability}"

    @property
    def data_products_availability_url(self) -> str:
        return f"{self.__base}{self.__data_products_availability}"

    # ephemeris
    # -------------------
    @property
    def ephemeris_search_url(self) -> str:
        return f"{self.__base}{self.__ephemeris_search}"

    @property
    def ephemeris_upload_url(self) -> str:
        return f"{self.__base}{self.__ephemeris_upload}"

    @property
    def ephemeris_request_url(self) -> str:
        return f"{self.__base}{self.__ephemeris_request}"

    # data products
    # -------------------
    @property
    def data_products_search_url(self) -> str:
        return f"{self.__base}{self.__data_products_search}"

    @property
    def data_products_upload_url(self) -> str:
        return f"{self.__base}{self.__data_products_upload}"

    @property
    def data_products_request_url(self) -> str:
        return f"{self.__base}{self.__data_products_request}"

    # conjunctions
    # -------------------
    @property
    def conjunction_search_url(self) -> str:
        return f"{self.__base}{self.__conjunction_search}"

    @property
    def conjunction_request_url(self) -> str:
        return f"{self.__base}{self.__conjunction_request}"

    # describe
    # -------------------
    @property
    def describe_conjunction_query_url(self) -> str:
        return f"{self.__base}{self.__describe_conjunction_query_url}"

    @property
    def describe_data_products_query_url(self) -> str:
        return f"{self.__base}{self.__describe_data_products_query_url}"

    @property
    def describe_ephemeris_query_url(self) -> str:
        return f"{self.__base}{self.__describe_ephemeris_query_url}"

    # admin
    # -------------------
    @property
    def list_requests_url(self) -> str:
        return f"{self.__base}{self.__list_requests_url}"

    @property
    def delete_requests_url(self) -> str:
        return f"{self.__base}{self.__delete_requests_url}"
