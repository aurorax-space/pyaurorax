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
from pyaurorax.search import EphemerisData


@pytest.mark.search_ro
def test_metadata_filters(aurorax):
    start = datetime.datetime(2008, 1, 1, 11, 0, 0)
    end = datetime.datetime(2008, 1, 1, 11, 59, 59)
    programs = ["themis-asi"]
    metadata_filters_logical_operator = "AND"
    metadata_filters = [{
        "key": "calgary_apa_ml_v1",
        "operator": "in",
        "values": ["classified as APA"]
    }, {
        "key": "calgary_apa_ml_v1_confidence",
        "operator": ">=",
        "values": ["95"]
    }]

    # perform the search
    s = aurorax.search.ephemeris.search(start=start,
                                        end=end,
                                        programs=programs,
                                        metadata_filters_logical_operator=metadata_filters_logical_operator,
                                        metadata_filters=metadata_filters)

    # check
    assert isinstance(s.data, list) is True
    assert len(s.data) > 0
    for e in s.data:
        assert isinstance(e, EphemerisData) is True
