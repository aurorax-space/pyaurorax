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
def test_simple(aurorax):
    start_dt = datetime.datetime(2018, 1, 1, 0, 0, 0)
    end_dt = datetime.datetime(2018, 1, 31, 23, 59, 59)
    programs = ["themis"]

    # do search
    s = EphemerisSearch(aurorax, start=start_dt, end=end_dt, programs=programs)
    s.execute()

    # cancel it
    result = aurorax.search.requests.cancel(s.request_url, wait=True, verbose=True)

    # check it was cancelled
    assert result == 0


@pytest.mark.search_ro
def test_no_wait(aurorax):
    start_dt = datetime.datetime(2018, 1, 1, 0, 0, 0)
    end_dt = datetime.datetime(2018, 1, 31, 23, 59, 59)
    programs = ["themis"]

    # do search
    s = EphemerisSearch(aurorax, start=start_dt, end=end_dt, programs=programs)
    s.execute()

    # cancel it
    aurorax.search.requests.cancel(s.request_url, wait=False)
