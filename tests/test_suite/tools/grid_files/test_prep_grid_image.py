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
def test_simple(at, themis_grid_data):
    grid = themis_grid_data.data.grid[:, :, 0]
    fill_val = themis_grid_data.data.fill_value
    rgba_grid = at.grid_files.prep_grid_image(grid, fill_val)
    assert rgba_grid.shape == (512, 1024, 4)


@pytest.mark.tools
def test_three_channel(at, trex_rgb_grid_data):
    grid = trex_rgb_grid_data.data.grid[:, :, :, 0]
    fill_val = trex_rgb_grid_data.data.fill_value
    rgba_grid = at.grid_files.prep_grid_image(grid, fill_val)
    assert rgba_grid.shape == (512, 1024, 4)


@pytest.mark.tools
def test_scale1(at, themis_grid_data):
    grid = themis_grid_data.data.grid[:, :, 0]
    fill_val = themis_grid_data.data.fill_value
    rgba_grid = at.grid_files.prep_grid_image(grid, fill_val, scale=[1000, 10000])
    assert rgba_grid.shape == (512, 1024, 4)


@pytest.mark.tools
def test_scale2(at, themis_grid_data):
    grid = themis_grid_data.data.grid[:, :, 0]
    fill_val = themis_grid_data.data.fill_value
    rgba_grid = at.grid_files.prep_grid_image(grid, fill_val, scale=(1000, 10000))
    assert rgba_grid.shape == (512, 1024, 4)


@pytest.mark.tools
def test_rgb_scale(at, trex_rgb_grid_data):
    grid = trex_rgb_grid_data.data.grid[:, :, :, 0]
    fill_val = trex_rgb_grid_data.data.fill_value
    rgba_grid = at.grid_files.prep_grid_image(grid, fill_val, scale=(15, 120))
    assert rgba_grid.shape == (512, 1024, 4)


@pytest.mark.tools
def test_bad_scale(at, themis_grid_data):
    grid = themis_grid_data.data.grid[:, :, 0]
    fill_val = themis_grid_data.data.fill_value
    with pytest.raises(ValueError) as e_info:
        at.grid_files.prep_grid_image(grid, fill_val, scale=(1000))
    assert "Scale must be provided as a two-element vector" in str(e_info)
    with pytest.raises(ValueError) as e_info:
        at.grid_files.prep_grid_image(grid, fill_val, scale=[1000])
    assert "Scale must be provided as a two-element vector" in str(e_info)


@pytest.mark.tools
def test_bad_data(at, trex_rgb_grid_data):
    grid = trex_rgb_grid_data.data.grid[:, :, :, 0:5]
    fill_val = trex_rgb_grid_data.data.fill_value
    with pytest.raises(ValueError) as e_info:
        at.grid_files.prep_grid_image(grid, fill_val)
    assert "Routine currently only supports grid data with shape" in str(e_info)
