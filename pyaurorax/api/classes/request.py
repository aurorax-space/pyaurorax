"""
Class definition used for managing an API request
"""

import json
import requests
from pydantic import BaseModel
from typing import Optional, Dict, List, Union
from ..._internal.util import json_converter
from .response import AuroraXResponse
from ..api import get_api_key
from ...import __version__
from ...exceptions import (AuroraXMaxRetriesException,
                           AuroraXUnauthorizedException,
                           AuroraXNotFoundException,
                           AuroraXUnexpectedContentTypeException,
                           AuroraXUnexpectedEmptyResponse,
                           AuroraXException,
                           AuroraXTimeoutException)

# pdoc init
__pdoc__: Dict = {}

# request globals
DEFAULT_RETRIES: int = 2
""" Number of retry attempts when requesting data from the API """

REQUEST_HEADERS: Dict = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "python-pyaurorax/%s" % (__version__),
}
""" The default headers sent as part of a request to the AuroraX API """

REQUEST_TIMEOUT = 60
""" Default request timeout, in seconds """

API_KEY_HEADER_NAME: str = "x-aurorax-api-key"
""" The API key header used when sending requests to the AuroraX API """


class AuroraXRequest(BaseModel):
    """
    AuroraX API request class

    Attributes:
        url: the URL to make the request against
        method: the HTTP method to use (get, post, put, delete, etc.)
        params: any URL parameters to send in the request, defaults to {}
        body: the body of the request (ie. post data), defaults to {}
        headers: any headers to send as part of the request (in addition to the default ones), default is {}
        null_response: signifies if we expect a response from the API that has no
            body/data in it (ie. requests to upload data that respond with just a
            202 status code), defaults to False
    """
    url: str
    method: str
    params: Optional[Dict] = {}
    body: Union[Optional[Dict], Optional[List]] = {}
    headers: Optional[Dict] = {}
    null_response: Optional[bool] = False

    def __merge_headers(self):
        # set initial headers
        all_headers = REQUEST_HEADERS

        # add headers passed into the class
        for key, value in self.headers.items():
            all_headers[key] = value

        # add api key
        api_key = get_api_key()
        if api_key:
            all_headers[API_KEY_HEADER_NAME] = api_key

        # return
        return all_headers

    def execute(self,
                limited_evaluation: Optional[bool] = False,
                skip_retry_logic: Optional[bool] = False) -> AuroraXResponse:
        """
        Execute an AuroraX request

        Args:
            limited_evaluation: don't evaluate the response after the retry
                mechanism, defaults to False
            skip_retry_logic: exclude the retry logic in the request, defaults
                to False

        Returns:
            an AuroraXResponse object

        Raises:
            pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error
            pyaurorax.exceptions.AuroraXNotFoundException: requested resource was not found
            pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected content error
            pyaurorax.exceptions.AuroraXUnexpectedEmptyResponse: unexpected empty response
            pyaurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation
        """
        # sanitize data
        body_santized = json.dumps(self.body, default=json_converter)

        # make request
        try:
            req = requests.request(self.method,
                                   self.url,
                                   headers=self.__merge_headers(),
                                   params=self.params,
                                   data=body_santized,
                                   timeout=REQUEST_TIMEOUT)
        except requests.exceptions.Timeout:
            raise AuroraXTimeoutException("Error 408: request timeout reached")

        # retry request if needed
        if (skip_retry_logic is False):
            for i in range(0, DEFAULT_RETRIES):
                if (req.status_code == 500 and "text/plain" in req.headers["Content-Type"]):
                    if (i == (DEFAULT_RETRIES - 1)):
                        raise AuroraXMaxRetriesException("%s (%s)" % (req.content.decode(),
                                                                      req.status_code))
                    try:
                        req = requests.request(self.method,
                                               self.url,
                                               headers=self.__merge_headers(),
                                               params=self.params,
                                               json=self.body,
                                               data=body_santized,
                                               timeout=REQUEST_TIMEOUT)
                    except requests.exceptions.Timeout:
                        raise AuroraXTimeoutException("Error 408: request timeout reached")
                else:
                    break

        # check if authorization worked (raised by API or by Nginx)
        if (req.status_code == 401):
            if (req.headers["Content-Type"] == "application/json"):
                if ("error_message" in req.json()):
                    # this will be an error message that the API meant to send
                    raise AuroraXUnauthorizedException("%s %s" % (req.status_code,
                                                                  req.json()["error_message"]))
                else:
                    raise AuroraXUnauthorizedException("Error 401: unauthorized")
            else:
                raise AuroraXUnauthorizedException("Error 401: unauthorized")

        # check for 404 error (raised by API or by Nginx)
        if (req.status_code == 404):
            if (req.headers["Content-Type"] == "application/json"):
                if ("error_message" in req.json()):
                    # this will be an error message that the API meant to send
                    raise AuroraXNotFoundException("%s %s" % (req.status_code,
                                                              req.json()["error_message"]))
                else:
                    # this will likely be a 404 from the java servlet
                    raise AuroraXNotFoundException("Error 404: not found")
            else:
                raise AuroraXNotFoundException("Error 404: not found")

        # check if we only want to do limited evaluation
        if (limited_evaluation is True):
            res = AuroraXResponse(request=req,
                                  data=None,
                                  status_code=req.status_code)
            return res

        # check content type
        if (self.null_response is False):
            if (req.headers["Content-Type"] == "application/json"):
                if (len(req.content) == 0):
                    raise AuroraXUnexpectedEmptyResponse("No response received")
                else:
                    response_data = req.json()
            else:
                raise AuroraXUnexpectedContentTypeException("%s (%s)" % (req.content.decode(),
                                                                         req.status_code))
        else:
            if (req.status_code in [200, 201, 202, 204]):
                response_data = None
            else:
                response_data = req.json()

        # check for server error
        if (req.status_code == 500):
            response_json = req.json()
            if ("error_message" in response_json):
                raise AuroraXException("%s (%s)" % (response_json["error_message"],
                                                    req.status_code))
            else:
                raise AuroraXException(response_json)

        # create response object
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
        return f"AuroraXRequest(method='{self.method}', url='{self.url}')"
