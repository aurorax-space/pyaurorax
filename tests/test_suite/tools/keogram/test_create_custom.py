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
from pyaurorax.tools import Keogram
from unittest.mock import patch


@pytest.mark.tools
def test_simple(at, themis_keogram_data, capsys):
    # init
    data = themis_keogram_data["raw_data"].data
    timestamp = themis_keogram_data["raw_data"].timestamp
    ccd_y = np.linspace(0, 255, 50)
    ccd_x = 127.5 + 80 * np.sin(np.pi * ccd_y / 255)

    # create the custom keogram
    keogram = at.keogram.create_custom(data, timestamp, "ccd", 2, ccd_x, ccd_y, metric="sum")
    assert isinstance(keogram, Keogram) is True
    assert keogram.data.shape[-1] == data.shape[-1]

    # check __str__ and __repr__ for Keogram type
    print_str = str(keogram)
    assert print_str != ""
    assert isinstance(str(keogram), str) is True
    assert isinstance(repr(keogram), str) is True
    keogram.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_simple_show_preview(mock_show, plot_cleanup, at, themis_keogram_data, capsys):
    # init
    data = themis_keogram_data["raw_data"].data
    timestamp = themis_keogram_data["raw_data"].timestamp
    ccd_y = np.linspace(0, 255, 50)
    ccd_x = 127.5 + 80 * np.sin(np.pi * ccd_y / 255)

    # create the custom keogram
    keogram = at.keogram.create_custom(data, timestamp, "ccd", 2, ccd_x, ccd_y, preview=True)
    assert isinstance(keogram, Keogram) is True
    assert keogram.data.shape[-1] == data.shape[-1]
    assert mock_show.call_count == 1

    # check __str__ and __repr__ for Keogram type
    print_str = str(keogram)
    assert print_str != ""
    assert isinstance(str(keogram), str) is True
    assert isinstance(repr(keogram), str) is True
    keogram.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.tools
def test_several_args(at, themis_keogram_data, capsys):
    # init
    data = themis_keogram_data["raw_data"].data
    timestamp = themis_keogram_data["raw_data"].timestamp
    ccd_y = np.linspace(0, 255, 50)
    ccd_x = 127.5 + 80 * np.sin(np.pi * ccd_y / 255)

    # create the custom keogram
    keogram = at.keogram.create_custom(data, timestamp, coordinate_system="ccd", width=2, x_locs=ccd_x, y_locs=ccd_y, metric="mean")
    assert isinstance(keogram, Keogram) is True
    assert keogram.data.shape[-1] == data.shape[-1]

    # check __str__ and __repr__ for Keogram type
    print_str = str(keogram)
    assert print_str != ""
    assert isinstance(str(keogram), str) is True
    assert isinstance(repr(keogram), str) is True
    keogram.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.tools
def test_latlon_keogram(at, trex_rgb_keogram_data, capsys):
    # init
    data = trex_rgb_keogram_data["raw_data"].data
    timestamp = trex_rgb_keogram_data["raw_data"].timestamp
    skymap_data = trex_rgb_keogram_data["skymap"]

    # define a curve in lat/lon space
    latitudes = np.linspace(20.0, 62.0, 100)
    longitudes = -102.0 + 5 * np.sin(np.pi * (latitudes - 51.0) / (62.0 - 51.0))

    # create the custom keogram
    keogram = at.keogram.create_custom(data,
                                       timestamp,
                                       coordinate_system="geo",
                                       width=2,
                                       x_locs=longitudes,
                                       y_locs=latitudes,
                                       altitude_km=110,
                                       skymap=skymap_data,
                                       metric="median")
    assert isinstance(keogram, Keogram) is True
    assert keogram.data.shape[2] == data.shape[2]
    assert keogram.data.shape[1] == data.shape[-1]

    # check __str__ and __repr__ for Keogram type
    print_str = str(keogram)
    assert print_str != ""
    assert isinstance(str(keogram), str) is True
    assert isinstance(repr(keogram), str) is True
    keogram.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.tools
