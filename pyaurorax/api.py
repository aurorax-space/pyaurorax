"""
The API module contains classes and methods used throughout PyAuroraX for API interaction.
"""
import pyaurorax
import json
import pprint
from pydantic import BaseModel
import requests
from typing import Optional, Dict, Any, List, Union
from ._internal.util import json_converter

# endpoint URLs
DEFAULT_URL_BASE = "https://api.aurorax.space"

# reqest globals
DEFAULT_RETRIES = 2
REQUEST_HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json"
}
API_KEY_HEADER_NAME = "x-aurorax-api-key"

# private dynamic globals
__api_key = ""


def get_api_key() -> str:
    """
    Returns the currently set API key for the module.

    Returns:
        Current API key string.
    """
    return __api_key


def authenticate(api_key: str) -> None:
    """
    Set authentication values for use with subsequent queries.

    Attributes:
        api_key: AuroraX API key string.

    """

    # set the global variable
    global __api_key
    __api_key = api_key


class AuroraXResponse(BaseModel):
    request: Any
    data: Any
    status_code: int

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)


class AuroraXRequest(BaseModel):
    url: str
    method: str
    params: Optional[Dict] = {}
    body: Union[Optional[Dict], Optional[List]] = {}
    headers: Optional[Dict] = {}
    null_response: Optional[bool] = False

    def __merge_headers(self):
        # set initial headers
        all_headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

        # add headers passed into the class
        for key, value in self.headers.items():
            all_headers[key] = value

        # add api key
        api_key = get_api_key()
        if api_key:
            all_headers[API_KEY_HEADER_NAME] = api_key

        # return
        return all_headers

    def execute(self, limited_evaluation: bool = False) -> AuroraXResponse:
        """
        Execute an AuroraX request.

        Attributes:
            limited_evaluation: set this to True if you don't want to evaluate the response outside of
                the retry mechanism, defaults to False.

        Returns:
            An AuroraXResponse object.

        Raises:
            pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error.
            pyaurorax.exceptions.AuroraXNotFoundException: requested resource was not found.
            pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected content error.
            pyaurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation.

        """
        # sanitize data
        body_santized = json.dumps(self.body, default=json_converter)

        # make request
        req = requests.request(self.method,
                               self.url,
                               headers=self.__merge_headers(),
                               params=self.params,
                               data=body_santized)

        # retry request if needed
        for i in range(0, pyaurorax.api.DEFAULT_RETRIES):
            if (req.status_code == 500 and "text/plain" in req.headers["Content-Type"]):
                if (i == (pyaurorax.api.DEFAULT_RETRIES - 1)):
                    raise pyaurorax.AuroraXMaxRetriesException("%s (%s)" % (req.content.decode(),
                                                                            req.status_code))
                req = requests.request(self.method,
                                       self.url,
                                       headers=self.__merge_headers(),
                                       params=self.params,
                                       json=self.body,
                                       data=body_santized)
            else:
                break

        # check if authorization worked
        if (req.status_code == 401):
            raise pyaurorax.AuroraXUnauthorizedException("%s %s" % (req.status_code,
                                                                    req.json()["error_message"]))

        if (req.status_code == 404):
            raise pyaurorax.AuroraXNotFoundException("%s %s" % (req.status_code,
                                                                req.json()["error_message"]))

        # check if we only want to do limited evaluation
        if (limited_evaluation is True):
            res = AuroraXResponse(request=req, data=None,
                                  status_code=req.status_code)
            return res

        # check content type
        if (self.null_response is False):
            if (req.headers["Content-Type"] == "application/json"):
                response_data = req.json()
            else:
                raise pyaurorax.AuroraXUnexpectedContentTypeException("%s (%s)" % (req.content.decode(),
                                                                                   req.status_code))
        else:
            if (req.status_code != 200 and req.status_code != 201 and req.status_code != 202 and req.status_code != 204):
                response_data = req.json()
            else:
                response_data = None

        # check for server error
        if (req.status_code == 500):
            response_json = req.json()
            if ("error_message" in response_json):
                raise pyaurorax.AuroraXException("%s (%s)" % (response_json["error_message"],
                                                              req.status_code))
            else:
                raise pyaurorax.AuroraXException(response_json)

        # create reponse object
        res = AuroraXResponse(
            request=req, data=response_data, status_code=req.status_code)

        # return
        return res

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)


class URLs:
    __DEFAULT_URL_DATA_SOURCES = "/api/v1/data_sources"
    __DEFAULT_URL_STATS = "/api/v1/stats"
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

    def __init__(self, base_url: str = DEFAULT_URL_BASE) -> None:
        self.__base = base_url
        self.__data_sources = self.__DEFAULT_URL_DATA_SOURCES
        self.__stats = self.__DEFAULT_URL_STATS
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
        return "%s%s" % (self.__base, self.__data_sources)

    @property
    def stats_url(self) -> str:
        return "%s%s" % (self.__base, self.__stats)

    # availability
    # -------------------
    @property
    def ephemeris_availability_url(self) -> str:
        return "%s%s" % (self.__base, self.__ephemeris_availability)

    @property
    def data_products_availability_url(self) -> str:
        return "%s%s" % (self.__base, self.__data_products_availability)

    # ephemeris
    # -------------------
    @property
    def ephemeris_search_url(self) -> str:
        return "%s%s" % (self.__base, self.__ephemeris_search)

    @property
    def ephemeris_upload_url(self) -> str:
        return "%s%s" % (self.__base, self.__ephemeris_upload)

    @property
    def ephemeris_request_url(self) -> str:
        return "%s%s" % (self.__base, self.__ephemeris_request)

    # data products
    # -------------------
    @property
    def data_products_search_url(self) -> str:
        return "%s%s" % (self.__base, self.__data_products_search)

    @property
    def data_products_upload_url(self) -> str:
        return "%s%s" % (self.__base, self.__data_products_upload)

    @property
    def data_products_request_url(self) -> str:
        return "%s%s" % (self.__base, self.__data_products_request)

    # conjunctions
    # -------------------
    @property
    def conjunction_search_url(self) -> str:
        return f"{self.__base}{self.__conjunction_search}"

    @property
    def conjunction_request_url(self) -> str:
        return f"{self.__base}{self.__conjunction_request}"


# create instance of URLs that will be used throughout the application
urls = URLs()


def set_base_url(url: str) -> None:
    """
    Change the base URL for the API (ie. change to the staging system or local server).

    Attributes:
        url: new base url string (ie. 'https://api.staging.aurorax.space').

    """
    urls.base_url = url


def get_base_url() -> str:
    """
    Returns the current base URL for the API.
    """
    return urls.base_url


def reset_base_url() -> None:
    """
    Set the base URL for the API back to the default.
    """
    urls.base_url = DEFAULT_URL_BASE
