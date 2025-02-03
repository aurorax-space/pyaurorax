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
from pyaurorax.search import Location


@pytest.mark.search_ro
def test_create_location_object():
    loc = Location(lat=51, lon=-110)
    assert loc.lat == 51.0 and loc.lon == -110.0

    print_str = print(loc)
    assert print_str != ""


@pytest.mark.search_ro
def test_create_empty_location_object():
    loc = Location(lat=None, lon=None)
    assert loc.lat is None and loc.lon is None


@pytest.mark.search_ro
def test_create_invalid_location_object():
    with pytest.raises(ValueError):
        Location(lat=51, lon=None)
