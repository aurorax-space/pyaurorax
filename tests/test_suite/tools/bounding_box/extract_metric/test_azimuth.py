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
    az_range = [140, 173]
    bb_data = at.bounding_box.extract_metric.azimuth(imgs, skymap, az_range)
    assert bb_data.shape == (imgs.shape[-1], )


@pytest.mark.tools
def test_simple_mean(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    az_range = [140, 173]
    bb_data = at.bounding_box.extract_metric.azimuth(imgs, skymap, az_range, metric="mean")
    assert bb_data.shape == (imgs.shape[-1], )


@pytest.mark.tools
def test_simple_sum(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    az_range = [140, 173]
    bb_data = at.bounding_box.extract_metric.azimuth(imgs, skymap, az_range, metric="sum")
    assert bb_data.shape == (imgs.shape[-1], )


@pytest.mark.tools
def test_three_channel(at, bounding_box_data):
    imgs = bounding_box_data["trex_rgb_data"].data
    skymap = bounding_box_data["trex_rgb_skymap"]
    az_range = [140, 173]
    bb_data = at.bounding_box.extract_metric.azimuth(imgs, skymap, az_range)
    assert bb_data.shape == (3, imgs.shape[-1])


@pytest.mark.tools
def test_n_channels(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    az_range = [140, 173]
    bb_data = at.bounding_box.extract_metric.azimuth(imgs, skymap, az_range, n_channels=1)
    assert bb_data.shape == (imgs.shape[-1], )


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_show_preview(mock_show, at, plot_cleanup, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    az_range = [140, 173]
    bb_data = at.bounding_box.extract_metric.azimuth(imgs, skymap, az_range, show_preview=True)
    assert bb_data.shape == (imgs.shape[-1], )
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_three_channel_show_preview(mock_show, at, plot_cleanup, bounding_box_data):
    imgs = bounding_box_data["trex_rgb_data"].data
    skymap = bounding_box_data["trex_rgb_skymap"]
    az_range = [140, 173]
    bb_data = at.bounding_box.extract_metric.azimuth(imgs, skymap, az_range, show_preview=True)
    assert bb_data.shape == (3, imgs.shape[-1])
    assert mock_show.call_count == 1


@pytest.mark.tools
def test_order(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    az_range = [173, 140]
    bb_data = at.bounding_box.extract_metric.azimuth(imgs, skymap, az_range)
    assert bb_data.shape == (imgs.shape[-1], )


@pytest.mark.tools
def test_bad_azimuth1(at, bounding_box_data):
    # check first azimuth value
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.azimuth(imgs, skymap, [-180, 90])
    assert "Invalid azimuth" in str(e_info)
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.azimuth(imgs, skymap, [390, 90])
    assert "Invalid azimuth" in str(e_info)


@pytest.mark.tools
def test_bad_azimuth2(at, bounding_box_data):
    # check second azimuth value
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.azimuth(imgs, skymap, [90, -180])
    assert "Invalid azimuth" in str(e_info)
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.azimuth(imgs, skymap, [90, 390])
    assert "Invalid azimuth" in str(e_info)


@pytest.mark.tools
def test_bad_azimuth3(at, bounding_box_data):
    # check azimuth value when same
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.azimuth(imgs, skymap, [90, 90])
    assert "Azimuth bounds defined with zero area" in str(e_info)


@pytest.mark.tools
def test_bad_metric(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    skymap = bounding_box_data["themis_skymap"]
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.azimuth(imgs, skymap, [90, 100], metric="bad_metric")
    assert "Metric" in str(e_info) and "is not recognized" in str(e_info)
