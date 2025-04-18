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
from unittest.mock import patch


@pytest.mark.tools
def test_simple_median(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    ts = bounding_box_data["themis_data"].timestamp[0]
    lon_lat = [-52, -50, 62, 61.1]
    altitude_km = 110
    bb_data = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, lon_lat)
    assert bb_data.shape == (imgs.shape[-1], )


@pytest.mark.tools
def test_simple_mean(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    ts = bounding_box_data["themis_data"].timestamp[0]
    lon_lat = [-52, -50, 62, 61.1]
    altitude_km = 115
    bb_data = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, lon_lat, metric="mean")
    assert bb_data.shape == (imgs.shape[-1], )


@pytest.mark.tools
def test_simple_sum(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    ts = bounding_box_data["themis_data"].timestamp[0]
    lon_lat = [-52, -50, 62, 61.1]
    altitude_km = 115
    bb_data = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, lon_lat, metric="sum")
    assert bb_data.shape == (imgs.shape[-1], )


@pytest.mark.tools
def test_three_channel(at, bounding_box_data):
    imgs = bounding_box_data["trex_rgb_data"].data
    skymap = bounding_box_data["trex_rgb_skymap"]
    ts = bounding_box_data["themis_data"].timestamp[0]
    lon_lat = [-25, -20, 60, 64]
    altitude_km = 115
    bb_data = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, lon_lat)
    assert bb_data.shape == (3, imgs.shape[-1])


@pytest.mark.tools
def test_n_channels(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    ts = bounding_box_data["themis_data"].timestamp[0]
    lon_lat = [-52, -50, 62, 61.1]
    altitude_km = 115
    bb_data = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, lon_lat, n_channels=1)
    assert bb_data.shape == (imgs.shape[-1], )


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_show_preview(mock_show, at, plot_cleanup, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    ts = bounding_box_data["themis_data"].timestamp[0]
    lon_lat = [-52, -50, 62, 61.1]
    altitude_km = 115
    bb_data = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, lon_lat, show_preview=True)
    assert bb_data.shape == (imgs.shape[-1], )
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_three_channel_show_preview(mock_show, at, plot_cleanup, bounding_box_data):
    imgs = bounding_box_data["trex_rgb_data"].data
    skymap = bounding_box_data["trex_rgb_skymap"]
    ts = bounding_box_data["themis_data"].timestamp[0]
    lon_lat = [-25, -20, 60, 64]
    altitude_km = 115
    bb_data = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, lon_lat, show_preview=True)
    assert bb_data.shape == (3, imgs.shape[-1])
    assert mock_show.call_count == 1


@pytest.mark.tools
def test_big_longitudes(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    ts = bounding_box_data["themis_data"].timestamp[0]
    lon_lat = [308, 306, 62, 61.1]
    altitude_km = 115
    bb_data = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, lon_lat)
    assert bb_data.shape == (imgs.shape[-1], )


@pytest.mark.tools
def test_order(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    ts = bounding_box_data["themis_data"].timestamp[0]
    lon_lat = [-50, -52, 61.1, 62]
    altitude_km = 115
    bb_data = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, lon_lat)
    assert bb_data.shape == (imgs.shape[-1], )


@pytest.mark.tools
def test_bad_coords1(at, bounding_box_data):
    # check first latitude value
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    ts = bounding_box_data["themis_data"].timestamp[0]
    altitude_km = 115
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, [-52, -50, 100, 61.1])
    assert "Invalid latitude" in str(e_info)
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, [-52, -50, -100, 61.1])
    assert "Invalid latitude" in str(e_info)


@pytest.mark.tools
def test_bad_coords2(at, bounding_box_data):
    # check second latitude value
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    ts = bounding_box_data["themis_data"].timestamp[0]
    altitude_km = 115
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, [-52, -50, 62, 100])
    assert "Invalid latitude" in str(e_info)
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, [-52, -50, 62, -100])
    assert "Invalid latitude" in str(e_info)


@pytest.mark.tools
def test_bad_coords3(at, bounding_box_data):
    # check first longitude value
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    ts = bounding_box_data["themis_data"].timestamp[0]
    altitude_km = 115
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, [380, -50, 62, 61.1])
    assert "Invalid longitude" in str(e_info)
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, [-190, -50, 62, 61.1])
    assert "Invalid longitude" in str(e_info)


@pytest.mark.tools
def test_bad_coords4(at, bounding_box_data):
    # check second longitude value
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    ts = bounding_box_data["themis_data"].timestamp[0]
    altitude_km = 115
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, [-52, 380, 62, 61.1])
    assert "Invalid longitude" in str(e_info)
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, [-52, -190, 62, 61.1])
    assert "Invalid longitude" in str(e_info)


@pytest.mark.tools
def test_bad_coords5(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    ts = bounding_box_data["themis_data"].timestamp[0]
    altitude_km = 110
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, [-52, -50, 85., 89.])
    assert "Latitude range supplied is outside the valid range for this skymap" in str(e_info)
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, [-70, -75, 62, 61.1])
    assert "Longitude range supplied is outside the valid range for this skymap" in str(e_info)


@pytest.mark.tools
def test_same_coords(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    ts = bounding_box_data["themis_data"].timestamp[0]
    altitude_km = 115
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, [-52, -52, 62, 61.1])
    assert "Polygon defined with zero area" in str(e_info)
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, [-52, -50, 62, 62])
    assert "Polygon defined with zero area" in str(e_info)
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, [-52, -52, 62, 62])
    assert "Polygon defined with zero area" in str(e_info)


@pytest.mark.tools
def test_bad_altitude(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    ts = bounding_box_data["themis_data"].timestamp[0]
    altitude_km = 1000
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, [-52, -50, 62, 61.1])
    assert "Altitude" in str(e_info) and "outside valid range of" in str(e_info)


@pytest.mark.tools
def test_bad_metric(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    ts = bounding_box_data["themis_data"].timestamp[0]
    altitude_km = 115
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.mag(imgs, ts, skymap, altitude_km, [-52, -50, 62, 61.1], metric="bad_metric")
    assert "Metric" in str(e_info) and "is not recognized" in str(e_info)
