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
from pyaurorax.models import ATMForwardOutputFlags, ATMForwardResult


@pytest.mark.models
def test_forward(aurorax):
    # set up output flags
    output = ATMForwardOutputFlags()
    output.enable_only_height_integrated_rayleighs()
    output.altitudes = True
    output.emission_5577 = True

    # set up lat, lon, time
    latitude = 51.04
    longitude = -114.5
    timestamp = datetime.datetime.now().replace(hour=6, minute=0, second=0, microsecond=0) - datetime.timedelta(days=1)

    # perform the calculation
    result = aurorax.models.atm.forward(timestamp, latitude, longitude, output)

    # check
    assert isinstance(result, ATMForwardResult) is True
