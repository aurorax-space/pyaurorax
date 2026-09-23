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
from pyaurorax.exceptions import AuroraXError, AuroraXAPIError


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

    # ATM calculations go through the UCalgary SRS API; test against staging server
    aurorax.srs_obj.api_base_url = "https://api-staging.phys.ucalgary.ca"

    # perform the calculation
    result = aurorax.models.atm.forward(timestamp, latitude, longitude, output, maxwellian_energy_flux=10.0, maxwellian_characteristic_energy=5000.0)

    # check
    assert isinstance(result, ATMForwardResult) is True


def __hir(aurorax, **kw):
    aurorax.srs_obj.api_base_url = "https://api-staging.phys.ucalgary.ca"
    output = ATMForwardOutputFlags()
    output.enable_only_height_integrated_rayleighs()
    r = aurorax.models.atm.forward(datetime.datetime(2025, 3, 20, 9, 0, 0), 60.0, -105.0, output, oxygen_correction_factor=0.5, no_cache=True, **kw)
    return [
        r.height_integrated_rayleighs_4278, r.height_integrated_rayleighs_5577, r.height_integrated_rayleighs_6300, r.height_integrated_rayleighs_8446
    ]


@pytest.mark.models
def test_forward_maxwellian_mean_energy(aurorax):
    by_mean = __hir(aurorax, maxwellian_energy_flux=2.0, maxwellian_mean_energy=4000.0)
    by_char = __hir(aurorax, maxwellian_energy_flux=2.0, maxwellian_characteristic_energy=2000.0)
    assert by_mean == pytest.approx(by_char, rel=1e-4)


@pytest.mark.models
def test_forward_both_maxwellian_energies(aurorax):
    with pytest.raises(AuroraXError, match="Only one of"):
        __hir(aurorax, maxwellian_energy_flux=2.0, maxwellian_mean_energy=4000.0, maxwellian_characteristic_energy=2000.0)


@pytest.mark.models
def test_forward_no_spectrum(aurorax):
    with pytest.raises(AuroraXAPIError, match="No precipitation spectrum specified"):
        __hir(aurorax)
