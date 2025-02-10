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
@pytest.mark.parametrize("altitude,constant_lat", [(110, 60), (115, 60)])
def test_simple_constant_lat(at, ccd_contour_data, altitude, constant_lat):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    ts = ccd_contour_data["trex_rgb_data"].timestamp[0]
    x_pix, y_pix = at.ccd_contour.mag(skymap_data, ts, altitude_km=altitude, constant_lat=constant_lat)
    assert len(x_pix) > 0
    assert len(y_pix) > 0


@pytest.mark.tools
@pytest.mark.parametrize("altitude,constant_lon", [(110, -90), (115, -30)])
def test_simple_constant_lon(at, ccd_contour_data, altitude, constant_lon):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    ts = ccd_contour_data["trex_rgb_data"].timestamp[0]
    x_pix, y_pix = at.ccd_contour.mag(skymap_data, ts, altitude_km=altitude, constant_lon=constant_lon)
    assert len(x_pix) > 0
    assert len(y_pix) > 0


@pytest.mark.tools
def test_simple_custom(at, ccd_contour_data):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    ts = ccd_contour_data["trex_rgb_data"].timestamp[0]
    altitude_km = 115
    latitudes = np.linspace(59.0, 69.0, 50)
    longitudes = -30.0 + (np.sin(np.linspace(0, np.pi / 2, 50)) + 1) * (11 / 2)
    x_pix, y_pix = at.ccd_contour.mag(skymap_data, ts, altitude_km, contour_lats=latitudes, contour_lons=longitudes)
    assert len(x_pix) > 0
    assert len(y_pix) > 0


@pytest.mark.tools
@pytest.mark.parametrize("latitudes,longitudes", [
    ([60], [-30]),
    ([60, 70], [-30, -20]),
    (np.asarray([60]), np.asarray([-30])),
    (np.asarray([60, 70]), np.asarray([-30, -20])),
])
def test_custom_value_types(at, ccd_contour_data, latitudes, longitudes):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    ts = ccd_contour_data["trex_rgb_data"].timestamp[0]
    altitude_km = 115
    x_pix, y_pix = at.ccd_contour.mag(skymap_data, ts, altitude_km, contour_lats=latitudes, contour_lons=longitudes)
    assert len(x_pix) > 0
    assert len(y_pix) > 0


@pytest.mark.tools
def test_no_remove_edge_cases_constant_lat(at, ccd_contour_data):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    ts = ccd_contour_data["trex_rgb_data"].timestamp[0]
    x_pix, y_pix = at.ccd_contour.mag(skymap_data, ts, altitude_km=110, constant_lat=55, remove_edge_cases=False)
    assert len(x_pix) > 0
    assert len(y_pix) > 0


@pytest.mark.tools
def test_no_remove_edge_cases_constant_lon(at, ccd_contour_data):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    ts = ccd_contour_data["trex_rgb_data"].timestamp[0]
    x_pix, y_pix = at.ccd_contour.mag(skymap_data, ts, altitude_km=110, constant_lon=-100, remove_edge_cases=False)
    assert len(x_pix) > 0
    assert len(y_pix) > 0


@pytest.mark.tools
def test_no_remove_edge_cases_custom(at, ccd_contour_data):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    ts = ccd_contour_data["trex_rgb_data"].timestamp[0]
    altitude_km = 115
    latitudes = np.linspace(59.0, 69.0, 50)
    longitudes = -30.0 + (np.sin(np.linspace(0, np.pi / 2, 50)) + 1) * (11 / 2)
    x_pix, y_pix = at.ccd_contour.mag(skymap_data, ts, altitude_km, contour_lats=latitudes, contour_lons=longitudes, remove_edge_cases=False)
    assert len(x_pix) > 0
    assert len(y_pix) > 0


@pytest.mark.tools
def test_bad_custom_args(at, ccd_contour_data):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    ts = ccd_contour_data["trex_rgb_data"].timestamp[0]
    altitude_km = 115
    latitudes = np.linspace(51.0, 62.0, 50)
    longitudes = -102.0 + 5 * np.sin(np.pi * (latitudes - 51.0) / (62.0 - 51.0))
    with pytest.raises(ValueError) as e_info:
        at.ccd_contour.mag(skymap_data, ts, altitude_km, contour_lats=latitudes)
    assert "When defining a custom contour, both 'contour_lats' and 'contour_lons' must be supplied" in str(e_info)
    with pytest.raises(ValueError) as e_info:
        at.ccd_contour.mag(skymap_data, ts, altitude_km, contour_lons=longitudes)
    assert "When defining a custom contour, both 'contour_lats' and 'contour_lons' must be supplied" in str(e_info)


@pytest.mark.tools
def test_too_many_args(at, ccd_contour_data):
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    ts = ccd_contour_data["trex_rgb_data"].timestamp[0]
    altitude_km = 115
    latitudes = np.linspace(51.0, 62.0, 50)
    longitudes = -102.0 + 5 * np.sin(np.pi * (latitudes - 51.0) / (62.0 - 51.0))
    constant_lat = 55
    constant_lon = 110
    with pytest.raises(ValueError) as e_info:
        at.ccd_contour.mag(
            skymap_data,
            ts,
            altitude_km,
            contour_lats=latitudes,
            contour_lons=longitudes,
            constant_lat=constant_lat,
            constant_lon=constant_lon,
        )
    assert "Only one contour can be defined per call" in str(e_info)


@pytest.mark.tools
def test_not_enough_args(at, ccd_contour_data):
    altitude_km = 115
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    ts = ccd_contour_data["trex_rgb_data"].timestamp[0]
    with pytest.raises(ValueError) as e_info:
        at.ccd_contour.mag(skymap_data, ts, altitude_km)
    assert "No contour defined in input" in str(e_info)


@pytest.mark.tools
def test_bad_altitude(at, ccd_contour_data):
    altitude_km = 1000
    skymap_data = ccd_contour_data["trex_rgb_skymap"]
    ts = ccd_contour_data["trex_rgb_data"].timestamp[0]
    with pytest.raises(ValueError) as e_info:
        at.ccd_contour.mag(skymap_data, ts, altitude_km, constant_lat=40)
    assert "Altitude" in str(e_info) and "outside valid range of" in str(e_info)
