import requests
import aurorax
import pprint
import json
from typing import Optional, Dict, Any, List, Union
from pydantic import BaseModel
from .._internal.util import json_converter

# reqest globals
DEFAULT_RETRIES = 2
REQUEST_HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json"
}
API_KEY_HEADER_NAME = "x-aurorax-api-key"

# private dynamic globals
__api_key = ""


def get_api_key():
    return __api_key


def authenticate(api_key: str) -> int:
    """
    Set authentication values for use with subsequent queries

    :param api_key: api key
    :type api_key: str

    :return: 0
    :rtype: int
    """

    # set the global variable
    global __api_key
    __api_key = api_key

    # return
    return 0


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
        if (api_key is not None):
            all_headers[API_KEY_HEADER_NAME] = api_key

        # return
        return all_headers

    def execute(self, limited_evaluation: bool = False) -> AuroraXResponse:
        """Execute an AuroraX request

        :param limited_evaluation: set true if you don't want to evaluate the response outside of
                                   the retry mechanism, defaults to False
        :type limited_evaluation: bool, optional

        :raises aurorax.AuroraXMaxRetriesException: max retry error
        :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected content error

        :return: response
        :rtype: AuroraXResponse
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
        for i in range(0, aurorax.api.DEFAULT_RETRIES):
            if (req.status_code == 500 and "text/plain" in req.headers["Content-Type"]):
                if (i == (aurorax.api.DEFAULT_RETRIES - 1)):
                    raise aurorax.AuroraXMaxRetriesException("%s (%s)" % (req.content.decode(),
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
            raise aurorax.AuroraXUnauthorizedException("%s %s" % (req.status_code,
                                                                  req.json()["error_message"]))

        # check if we only want to do limited evaluation
        if (limited_evaluation is True):
            res = AuroraXResponse(request=req, data=None, status_code=req.status_code)
            return res

        # check content type
        if (self.null_response is False):
            if (req.headers["Content-Type"] == "application/json"):
                response_data = req.json()
            else:
                raise aurorax.AuroraXUnexpectedContentTypeException("%s (%s)" % (req.content.decode(),
                                                                                 req.status_code))
        else:
            if (req.status_code != 200 and req.status_code != 201 and req.status_code != 202):
                response_data = req.json()
            else:
                response_data = None

        # check for server error
        if (req.status_code == 500):
            response_json = req.json()
            if ("error_message" in response_json):
                raise aurorax.AuroraXException("%s (%s)" % (response_json["error_message"],
                                                            req.status_code))
            else:
                raise aurorax.AuroraXException(response_json)

        # create reponse object
        res = AuroraXResponse(request=req, data=response_data, status_code=req.status_code)

        # return
        return res

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
