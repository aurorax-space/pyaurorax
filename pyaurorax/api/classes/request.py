"""
Class definition used for managing an API request
"""

import pyaurorax
import json
import pprint
import requests
from pydantic import BaseModel
from typing import Optional, Dict, List, Union
from ..._internal.util import json_converter
from .response import AuroraXResponse
from ..api import get_api_key

# pdoc init
__pdoc__: Dict = {}

# request globals
DEFAULT_RETRIES: int = 2
""" Number of retry attempts when requesting data from the API """

REQUEST_HEADERS: Dict = {
    "accept": "application/json",
    "Content-Type": "application/json"
}
""" The default headers sent as part of a request to the AuroraX API """

API_KEY_HEADER_NAME: str = "x-aurorax-api-key"
""" The API key header used when sending requests to the AuroraX API """


class AuroraXRequest(BaseModel):
    """
    AuroraX API request class
    """
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

    def execute(self, limited_evaluation: Optional[bool] = False) -> AuroraXResponse:
        """
        Execute an AuroraX request

        Args:
            limited_evaluation: set this to True if you don't want to evaluate
                the response outside of the retry mechanism, defaults to False

        Returns:
            an AuroraXResponse object

        Raises:
            pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error
            pyaurorax.exceptions.AuroraXNotFoundException: requested resource was not found
            pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected content error
            pyaurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation
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
            res = AuroraXResponse(request=req,
                                  data=None,
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
        res = AuroraXResponse(request=req,
                              data=response_data,
                              status_code=req.status_code)

        # return
        return res

    def __str__(self) -> str:
        """
        String method

        Returns:
            string format of AuroraXRequest
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation

        Returns:
            object representation of AuroraXRequest
        """
        return pprint.pformat(self.__dict__)
