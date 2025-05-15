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
import warnings
import os
import string
import random
import datetime
import cartopy.crs
from matplotlib import pyplot as plt
from unittest.mock import patch


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_add_contours(mock_show, plot_cleanup, at):

    # Create FOVData
    fov_data = at.fov.create_data(
        ['atha', 'fsmi'],
        instrument_array='themis_asi',
    )

    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=-100.0, central_latitude=55.0)
    fov_map = at.fov.create_map(projection_obj, fov_data)

    # Add some geographic contours
    fov_map.add_geo_contours(lats=[60.0, 60.0, 60.0],
                             lons=[-130.0, -125.0, -120.0],
                             constant_lats=[55.0],
                             constant_lons=[-150.0],
                             color="red",
                             linewidth=2,
                             linestyle="--",
                             marker="o",
                             bring_to_front=True)
    
    # Add some magnetic and geomagnetic contours using scalar lat/lons
    fov_map.add_mag_contours(datetime.datetime.today(),
                             lats=[60.0, 60.0, 60.0],
                             lons=[-130.0, -125.0, -120.0],
                             constant_lats=58.7,
                             constant_lons=-150.0,
                             color="red",
                             linewidth=2,
                             linestyle="--",
                             marker="o",
                             bring_to_front=True)

    # Add another FOV directly to the map
    fov_data_2 = at.fov.create_data(sites=[("custom1", 60.0, -120.0), ("custom2", 65.0, -130.0)], height_km=110.0)
    fov_map.add_fov(fov_data_2)

    # Add two more FOVs directly to the map
    fov_data_3 = at.fov.create_data(sites=[("custom3", 45.0, -120.0), ("custom4", 45.0, -130.0)], height_km=110.0)
    fov_data_4 = at.fov.create_data(sites=[("custom5", 35.0, -123.0), ("custom6", 27.0, -128.0)], height_km=110.0)
    fov_map.add_fov([fov_data_3, fov_data_4])


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_contours_and_no_data(mock_show, plot_cleanup, at):

    # Create FOV with no data
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=-100.0, central_latitude=55.0)
    fov_map = at.fov.create_map(projection_obj)

    # Add some magnetic and geomagnetic contours
    fov_map.add_geo_contours(lats=[60.0, 60.0, 60.0],
                             lons=[-130.0, -125.0, -120.0],
                             constant_lats=[55.0],
                             constant_lons=[-150.0],
                             color="red",
                             linewidth=2,
                             linestyle="--",
                             marker="o",
                             bring_to_front=True)

    # Add an FOV directly to the map
    fov_data_2 = at.fov.create_data(sites=[("custom1", 60.0, -120.0), ("custom2", 65.0, -130.0)], height_km=110.0)
    fov_map.add_fov(fov_data_2)

    # check __str__ and __repr__ for fov_map type
    print_str = str(fov_map)
    assert print_str != ""
    assert isinstance(str(fov_map), str) is True
    assert isinstance(repr(fov_map), str) is True


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_geo_contour_errors(mock_show, plot_cleanup, at):

    # Create FOVData
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=-100.0, central_latitude=55.0)
    fov_map = at.fov.create_map(projection_obj)

    # Attempt to add contours without specifying lats or lons
    with pytest.raises(ValueError) as e_info:
        fov_map.add_geo_contours(color="red", linewidth=2, linestyle="--", marker="o", bring_to_front=True)

    assert "No latitudes or longitudes provided." in str(e_info)

    # Attempt to add contours only specifying lons
    with pytest.raises(ValueError) as e_info:
        fov_map.add_geo_contours(lons = [-130.0], color="red", linewidth=2, linestyle="--", marker="o", bring_to_front=True)

    assert "Manually supplying contour requires both lats and lons." in str(e_info)

    # Attempt to add contours only specifying lats
    with pytest.raises(ValueError) as e_info:
        fov_map.add_geo_contours(lats = [60.0], color="red", linewidth=2, linestyle="--", marker="o", bring_to_front=True)

    assert "Manually supplying contour requires both lats and lons." in str(e_info)

    # Attempt to add contours with incorrect color
    with pytest.raises(ValueError) as e_info:
        fov_map.add_geo_contours(lats = [60.0], lons = [-130.0], color="some_non_existent_color", linewidth=2, linestyle="--", marker="o", bring_to_front=True)

    assert "Color" in str(e_info) and " not recognized by matplotlib." in str(e_info)

    # Attempt to add contours with incorrect linewidth
    with pytest.raises(ValueError) as e_info:
        fov_map.add_geo_contours(lats = [60.0], lons = [-130.0], color="red", linewidth=-2, linestyle="--", marker="o", bring_to_front=True)

    assert "Linewidth must be greater than zero." in str(e_info)

    # Attempt to add contours with incorrect linestyle
    with pytest.raises(ValueError) as e_info:
        fov_map.add_geo_contours(lats = [60.0], lons = [-130.0], color="red", linewidth=2, linestyle="some_non_existent_linestyle", marker="o", bring_to_front=True)

    assert "Linestyle" in str(e_info) and "not recognized by matplotlib." in str(e_info)

    # Attempt to add contours with incorrect marker
    with pytest.raises(ValueError) as e_info:
        fov_map.add_geo_contours(lats = [60.0], lons = [-130.0], color="red", linewidth=2, linestyle="--", marker="some_non_existent_marker", bring_to_front=True)

    assert "Marker" in str(e_info) and "is not currently supported" in str(e_info)

    # Attempt to add contours with mistmatched length lat/lons
    with pytest.raises(ValueError) as e_info:
        fov_map.add_geo_contours(lats = [60.0, 61.0], lons = [-130.0], color="red")

    assert "Lat/Lon data must be of the same size." in str(e_info)

