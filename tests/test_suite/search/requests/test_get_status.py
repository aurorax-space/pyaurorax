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
from pyaurorax.search import EphemerisSearch


@pytest.mark.search_ro
def test_get_request_status(aurorax):
    # start search
    r = EphemerisSearch(aurorax,
                        datetime.datetime(2020, 1, 1, 0, 0, 0),
                        datetime.datetime(2020, 1, 1, 1, 0, 0),
                        programs=["swarm"],
                        platforms=["swarma"],
                        instrument_types=["footprint"])
    r.execute()

    # sleep briefly
    r.wait()

    # get status
    status = aurorax.search.requests.get_status(r.request_url)
    assert status
