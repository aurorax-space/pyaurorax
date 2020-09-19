import requests
from typing import Dict

# public globals
URL_API_STUB = "http://api.staging.aurorax.space"
URL_EPHEMERIS_SOURCES = "%s/api/v1/ephemeris-sources" % (URL_API_STUB)
URL_EPHEMERIS_AVAILABILITY = "%s/api/v1/availability" % (URL_API_STUB)
URL_DATA_PRODUCTS_AVAILABILITY = "%s/api/v1/availability" % (URL_API_STUB)
URL_EPHEMERIS_UPLOAD = "%s/api/v1/ephemeris-sources/{}/ephemeris" % (URL_API_STUB)
URL_EPHEMERIS_SEARCH = "%s/api/v1/ephemeris/search" % (URL_API_STUB)
URL_EPHEMERIS_REQUEST_STATUS = "%s/api/v1/ephemeris/requests/{}" % (URL_API_STUB)


class AuroraXRequest():
    """
    Class to streamline performing a synchronous or asynchronous request against the AuroraX API
    """

    # private globals
    __STANDARD_REQUEST_HEADERS = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    def __init__(self, url: str, params: Dict = {}, json: Dict = {}, method: str = "GET", api_key: str = "") -> None:
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
        req = requests.request(
            self.method, self.url, params=self.params, json=self.json, headers=request_headers)

        # create response object
        res = AuroraXResponse(req)

        # return
        return res


class AuroraXRawRequest(AuroraXRequest):
    """
    Class to run a raw AuroraX API request and not wrap as an AuroraXResponse object
    """

    # private globals
    __STANDARD_REQUEST_HEADERS = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    def execute(self) -> requests.Request:
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
        req = requests.request(
            self.method, self.url, params=self.params, json=self.json, headers=request_headers)

        # return
        return req


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
