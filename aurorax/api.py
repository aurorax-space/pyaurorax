import requests
import datetime
from typing import Dict

# private globals
__URL_STUB = "http://api.staging.aurorax.space:8080"

# public globals
URL_EPHEMERIS_SOURCES = "%s/api/v1/ephemeris-sources" % (__URL_STUB)
URL_EPHEMERIS_AVAILABILITY = "%s/api/v1/availability" % (__URL_STUB)
URL_DATA_PRODUCTS_AVAILABILITY = "%s/api/v1/availability" % (__URL_STUB)
URL_EPHEMERIS_UPLOAD = "%s/api/v1/ephemeris-sources/{}/ephemeris" % (__URL_STUB)
URL_EPHEMERIS_SEARCH = "%s/api/v1/ephemeris/search" % (__URL_STUB)
URL_EPHEMERIS_REQUEST_STATUS = "%s/api/v1/ephemeris/requests/{}" % (__URL_STUB)


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
        req = requests.request(
            self.method, self.url, params=self.params, json=self.json, headers=request_headers)

        # create response object
        res = AuroraXResponse(req)

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
        req = requests.request(
            self.method, self.url, params=self.params, json=self.json, headers=request_headers)

        # return
        return req


class AuroraXResponse():

    def __init__(self, request: AuroraXRequest) -> None:
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


def get_request_status(url: str) -> Dict:
    # get request status
    req = AuroraXRequest(url)
    res = req.execute()

    # set return dict
    return_dict = {
        "status_code": res.status_code,
        "data": {},
        "request_status": {
            "completed": False,
            "data_url": ""
        }
    }

    # determine the status of the request
    if (res.status_code == 200):
        return_dict["data"] = res.data
        if (res.data["search_result"]["data_uri"] is not None):
            return_dict["request_status"]["completed"] = True
            return_dict["request_status"]["data_url"] = "%s%s" % (__URL_STUB, res.data["search_result"]["data_uri"])

    # return
    return return_dict


def get_request_data(url: str) -> Dict:
    # make request
    req = AuroraXRequest(url)
    res = req.execute()

    # set return dict
    return_dict = {
        "status_code": res.status_code,
        "data": []
    }
    if (res.status_code == 200):
        return_dict["data"] = res.data

    # serialize epochs to datetime objects
    for i in range(0, len(return_dict["data"])):
        if ("epoch" in return_dict["data"][i]):
            return_dict["data"][i]["epoch"] = datetime.datetime.strptime(return_dict["data"][i]["epoch"],
                                                                         "%Y-%m-%dT%H:%M:%S")

    # return
    return return_dict
