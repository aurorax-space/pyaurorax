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
import numpy as np


@pytest.mark.tools
def test_known_value(at):
    lats, lons = at.geocentric_to_geodetic([60.0], [-120.0], altitude_km=100.0)
    assert abs(lats[0] - 60.164) < 0.01
    assert abs(lons[0] - (-120.0)) < 1e-6


@pytest.mark.tools
def test_invariants(at):
    lats, _ = at.geocentric_to_geodetic([0.0, 90.0], [45.0, 0.0])
    assert abs(lats[0]) < 1e-9
    assert abs(lats[1] - 90.0) < 1e-9


@pytest.mark.tools
def test_nan_passthrough(at):
    lats, lons = at.geocentric_to_geodetic([60.0, np.nan], [-120.0, -120.0])
    assert np.isfinite(lats[0])
    assert np.isnan(lats[1])


@pytest.mark.tools
def test_shape_mismatch(at):
    with pytest.raises(ValueError):
        at.geocentric_to_geodetic([60.0, 61.0], [-120.0])
