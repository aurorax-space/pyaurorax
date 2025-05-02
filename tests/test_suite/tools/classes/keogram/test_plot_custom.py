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
import numpy as np
from unittest.mock import patch


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_simple(mock_show, plot_cleanup, at, themis_keogram_data):
    # init
    data = themis_keogram_data["raw_data"].data
    timestamp = themis_keogram_data["raw_data"].timestamp
    ccd_y = np.linspace(0, 255, 50)
    ccd_x = 127.5 + 80 * np.sin(np.pi * ccd_y / 255)
    keogram = at.keogram.create_custom(data, timestamp, "ccd", 2, ccd_x, ccd_y)

    # plot
    with warnings.catch_warnings(record=True) as w:
        keogram.plot()
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "Unable to plot CCD y-axis" in str(w[-1].message)
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_geo_rgb(mock_show, plot_cleanup, at, trex_rgb_keogram_data):
    # init
    data = trex_rgb_keogram_data["raw_data"].data
    timestamp = trex_rgb_keogram_data["raw_data"].timestamp
    skymap_data = trex_rgb_keogram_data["skymap"]
    latitudes = np.linspace(51.0, 62.0, 50)
    longitudes = -102.0 + 5 * np.sin(np.pi * (latitudes - 51.0) / (62.0 - 51.0))
    keogram = at.keogram.create_custom(data,
                                       timestamp,
                                       coordinate_system="geo",
                                       width=2,
                                       x_locs=longitudes,
                                       y_locs=latitudes,
                                       preview=True,
                                       altitude_km=115,
                                       skymap=skymap_data,
                                       metric="median")
    assert mock_show.call_count == 1

    # plot
    with warnings.catch_warnings(record=True) as w:
        keogram.plot()
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "Unable to plot CCD y-axis" in str(w[-1].message)
    assert mock_show.call_count == 2


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_mag_rgb(mock_show, plot_cleanup, at, trex_rgb_keogram_data):
    # init
    data = trex_rgb_keogram_data["raw_data"].data
    timestamp = trex_rgb_keogram_data["raw_data"].timestamp
    skymap_data = trex_rgb_keogram_data["skymap"]
    latitudes = np.linspace(51.0, 62.0, 50)
    longitudes = -102.0 + 5 * np.sin(np.pi * (latitudes - 51.0) / (62.0 - 51.0))
    keogram = at.keogram.create_custom(data,
                                       timestamp,
                                       coordinate_system="mag",
                                       width=2,
                                       x_locs=longitudes,
                                       y_locs=latitudes,
                                       preview=True,
                                       altitude_km=115,
                                       skymap=skymap_data,
                                       metric="median")
    assert mock_show.call_count == 1

    # plot
    with warnings.catch_warnings(record=True) as w:
        keogram.plot()
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "Unable to plot CCD y-axis" in str(w[-1].message)
    assert mock_show.call_count == 2


@pytest.mark.tools
def test_unexpected_altitude(at, themis_keogram_data):
    data = themis_keogram_data["raw_data"].data
    timestamp = themis_keogram_data["raw_data"].timestamp
    ccd_y = np.linspace(0, 255, 50)
    ccd_x = 127.5 + 80 * np.sin(np.pi * ccd_y / 255)
    with pytest.raises(ValueError) as e_info:
        at.keogram.create_custom(data, timestamp, "ccd", 2, ccd_x, ccd_y, altitude_km=1000)
    assert "Conflict in passing in a skymap or altitude when working in CCD coordinates" in str(e_info)


@pytest.mark.tools
def test_bad_altitude(at, themis_keogram_data):
    data = themis_keogram_data["raw_data"].data
    timestamp = themis_keogram_data["raw_data"].timestamp
    skymap_data = themis_keogram_data["skymap"]
    latitudes = np.linspace(51.0, 62.0, 50)
    longitudes = -102.0 + 5 * np.sin(np.pi * (latitudes - 51.0) / (62.0 - 51.0))
    with pytest.raises(ValueError) as e_info:
        at.keogram.create_custom(data,
                                 timestamp,
                                 coordinate_system="geo",
                                 width=2,
                                 x_locs=longitudes,
                                 y_locs=latitudes,
                                 altitude_km=1000,
                                 skymap=skymap_data)
    assert "Altitude" in str(e_info) and "outside valid range" in str(e_info)
