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
import datetime
from pyaurorax.exceptions import AuroraXUnauthorizedError


@pytest.mark.search_ro
def test_simple(aurorax):
    # list requests
    requests = aurorax.search.requests.list(
        search_type="conjunction",
        start=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1),
        end=datetime.datetime.now(datetime.timezone.utc),
    )
    assert len(requests) > 0


@pytest.mark.search_ro
def test_many_filters(aurorax):
    # list requests
    requests = aurorax.search.requests.list(search_type="conjunction",
                                            start=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1),
                                            end=datetime.datetime.now(datetime.timezone.utc),
                                            active=True,
                                            file_size=1000,
                                            result_count=10,
                                            query_duration=1,
                                            error_condition=False)
    assert len(requests) > 0


@pytest.mark.search_ro
def test_bad_type(aurorax):
    # list requests
    with pytest.raises(ValueError) as e_info:
        aurorax.search.requests.list(
            search_type="some-bad-type",
            start=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1),
            end=datetime.datetime.now(datetime.timezone.utc),
        )
    assert "is not one that PyAuroraX knows about" in str(e_info)


@pytest.mark.search_ro
def test_no_api_key(aurorax):
    # remove api key
    aurorax.api_key = None

    # list requests
    with pytest.raises(AuroraXUnauthorizedError) as e_info:
        aurorax.search.requests.list(
            search_type="conjunction",
            start=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1),
            end=datetime.datetime.now(datetime.timezone.utc),
        )
    assert "An Administrator API key was not detected, and is required for this function" in str(e_info)