def test_supplied_xy_errors(at, themis_keogram_data):
    # init
    data = themis_keogram_data["raw_data"].data
    timestamp = themis_keogram_data["raw_data"].timestamp
    ccd_y = np.linspace(-17, 312, 50)
    ccd_x = 127.5 + 80 * np.sin(np.pi * ccd_y / 255)

    # Attempt to pass in multi-dimensional array for y coords
    bad_ccd_y = ccd_y[:, np.newaxis]

    with pytest.raises(ValueError) as e_info:
        _ = at.keogram.create_custom(data, timestamp, coordinate_system="ccd", width=2, x_locs=ccd_x, y_locs=bad_ccd_y)

    assert "Y coordinates may not be multidimensional. Sequence passed with shape" in str(e_info)

    # Attempt to pass in multi-dimensional array for x coords
    bad_ccd_x = ccd_x[:, np.newaxis]

    with pytest.raises(ValueError) as e_info:
        _ = at.keogram.create_custom(data, timestamp, coordinate_system="ccd", width=2, x_locs=bad_ccd_x, y_locs=ccd_y, metric="sum")

    assert "X coordinates may not be multidimensional. Sequence passed with shape" in str(e_info)

    # Attempt to pass in x and y coords with mismatched lengths
    ccd_x = 107.5 + 80 * np.sin(np.pi * ccd_y / 255)
    ccd_y = ccd_y[0:5]

    with pytest.raises(ValueError) as e_info:
        _ = at.keogram.create_custom(data,
                                     timestamp,
                                     coordinate_system="ccd",
                                     width=2,
                                     x_locs=ccd_x,
                                     y_locs=ccd_y,
                                     metric="percentile",
                                     percentile=95)

    assert "X and Y coordinates must have same length. Sequences passed with shapes" in str(e_info)


def test_metrics_single_channel(at, themis_keogram_data, capsys):

    # init
    data = themis_keogram_data["raw_data"].data
    timestamp = themis_keogram_data["raw_data"].timestamp
    skymap_data = themis_keogram_data["skymap"]

    # define a curve in lat/lon space
    latitudes = np.linspace(20.0, 62.0, 100)
    longitudes = -102.0 + 5 * np.sin(np.pi * (latitudes - 51.0) / (62.0 - 51.0))

    # create the custom keogram using median
    keogram = at.keogram.create_custom(data,
                                       timestamp,
                                       coordinate_system="geo",
                                       width=2,
                                       x_locs=longitudes,
                                       y_locs=latitudes,
                                       altitude_km=110,
                                       skymap=skymap_data,
                                       metric="median")
    assert isinstance(keogram, Keogram) is True
    assert keogram.data.shape[-1] == data.shape[-1]

    # check __str__ and __repr__ for Keogram type
    print_str = str(keogram)
    assert print_str != ""
    assert isinstance(str(keogram), str) is True
    assert isinstance(repr(keogram), str) is True
    keogram.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # create the custom keogram using median
    keogram = at.keogram.create_custom(data,
                                       timestamp,
                                       coordinate_system="geo",
                                       width=2,
                                       x_locs=longitudes,
                                       y_locs=latitudes,
                                       altitude_km=110,
                                       skymap=skymap_data,
                                       metric="mean")
    assert isinstance(keogram, Keogram) is True
    assert keogram.data.shape[-1] == data.shape[-1]

    # check __str__ and __repr__ for Keogram type
    print_str = str(keogram)
    assert print_str != ""
    assert isinstance(str(keogram), str) is True
    assert isinstance(repr(keogram), str) is True
    keogram.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # create the custom keogram using median
    keogram = at.keogram.create_custom(data,
                                       timestamp,
                                       coordinate_system="geo",
                                       width=2,
                                       x_locs=longitudes,
                                       y_locs=latitudes,
                                       altitude_km=110,
                                       skymap=skymap_data,
                                       metric="sum")
    assert isinstance(keogram, Keogram) is True
    assert keogram.data.shape[-1] == data.shape[-1]

    # check __str__ and __repr__ for Keogram type
    print_str = str(keogram)
    assert print_str != ""
    assert isinstance(str(keogram), str) is True
    assert isinstance(repr(keogram), str) is True
    keogram.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # create the custom keogram using median
    keogram = at.keogram.create_custom(data,
                                       timestamp,
                                       coordinate_system="geo",
                                       width=2,
                                       x_locs=longitudes,
                                       y_locs=latitudes,
                                       altitude_km=110,
                                       skymap=skymap_data,
                                       metric="percentile",
                                       percentile=85)
    assert isinstance(keogram, Keogram) is True
    assert keogram.data.shape[-1] == data.shape[-1]

    # check __str__ and __repr__ for Keogram type
    print_str = str(keogram)
    assert print_str != ""
    assert isinstance(str(keogram), str) is True
    assert isinstance(repr(keogram), str) is True
    keogram.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # create the custom keogram using non-recognized metric
    with pytest.raises(ValueError) as e_info:
        _ = at.keogram.create_custom(data,
                                     timestamp,
                                     coordinate_system="geo",
                                     width=2,
                                     x_locs=longitudes,
                                     y_locs=latitudes,
                                     altitude_km=110,
                                     skymap=skymap_data,
                                     metric="some_other_metric")

    assert "is not recognized. Currently supported metrics are ['median', 'mean', 'sum', 'percentile']." in str(e_info)


