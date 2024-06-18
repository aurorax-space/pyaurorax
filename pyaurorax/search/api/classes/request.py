# Copyright 2024 University of Calgary
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Class definition for an AuroraX API request
"""

import json
import requests
import datetime
from typing import Literal, Dict, List, Union
from ....exceptions import AuroraXAPIError, AuroraXUnauthorizedError, AuroraXMaintenanceError
from .response import AuroraXAPIResponse


class AuroraXAPIRequest:
    """
    Class definition for an AuroraX API request

    Attributes:
        url (str): API endpoint URL for the request
        method (str): the HTTP method to use. Valid values are: `get`, `post`, `put`, `delete`, `patch`
        params (Dict): URL parameters to send in the request, defaults to `{}`
        body (Dict): the body of the request (ie. post data), defaults to `{}`
        headers (Dict): any headers to send as part of the request (in addition to the default ones), defaults to `{}`
        null_response (bool): signifies if we expect a response from the API that has no body/data in it (ie. 
            requests to upload data that respond with just a 202 status code), defaults to `False`
    """

    __API_KEY_HEADER_NAME = "x-aurorax-api-key"

    def __init__(self,
                 aurorax_obj,
                 url: str,
                 method: Literal["get", "post", "put", "delete", "patch"],
                 params: Dict = {},
                 body: Union[List, Dict] = {},
                 headers: Dict = {},
                 null_response: bool = False):
        self.__aurorax_obj = aurorax_obj
        self.url = url
        self.method = method
        self.params = params
        self.body = body
        self.headers = headers
        self.null_response = null_response

    def __json_converter(self, o):
        if (isinstance(o, datetime.datetime) is True):
            return str(o)

    def __merge_headers(self):
        # set initial headers
        all_headers = self.__aurorax_obj.api_headers

        # add headers passed into the class
        for key, value in self.headers.items():
            all_headers[key.lower()] = value

        # add api key
        if self.__aurorax_obj.api_key:
            all_headers[self.__API_KEY_HEADER_NAME] = self.__aurorax_obj.api_key

        # return
        return all_headers

    def execute(self) -> AuroraXAPIResponse:
        """
        Execute an AuroraX API request
    
        Returns:
            an `pyaurorax.search.api.AuroraXAPIResponse` object

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: error during API call
        """
        # sanitize data
        body_santized = json.dumps(self.body, default=self.__json_converter)

        # make request
        try:
            req = requests.request(self.method,
                                   self.url,
                                   headers=self.__merge_headers(),
                                   params=self.params,
                                   data=body_santized,
                                   timeout=self.__aurorax_obj.api_timeout)
        except requests.exceptions.Timeout:
            raise AuroraXAPIError("API request timeout reached") from None

        # check if authorization worked (raised by API or Nginx)
        if (req.status_code == 401):
            if (req.headers["Content-Type"] == "application/json"):
                if ("error_message" in req.json()):
                    # this will be an error message that the API meant to send
                    raise AuroraXUnauthorizedError("API error code %d: %s" % (req.status_code, req.json()["error_message"]))
                else:
                    raise AuroraXUnauthorizedError("API error code 401: unauthorized")
            else:
                raise AuroraXUnauthorizedError("API error code 401: unauthorized")

        # check for 404 error (raised by API or by Nginx)
        if (req.status_code == 404):
            if (req.headers["Content-Type"] == "application/json"):
                if ("error_message" in req.json()):
                    # this will be an error message that the API meant to send
                    raise AuroraXAPIError("API error code %d: %s" % (req.status_code, req.json()["error_message"]))
                else:
                    # this will likely be a 404 from the API
                    raise AuroraXAPIError("API error code 404: not found")
            else:
                raise AuroraXAPIError("API error code 404: not found")

        # check for server error
        if (req.status_code == 500):
            response_json = req.json()
            if ("error_message" in response_json):
                raise AuroraXAPIError("API error code %d: %s" % (req.status_code, response_json["error_message"]))
            else:
                raise AuroraXAPIError("API error code %d: %s" % (req.status_code, response_json))

        # check for maintenance mode error
        if (req.status_code == 502):
            raise AuroraXAPIError("API error code %d: API inaccessible, bad gateway" % (req.status_code))

        # check for maintenance mode error
        if (req.status_code == 503):
            response_json = req.json()
            if ("maintenance mode" in response_json["error_message"].lower()):
                raise AuroraXMaintenanceError(response_json["error_message"])
            else:
                raise AuroraXAPIError("API error code %d: %s" % (req.status_code, response_json["error_message"]))

        # check content type
        if (self.null_response is False):
            if (req.headers["Content-Type"] == "application/json"):
                if (len(req.content) == 0):
                    raise AuroraXAPIError("API error code %d: no response received" % (req.status_code))
                else:
                    response_data = req.json()
            else:
                raise AuroraXAPIError("API error code %d: %s" % (req.status_code, req.content.decode()))
        else:
            if (req.status_code in [200, 201, 202, 204]):
                response_data = None
            else:
                response_data = req.json()

        # create response object
        res = AuroraXAPIResponse(request=req, data=response_data, status_code=req.status_code)

        # return
        return res

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"AuroraXAPIRequest(method='{self.method}', url='{self.url}')"
