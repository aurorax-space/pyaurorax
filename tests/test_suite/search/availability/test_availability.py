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
from pyaurorax.search import AvailabilityResult


@pytest.mark.search_ro
def test_ephemeris_availability(aurorax):
    # set params
    start_date = datetime.datetime(2019, 1, 1)
    end_date = datetime.date(2019, 1, 2)
    program = "swarm"
    platform = "swarma"
    instrument_type = "footprint"

    # get availability
    availability = aurorax.search.availability.ephemeris(start_date,
                                                         end_date,
                                                         program=program,
                                                         platform=platform,
                                                         instrument_type=instrument_type,
                                                         slow=False)

    # check
    assert isinstance(availability, list) is True
    assert len(availability) > 0
    assert isinstance(availability[0], AvailabilityResult) is True
    assert availability[0].data_source.program == "swarm"


@pytest.mark.search_ro
def test_data_product_availability(aurorax):
    # set params
    start_date = datetime.datetime(2019, 1, 1)
    end_date = datetime.date(2019, 1, 2)
    program = "trex"
    instrument_type = "RGB ASI"

    # get availability
    availability = aurorax.search.availability.data_products(
        start_date,
        end_date,
        program=program,
        instrument_type=instrument_type,
        slow=True,
    )

    # check
    assert isinstance(availability, list) is True
    assert len(availability) > 0
    assert isinstance(availability[0], AvailabilityResult) is True
    assert availability[0].data_source.program == "trex"
