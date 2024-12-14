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
Class definition for an AuroraX API response
"""

from typing import Any
from http.client import responses


class AuroraXAPIResponse:
    """
    Class definition for an AuroraX API response

    Attributes:
        request (Any): the request object
        data (Any): the data received as part of the request
        status_code (int): the HTTP status code received when making the request
    """

    def __init__(self, request: Any, data: Any, status_code: int):
        self.request = request
        self.data = data
        self.status_code = status_code

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"AuroraXAPIResponse [{self.status_code}] ({responses[self.status_code]})"