@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_mag_contour_errors(mock_show, plot_cleanup, at):

    timestamp = datetime.datetime.today()

    # Create FOVData
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=-100.0, central_latitude=55.0)
    fov_map = at.fov.create_map(projection_obj)

    # Attempt to add contours without specifying lats or lons
    with pytest.raises(ValueError) as e_info:
        fov_map.add_mag_contours(timestamp, color="red", linewidth=2, linestyle="--", marker="o", bring_to_front=True)

    assert "No latitudes or longitudes provided." in str(e_info)

    # Attempt to add contours only specifying lons
    with pytest.raises(ValueError) as e_info:
        fov_map.add_mag_contours(timestamp, lons = [-130.0], color="red", linewidth=2, linestyle="--", marker="o", bring_to_front=True)

    assert "Manually supplying contour requires both lats and lons." in str(e_info)

    # Attempt to add contours only specifying lats
    with pytest.raises(ValueError) as e_info:
        fov_map.add_mag_contours(timestamp, lats = [60.0], color="red", linewidth=2, linestyle="--", marker="o", bring_to_front=True)

    assert "Manually supplying contour requires both lats and lons." in str(e_info)

    # Attempt to add contours with incorrect color
    with pytest.raises(ValueError) as e_info:
        fov_map.add_mag_contours(timestamp, lats = [60.0], lons = [-130.0], color="some_non_existent_color", linewidth=2, linestyle="--", marker="o", bring_to_front=True)

    assert "Color" in str(e_info) and " not recognized by matplotlib." in str(e_info)

    # Attempt to add contours with incorrect linewidth
    with pytest.raises(ValueError) as e_info:
        fov_map.add_mag_contours(timestamp, lats = [60.0], lons = [-130.0], color="red", linewidth=-2, linestyle="--", marker="o", bring_to_front=True)

    assert "Linewidth must be greater than zero." in str(e_info)

    # Attempt to add contours with incorrect linestyle
    with pytest.raises(ValueError) as e_info:
        fov_map.add_mag_contours(timestamp, lats = [60.0], lons = [-130.0], color="red", linewidth=2, linestyle="some_non_existent_linestyle", marker="o", bring_to_front=True)

    assert "Linestyle" in str(e_info) and "not recognized by matplotlib." in str(e_info)

    # Attempt to add contours with incorrect marker
    with pytest.raises(ValueError) as e_info:
        fov_map.add_mag_contours(timestamp, lats = [60.0], lons = [-130.0], color="red", linewidth=2, linestyle="--", marker="some_non_existent_marker", bring_to_front=True)

    assert "Marker" in str(e_info) and "is not currently supported" in str(e_info)

    # Attempt to add contours with mistmatched length lat/lons
    with pytest.raises(ValueError) as e_info:
        fov_map.add_mag_contours(timestamp, lats = [60.0, 61.0], lons = [-130.0], color="red")

    assert "Lat/Lon data must be of the same size." in str(e_info)

    