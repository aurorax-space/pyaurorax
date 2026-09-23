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
from pyaurorax.models import ATMInverseOutputFlags, ATMInverseResult
from pyaurorax.exceptions import AuroraXError


@pytest.mark.models
def test_inverse(aurorax):
    # set up output flags
    output = ATMInverseOutputFlags()
    output.energy_flux = True
    output.mean_energy = True
    output.oxygen_correction_factor = True

    # set up lat, lon, timestamp
    timestamp = datetime.datetime(2021, 11, 4, 6, 0, 0)
    latitude = 58.227808
    longitude = -103.680631

    # set up input intensities
    intensity_4278 = 2302.6
    intensity_5577 = 11339.5
    intensity_6300 = 528.3
    intensity_8446 = 427.4

    # ATM calculations go through the UCalgary SRS API; test against staging server
    aurorax.srs_obj.api_base_url = "https://api-staging.phys.ucalgary.ca"

    # perform the calculation
    result = aurorax.models.atm.inverse(timestamp,
                                        latitude,
                                        longitude,
                                        intensity_4278,
                                        intensity_5577,
                                        intensity_6300,
                                        intensity_8446,
                                        output,
                                        precipitation_flux_spectral_type="maxwellian")
    # check
    assert isinstance(result, ATMInverseResult) is True


@pytest.mark.models
def test_inverse_spectral_type_required(aurorax):
    aurorax.srs_obj.api_base_url = "https://api-staging.phys.ucalgary.ca"
    output = ATMInverseOutputFlags()
    output.mean_energy = True
    args = (datetime.datetime(2025, 3, 20, 9, 0, 0), 60.0, -105.0, 499.27, 3036.96, 643.31, 287.61, output)
    with pytest.raises(TypeError):
        aurorax.models.atm.inverse(*args)  # type: ignore
    with pytest.raises(AuroraXError, match="required"):
        aurorax.models.atm.inverse(*args, precipitation_flux_spectral_type=None)  # type: ignore
