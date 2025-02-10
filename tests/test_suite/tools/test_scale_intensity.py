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
def test_simple(at, themis_single_file):
    img = themis_single_file.data[:, :, 0]
    print(img.shape)
    img_scaled = at.scale_intensity(img)
    assert img_scaled.shape == img.shape


@pytest.mark.tools
def test_multiple_frames(at, themis_single_file):
    img = themis_single_file.data[:, :, 0:5]
    img_scaled = at.scale_intensity(img)
    assert img_scaled.shape == img.shape


@pytest.mark.tools
def test_specific_floor(at, themis_single_file):
    img = themis_single_file.data[:, :, 0:5]
    img_scaled = at.scale_intensity(img, min=1000)
    assert img_scaled.shape == img.shape


@pytest.mark.tools
def test_specific_ceiling(at, themis_single_file):
    img = themis_single_file.data[:, :, 0:5]
    img_scaled = at.scale_intensity(img, max=10000)
    assert img_scaled.shape == img.shape


@pytest.mark.tools
def test_specific_floor_and_ceiling(at, themis_single_file):
    img = themis_single_file.data[:, :, 0:5]
    img_scaled = at.scale_intensity(img, min=1000, max=10000)
    assert img_scaled.shape == img.shape


@pytest.mark.tools
def test_same_floor_and_ceiling(at, themis_single_file):
    img = themis_single_file.data[:, :, 0:5]
    img_scaled = at.scale_intensity(img, min=1000, max=1000)
    assert img_scaled.shape == img.shape


@pytest.mark.tools
def test_three_channel(at, trex_rgb_single_file):
    img = trex_rgb_single_file.data[:, :, :, 0]
    img_scaled = at.scale_intensity(img)
    assert img_scaled.shape == img.shape


@pytest.mark.tools
def test_three_channel_multiple_frames(at, trex_rgb_single_file):
    img = trex_rgb_single_file.data[:, :, :, 0:5]
    img_scaled = at.scale_intensity(img)
    assert img_scaled.shape == img.shape


@pytest.mark.tools
def test_memory_saver(at, trex_rgb_single_file):
    img = trex_rgb_single_file.data[:, :, :, 0:5]
    img_scaled = at.scale_intensity(img, memory_saver=False)
    assert img_scaled.shape == img.shape


@pytest.mark.tools
def test_bad_ceiling(at, themis_single_file):
    img = themis_single_file.data[:, :, 0:5]
    with pytest.raises(ValueError) as e_info:
        _ = at.scale_intensity(img, min=1000, max=999)
    assert "The max value must be larger than the min value" in str(e_info)


@pytest.mark.tools
def test_bad_top(at, themis_single_file):
    img = themis_single_file.data[:, :, 0:5]
    with pytest.raises(ValueError) as e_info:
        _ = at.scale_intensity(img, min=1000, max=10000, top=100000)
    assert "The top value must be less than or equal to" in str(e_info)


@pytest.mark.tools
def test_bad_top_double(at, themis_single_file):
    img = themis_single_file.data[:, :, 0].astype(np.float32)  # convert to float array
    with pytest.raises(ValueError) as e_info:
        _ = at.scale_intensity(img)
    assert "The top parameter must be specified when a float array is supplied" in str(e_info)
