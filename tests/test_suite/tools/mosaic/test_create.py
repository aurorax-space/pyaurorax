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
import cartopy.crs
from pyaurorax.tools import Mosaic


@pytest.mark.tools
def test_simple(at, themis_mosaic_data, capsys):
    # init
    mosaic_dt = themis_mosaic_data["dt"]
    prepped_images = themis_mosaic_data["prepped_images"]
    prepped_skymaps = themis_mosaic_data["prepped_skymaps"]

    # create projection
    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # create mosaic
    mosaic = at.mosaic.create(prepped_images, prepped_skymaps, mosaic_dt, projection_obj)
    assert isinstance(mosaic, Mosaic) is True

    # check __str__ and __repr__ for Mosaic type
    print_str = str(mosaic)
    assert print_str != ""
    assert isinstance(str(mosaic), str) is True
    assert isinstance(repr(mosaic), str) is True
    mosaic.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""
