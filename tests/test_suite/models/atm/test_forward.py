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
from pyaurorax.models import ATMForwardOutputFlags, ATMInverseOutputFlags, ATMInverseResult, ATMForwardResult


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


@pytest.mark.models
def test_inverse(aurorax):
    # set up output flags
    output = ATMInverseOutputFlags()
    output.energy_flux = True
    output.characteristic_energy = True
    output.oxygen_correction_factor = True

    # set up lat, lon, timestamp
    timestamp = datetime.datetime(2021, 10, 12, 6, 0, 0)
    latitude = 58.227808
    longitude = -103.680631

    # set up input intensities
    intensity_4278 = 2302.6
    intensity_5577 = 11339.5
    intensity_6300 = 528.3
    intensity_8446 = 427.4

    # perform the calculation
    result = aurorax.models.atm.inverse(timestamp, latitude, longitude, intensity_4278, intensity_5577, intensity_6300, intensity_8446, output)

    # check
    assert isinstance(result, ATMInverseResult) is True
