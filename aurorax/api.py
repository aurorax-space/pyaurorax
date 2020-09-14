import requests
from typing import Dict

# private globals
__URL_STUB = "http://staging-zaphod-api.aurorax.space"

# public globals
URL_EPHEMERIS_SOURCES = "%s/api/v1/ephemeris-sources" % (__URL_STUB)
URL_EPHEMERIS_AVAILABILITY = "%s/api/v1/availability" % (__URL_STUB)
URL_DATA_PRODUCTS_AVAILABILITY = "%s/api/v1/availability" % (__URL_STUB)
URL_EPHEMERIS_UPLOAD = "%s/api/v1/ephemeris-sources/{}/ephemeris" % (__URL_STUB)


class AuroraXRequest():

    # private globals
    __STANDARD_REQUEST_HEADERS = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    def __init__(self, url: str, params: Dict = {}, json: Dict = {}, method: str = "GET", api_key: str = "") -> None:
        # set attributes
        self.json = json
        self.params = params
        self.method = method.upper()
        self.url = url
        self.api_key = api_key

    def execute(self) -> "AuroraXResponse":
        # prep request headers
        request_headers = self.__STANDARD_REQUEST_HEADERS
        if (self.api_key != ""):
            request_headers["x-aurorax-api-key"] = self.api_key

        # perform request
        req = requests.request(self.method, self.url, params=self.params, json=self.json, headers=request_headers)

        # serialize response into an AuroraXResponse object
        # TODO  --> once async version of API is available
        #           to work with, then implement the
        #           differentiation between the two types
        #           of requests
        res = AuroraXResponse(req, asynchronous=False)

        # return
        return res


class AuroraXRawRequest(AuroraXRequest):

    # private globals
    __STANDARD_REQUEST_HEADERS = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    def execute(self) -> requests.Request:
        # prep request headers
        request_headers = self.__STANDARD_REQUEST_HEADERS
        if (self.api_key != ""):
            request_headers["x-aurorax-api-key"] = self.api_key

        # perform request
        req = requests.request(self.method, self.url, params=self.params, json=self.json, headers=request_headers)

        # return
        return req


class AuroraXResponse():

    # private globals
    __STR_DATA_LENGTH = 115

    def __init__(self, request: AuroraXRequest, asynchronous: bool = False) -> None:
        # init values
        self.headers = {}
        self.request = request
        self.data = None
        self.asynchronous = asynchronous
        self.status_code = request.status_code

        # if synchronous, set response values
        if (self.asynchronous is False):
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

    # async request method
    # TODO   --> implement once async API version is available
    def check_for_data(self) -> None:
        pass

    def __str__(self) -> str:
        # update status if asynchronous
        if (self.asynchronous is True):
            self.check_for_data()

        # status code
        ret_str = "status_code: %d\n" % (self.status_code)

        # data
        if (len(str(self.data)) > self.__STR_DATA_LENGTH):
            ret_str += "data: %s ..." % (str(self.data)[0:self.__STR_DATA_LENGTH])
        else:
            ret_str += "data: %s" % (str(self.data))

        # return
        return ret_str
