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
Interface for AuroraX API requests. Primarily an under-the-hood module 
not needed for most use-cases.
"""

from .classes.request import AuroraXAPIRequest
from .classes.response import AuroraXAPIResponse

URL_SUFFIX_DATA_SOURCES = "api/v1/data_sources"
URL_SUFFIX_DATA_SOURCES_SEARCH = "/api/v1/data_sources/search"
URL_SUFFIX_EPHEMERIS_AVAILABILITY = "api/v1/availability/ephemeris"
URL_SUFFIX_EPHEMERIS_UPLOAD = "api/v1/data_sources/{}/ephemeris"
URL_SUFFIX_EPHEMERIS_SEARCH = "api/v1/ephemeris/search"
URL_SUFFIX_EPHEMERIS_REQUEST = "api/v1/ephemeris/requests/{}"
URL_SUFFIX_DATA_PRODUCTS_AVAILABILITY = "api/v1/availability/data_products"
URL_SUFFIX_DATA_PRODUCTS_UPLOAD = "api/v1/data_sources/{}/data_products"
URL_SUFFIX_DATA_PRODUCTS_SEARCH = "api/v1/data_products/search"
URL_SUFFIX_DATA_PRODUCTS_REQUEST = "api/v1/data_products/requests/{}"
URL_SUFFIX_CONJUNCTION_SEARCH = "api/v1/conjunctions/search"
URL_SUFFIX_CONJUNCTION_REQUEST = "api/v1/conjunctions/requests/{}"
URL_SUFFIX_DESCRIBE_CONJUNCTION_QUERY = "api/v1/utils/describe/query/conjunction"
URL_SUFFIX_DESCRIBE_DATA_PRODUCTS_QUERY = "api/v1/utils/describe/query/data_products"
URL_SUFFIX_DESCRIBE_EPHEMERIS_QUERY = "api/v1/utils/describe/query/ephemeris"
URL_SUFFIX_LIST_REQUESTS = "api/v1/utils/admin/search_requests"
URL_SUFFIX_DELETE_REQUESTS = "api/v1/utils/admin/search_requests/{}"

__all__ = [
    "AuroraXAPIRequest",
    "AuroraXAPIResponse",
]
