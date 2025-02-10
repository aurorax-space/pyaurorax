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


@pytest.mark.tools
@pytest.mark.parametrize("elevation", [40, 90, 10, 70, 87])
def test_simple(at, ccd_contour_data, elevation):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    elev_x, elev_y = at.ccd_contour.elevation(skymap_data, elevation)
    assert len(elev_x) > 0
    assert len(elev_y) > 0


@pytest.mark.tools
def test_n_points(at, ccd_contour_data):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    elev_x, elev_y = at.ccd_contour.elevation(skymap_data, 40, n_points=10)
    assert len(elev_x) > 0
    assert len(elev_y) > 0


@pytest.mark.tools
def test_no_remove_edge_cases(at, ccd_contour_data):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    azim_x, azim_y = at.ccd_contour.elevation(skymap_data, 40, remove_edge_cases=False)
    assert len(azim_x) > 0
    assert len(azim_y) > 0


@pytest.mark.tools
def test_bad_elevation(at, ccd_contour_data):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    with pytest.raises(ValueError) as e_info:
        at.ccd_contour.elevation(skymap_data, -10)
    assert "Elevation" in str(e_info) and "is outside of valid range" in str(e_info)
    with pytest.raises(ValueError) as e_info:
        at.ccd_contour.elevation(skymap_data, 100)
    assert "Elevation" in str(e_info) and "is outside of valid range" in str(e_info)
