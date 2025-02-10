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
    ccd_bounds = [93, 102, 145, 171]
    bb_data = at.bounding_box.extract_metric.ccd(imgs, ccd_bounds)
    assert bb_data.shape == (imgs.shape[-1], )


@pytest.mark.tools
def test_simple_mean(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    ccd_bounds = [93, 102, 145, 171]
    bb_data = at.bounding_box.extract_metric.ccd(imgs, ccd_bounds, metric="mean")
    assert bb_data.shape == (imgs.shape[-1], )


@pytest.mark.tools
def test_simple_sum(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    ccd_bounds = [93, 102, 145, 171]
    bb_data = at.bounding_box.extract_metric.ccd(imgs, ccd_bounds, metric="sum")
    assert bb_data.shape == (imgs.shape[-1], )


@pytest.mark.tools
def test_n_channels(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    ccd_bounds = [93, 102, 145, 171]
    bb_data = at.bounding_box.extract_metric.ccd(imgs, ccd_bounds, n_channels=1)
    assert bb_data.shape == (imgs.shape[-1], )


@pytest.mark.tools
def test_three_channels(at, bounding_box_data):
    imgs = bounding_box_data["trex_rgb_data"].data
    ccd_bounds = [93, 102, 145, 171]
    bb_data = at.bounding_box.extract_metric.ccd(imgs, ccd_bounds)
    assert bb_data.shape == (3, imgs.shape[-1])


@pytest.mark.tools
def test_order(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    ccd_bounds = [102, 93, 171, 145]
    bb_data = at.bounding_box.extract_metric.ccd(imgs, ccd_bounds, n_channels=1)
    assert bb_data.shape == (imgs.shape[-1], )


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_show_preview(mock_show, at, plot_cleanup, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    ccd_bounds = [102, 93, 171, 145]
    bb_data = at.bounding_box.extract_metric.ccd(imgs, ccd_bounds, show_preview=True)
    assert bb_data.shape == (imgs.shape[-1], )
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_three_channel_show_preview(mock_show, at, plot_cleanup, bounding_box_data):
    imgs = bounding_box_data["trex_rgb_data"].data
    ccd_bounds = [102, 93, 171, 145]
    bb_data = at.bounding_box.extract_metric.ccd(imgs, ccd_bounds, show_preview=True)
    assert bb_data.shape == (3, imgs.shape[-1])
    assert mock_show.call_count == 1


@pytest.mark.tools
def test_bad_coords1(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    ccd_bounds = [300, 102, 145, 171]
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.ccd(imgs, ccd_bounds)
    assert "CCD X0 coordinate" in str(e_info) and "out of range for image of shape" in str(e_info)


@pytest.mark.tools
def test_bad_coords2(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    ccd_bounds = [93, 300, 145, 171]
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.ccd(imgs, ccd_bounds)
    assert "CCD X1 coordinate" in str(e_info) and "out of range for image of shape" in str(e_info)


@pytest.mark.tools
def test_bad_coords3(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    ccd_bounds = [93, 102, 300, 171]
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.ccd(imgs, ccd_bounds)
    assert "CCD Y0 coordinate" in str(e_info) and "out of range for image of shape" in str(e_info)


@pytest.mark.tools
def test_bad_coords4(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    ccd_bounds = [93, 102, 145, 300]
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.ccd(imgs, ccd_bounds)
    assert "CCD Y1 coordinate" in str(e_info) and "out of range for image of shape" in str(e_info)


@pytest.mark.tools
def test_bad_region(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    ccd_bounds = [93, 93, 145, 150]
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.ccd(imgs, ccd_bounds)
    assert "Polygon defined with zero area" in str(e_info)

    ccd_bounds = [93, 100, 145, 145]
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.ccd(imgs, ccd_bounds)
    assert "Polygon defined with zero area" in str(e_info)

    ccd_bounds = [93, 93, 145, 145]
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.ccd(imgs, ccd_bounds)
    assert "Polygon defined with zero area" in str(e_info)


@pytest.mark.tools
def test_bad_metric(at, bounding_box_data):
    imgs = bounding_box_data["themis_data"].data
    ccd_bounds = [102, 93, 171, 145]
    with pytest.raises(ValueError) as e_info:
        _ = at.bounding_box.extract_metric.ccd(imgs, ccd_bounds, metric="bad_metric")
    assert "Metric" in str(e_info) and "is not recognized" in str(e_info)
