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

import pytest


@pytest.mark.search_ro
def test_get_request_url(aurorax):
    request_id = "testing-request-id"
    expected_url = aurorax.api_base_url + "/api/v1/conjunctions/requests/" + request_id
    returned_url = aurorax.search.conjunctions.get_request_url(request_id)
    assert returned_url == expected_url
