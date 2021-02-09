import requests as _requests
import pprint as _pprint
from typing import Dict as _Dict

# public globals
_URL_API_STUB = "http://api.aurorax.space"
URL_DATA_SOURCES = "%s/api/v1/data-sources" % (_URL_API_STUB)
URL_EPHEMERIS_AVAILABILITY = "%s/api/v1/availability/ephemeris" % (_URL_API_STUB)
URL_EPHEMERIS_UPLOAD = "%s/api/v1/data-sources/{}/ephemeris" % (_URL_API_STUB)
URL_EPHEMERIS_SEARCH = "%s/api/v1/ephemeris/search" % (_URL_API_STUB)
URL_EPHEMERIS_REQUEST_STATUS = "%s/api/v1/ephemeris/requests/{}" % (_URL_API_STUB)
URL_DATA_PRODUCTS_AVAILABILITY = "%s/api/v1/availability/data_products" % (_URL_API_STUB)
URL_DATA_PRODUCTS_UPLOAD = "%s/api/v1/data-sources/{}/data_products" % (_URL_API_STUB)
URL_DATA_PRODUCTS_SEARCH = "%s/api/v1/data_products/search" % (_URL_API_STUB)
URL_DATA_PRODUCTS_REQUEST_STATUS = "%s/api/v1/data_products/requests/{}" % (_URL_API_STUB)


class AuroraXRequest():
    """
    Class to streamline performing a synchronous or asynchronous request against the AuroraX API
    """

    # private globals
    __STANDARD_REQUEST_HEADERS = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    def __init__(self, url: str, params: _Dict = {}, json: _Dict = {}, method: str = "GET", api_key: str = "") -> None:
        """
        AuroraXRequest constructor

        :param url: AuroraX RESTful API endpoint URL
        :type url: str
        :param params: URL parameters to be included in the request
        :type params: Dict, optional
        :param json: JSON data to include in the request (ie. POST data), defaults to {}
        :type json: Dict, optional
        :param method: HTTP method (GET, POST, PUT, DELETE), defaults to "GET"
        :type method: str, optional
        :param api_key: AuroraX API key for endpoints requiring authorization, defaults to ""
        :type api_key: str, optional
        """
        # set attributes
        self.json = json
        self.params = params
        self.method = method.upper()
        self.url = url
        self.api_key = api_key

    def execute(self) -> "AuroraXResponse":
        """
        Initiate ephemeris search request

        :return: AuroraXReponse object for this request
        :rtype: AuroraXResponse
        """
        # prep request headers
        request_headers = self.__STANDARD_REQUEST_HEADERS
        if (self.api_key != ""):
            request_headers["x-aurorax-api-key"] = self.api_key

        # perform request
        req = _requests.request(self.method, self.url, params=self.params, json=self.json, headers=request_headers)

        # create response object
        res = AuroraXResponse(req)

        # return
        return res

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return _pprint.pformat(self.__dict__)


class AuroraXRawRequest(AuroraXRequest):
    """
    Class to run a raw AuroraX API request and not wrap as an AuroraXResponse object
    """

    # private globals
    __STANDARD_REQUEST_HEADERS = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    def execute(self) -> _requests.Request:
        """
        Initiate ephemeris search request

        :return: requests.Request object for this request
        :rtype: requests.Request
        """
        # prep request headers
        request_headers = self.__STANDARD_REQUEST_HEADERS
        if (self.api_key != ""):
            request_headers["x-aurorax-api-key"] = self.api_key

        # perform request
        req = _requests.request(self.method, self.url, params=self.params, json=self.json, headers=request_headers)

        # return
        return req

    def __str__(self) -> str:
        """String method

        :return: string format
        :rtype: str
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation

        :return: object representation
        :rtype: str
        """
        return _pprint.pformat(self.__dict__)


class AuroraXResponse():
    """
    Class containing the response information for an AuroraXRequest
    object.
    """

    def __init__(self, request: AuroraXRequest) -> None:
        """
        Constructor

        :param request: AuroraXResponse object associated with this response
        :type request: AuroraXRequest
        """
        # init values
        self.headers = {}
        self.request = request
        self.data = None
        self.status_code = request.status_code

        # set response values
        self.headers = self.request.headers
        if (self.status_code >= 200 and self.status_code < 300):
            if (self.request.text == ""):
                self.data = ""
            else:
                self.data = self.request.json()
        else:
            self.data = {
                "error": "HTTP error code %d" % (self.status_code),
                "response_body": self.request.text,
            }

    def __str__(self) -> str:
        """String method

        :return: string format
        :rtype: str
        """
        dict = self.__dict__
        if (dict["data"] is not None):
            dict["data"] = "..."
        return _pprint.pformat(dict)

    def __repr__(self) -> str:
        """
        Object representation

        :return: object representation
        :rtype: str
        """
        return "<AuroraXResponse [%d]>" % (self.status_code)


def set_url_stub(stub: str) -> None:
    """
    Change the URL stub for the API. For example if you want to migrate
    data from one endpointt to another.

    :param stub: URL stub (ie. http://api.staging.aurorax.space)
    :type stub: str
    """
    global _URL_API_STUB
    global URL_DATA_SOURCES
    global URL_EPHEMERIS_AVAILABILITY
    global URL_EPHEMERIS_UPLOAD
    global URL_EPHEMERIS_SEARCH
    global URL_EPHEMERIS_REQUEST_STATUS
    global URL_DATA_PRODUCTS_AVAILABILITY
    global URL_DATA_PRODUCTS_UPLOAD
    global URL_DATA_PRODUCTS_SEARCH
    global URL_DATA_PRODUCTS_REQUEST_STATUS

    _URL_API_STUB = stub
    URL_DATA_SOURCES = "%s/api/v1/data-sources" % (_URL_API_STUB)
    URL_EPHEMERIS_AVAILABILITY = "%s/api/v1/availability/ephemeris" % (_URL_API_STUB)
    URL_EPHEMERIS_UPLOAD = "%s/api/v1/data-sources/{}/ephemeris" % (_URL_API_STUB)
    URL_EPHEMERIS_SEARCH = "%s/api/v1/ephemeris/search" % (_URL_API_STUB)
    URL_EPHEMERIS_REQUEST_STATUS = "%s/api/v1/ephemeris/requests/{}" % (_URL_API_STUB)
    URL_DATA_PRODUCTS_AVAILABILITY = "%s/api/v1/availability/data_products" % (_URL_API_STUB)
    URL_DATA_PRODUCTS_UPLOAD = "%s/api/v1/data-sources/{}/data_products" % (_URL_API_STUB)
    URL_DATA_PRODUCTS_SEARCH = "%s/api/v1/data_products/search" % (_URL_API_STUB)
    URL_DATA_PRODUCTS_REQUEST_STATUS = "%s/api/v1/data_products/requests/{}" % (_URL_API_STUB)
