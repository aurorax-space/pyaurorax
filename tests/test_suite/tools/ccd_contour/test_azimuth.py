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
def test_simple(at, ccd_contour_data):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    azim_x, azim_y = at.ccd_contour.azimuth(skymap_data, 45)
    assert len(azim_x) > 0
    assert len(azim_y) > 0


@pytest.mark.tools
def test_min_elevation(at, ccd_contour_data):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    azim_x, azim_y = at.ccd_contour.azimuth(skymap_data, 45, min_elevation=0)
    assert len(azim_x) > 0
    assert len(azim_y) > 0


@pytest.mark.tools
def test_max_elevation(at, ccd_contour_data):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    azim_x, azim_y = at.ccd_contour.azimuth(skymap_data, 45, max_elevation=70)
    assert len(azim_x) > 0
    assert len(azim_y) > 0


@pytest.mark.tools
def test_min_and_max_elevation(at, ccd_contour_data):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    azim_x, azim_y = at.ccd_contour.azimuth(skymap_data, 45, min_elevation=10, max_elevation=80)
    assert len(azim_x) > 0
    assert len(azim_y) > 0


@pytest.mark.tools
def test_azimuth_360(at, ccd_contour_data):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    azim_x, azim_y = at.ccd_contour.azimuth(skymap_data, 360)
    assert len(azim_x) > 0
    assert len(azim_y) > 0


@pytest.mark.tools
def test_n_points(at, ccd_contour_data):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    azim_x, azim_y = at.ccd_contour.azimuth(skymap_data, 45, n_points=10)
    assert len(azim_x) == 10
    assert len(azim_y) == 10


@pytest.mark.tools
def test_no_remove_edge_cases(at, ccd_contour_data):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    azim_x, azim_y = at.ccd_contour.azimuth(skymap_data, 45, remove_edge_cases=False)
    assert len(azim_x) > 0
    assert len(azim_y) > 0


@pytest.mark.tools
def test_bad_azimuth(at, ccd_contour_data):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    with pytest.raises(ValueError) as e_info:
        at.ccd_contour.azimuth(skymap_data, -10)
    assert "Azimuth" in str(e_info) and "is outside of valid range" in str(e_info)
    with pytest.raises(ValueError) as e_info:
        at.ccd_contour.azimuth(skymap_data, 380)
    assert "Azimuth" in str(e_info) and "is outside of valid range" in str(e_info)


@pytest.mark.tools
def test_bad_min_elevation(at, ccd_contour_data):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    with pytest.raises(ValueError) as e_info:
        at.ccd_contour.azimuth(skymap_data, 45, min_elevation=-10)
    assert "Minimum elevation" in str(e_info) and "is outside of valid range" in str(e_info)
    with pytest.raises(ValueError) as e_info:
        at.ccd_contour.azimuth(skymap_data, 45, min_elevation=100)
    assert "Minimum elevation" in str(e_info) and "is outside of valid range" in str(e_info)


@pytest.mark.tools
def test_bad_max_elevation(at, ccd_contour_data):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    with pytest.raises(ValueError) as e_info:
        at.ccd_contour.azimuth(skymap_data, 45, max_elevation=-10)
    assert "Maximum elevation" in str(e_info) and "is outside of valid range" in str(e_info)
    with pytest.raises(ValueError) as e_info:
        at.ccd_contour.azimuth(skymap_data, 45, max_elevation=100)
    assert "Maximum elevation" in str(e_info) and "is outside of valid range" in str(e_info)


@pytest.mark.tools
def test_bad_min_max_elevation(at, ccd_contour_data):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    with pytest.raises(ValueError) as e_info:
        at.ccd_contour.azimuth(skymap_data, 45, min_elevation=10, max_elevation=10)
    assert "Minimum elevation is lower than maximum elevation" in str(e_info)
