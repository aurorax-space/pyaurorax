import requests

# public globals
URL_EPHEMERIS_SOURCES = "http://staging-zaphod-api.aurorax.space/api/v1/ephemeris-sources"


class AuroraXRequest():

    # private globals
    __STANDARD_REQUEST_HEADERS = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    def __init__(self, url, params={}, json={}, method="GET", api_key=""):
        # set attributes
        self.json = json
        self.params = params
        self.method = method.upper()
        self.url = url
        self.api_key = api_key

    def execute(self):
        # prep request headers
        request_headers = self.__STANDARD_REQUEST_HEADERS
        if (self.api_key != ""):
            request_headers["x-aurorax-api-key": self.api_key]

        # perform request
        req = requests.request(self.method, self.url, params=self.params, json=self.json)

        # serialize response into an AuroraXResponse object
        # TODO  --> once async version of API is available
        #           to work with, then implement the
        #           differentiation between the two types
        #           of requests
        res = AuroraXResponse(req, asynchronous=False)

        # return
        return res


class AuroraXResponse():

    # private globals
    __STR_DATA_LENGTH = 75

    def __init__(self, request, asynchronous=False):
        # init values
        self.headers = {}
        self.request = request
        self.data = None
        self.asynchronous = asynchronous
        self.status_code = request.status_code

        # if synchronous, set response values
        if (self.asynchronous is False):
            self.headers = self.request.headers
            self.data = self.request.json()

    # async request method
    # TODO   --> implement once async API version is available
    def check_for_data(self):
        pass

    def __str__(self):
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