def test_metrics_multi_channel(at, trex_rgb_keogram_data, capsys):

    # init
    data = trex_rgb_keogram_data["raw_data"].data
    timestamp = trex_rgb_keogram_data["raw_data"].timestamp
    skymap_data = trex_rgb_keogram_data["skymap"]

    # define a curve in lat/lon space
    latitudes = np.linspace(20.0, 62.0, 100)
    longitudes = -102.0 + 5 * np.sin(np.pi * (latitudes - 51.0) / (62.0 - 51.0))

    # create the custom keogram using median
    keogram = at.keogram.create_custom(data,
                                       timestamp,
                                       coordinate_system="geo",
                                       width=2,
                                       x_locs=longitudes,
                                       y_locs=latitudes,
                                       altitude_km=110,
                                       skymap=skymap_data,
                                       metric="median")
    assert isinstance(keogram, Keogram) is True
    assert keogram.data.shape[2] == data.shape[2]
    assert keogram.data.shape[1] == data.shape[-1]

    # check __str__ and __repr__ for Keogram type
    print_str = str(keogram)
    assert print_str != ""
    assert isinstance(str(keogram), str) is True
    assert isinstance(repr(keogram), str) is True
    keogram.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # create the custom keogram using median
    keogram = at.keogram.create_custom(data,
                                       timestamp,
                                       coordinate_system="geo",
                                       width=2,
                                       x_locs=longitudes,
                                       y_locs=latitudes,
                                       altitude_km=110,
                                       skymap=skymap_data,
                                       metric="mean")
    assert isinstance(keogram, Keogram) is True
    assert keogram.data.shape[2] == data.shape[2]
    assert keogram.data.shape[1] == data.shape[-1]

    # check __str__ and __repr__ for Keogram type
    print_str = str(keogram)
    assert print_str != ""
    assert isinstance(str(keogram), str) is True
    assert isinstance(repr(keogram), str) is True
    keogram.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # create the custom keogram using median
    keogram = at.keogram.create_custom(data,
                                       timestamp,
                                       coordinate_system="geo",
                                       width=2,
                                       x_locs=longitudes,
                                       y_locs=latitudes,
                                       altitude_km=110,
                                       skymap=skymap_data,
                                       metric="sum")
    assert isinstance(keogram, Keogram) is True
    assert keogram.data.shape[2] == data.shape[2]
    assert keogram.data.shape[1] == data.shape[-1]

    # check __str__ and __repr__ for Keogram type
    print_str = str(keogram)
    assert print_str != ""
    assert isinstance(str(keogram), str) is True
    assert isinstance(repr(keogram), str) is True
    keogram.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # create the custom keogram using median
    keogram = at.keogram.create_custom(data,
                                       timestamp,
                                       coordinate_system="geo",
                                       width=2,
                                       x_locs=longitudes,
                                       y_locs=latitudes,
                                       altitude_km=110,
                                       skymap=skymap_data,
                                       metric="percentile",
                                       percentile=85)
    assert isinstance(keogram, Keogram) is True
    assert keogram.data.shape[2] == data.shape[2]
    assert keogram.data.shape[1] == data.shape[-1]

    # check __str__ and __repr__ for Keogram type
    print_str = str(keogram)
    assert print_str != ""
    assert isinstance(str(keogram), str) is True
    assert isinstance(repr(keogram), str) is True
    keogram.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # create the custom keogram using non-recognized metric
    with pytest.raises(ValueError) as e_info:
        _ = at.keogram.create_custom(data,
                                     timestamp,
                                     coordinate_system="geo",
                                     width=2,
                                     x_locs=longitudes,
                                     y_locs=latitudes,
                                     altitude_km=110,
                                     skymap=skymap_data,
                                     metric="some_other_metric")

    assert "is not recognized. Currently supported metrics are ['median', 'mean', 'sum', 'percentile']." in str(e_info)
