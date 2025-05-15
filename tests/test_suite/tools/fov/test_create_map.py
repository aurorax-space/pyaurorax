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
from pyaurorax.tools import FOV

@pytest.mark.tools
def test_single_data(at, capsys):

    # create FOVData for two THEMIS sites
    fov_data = at.fov.create_data(sites=['atha', 'gill'], instrument_array='themis_asi')

    # create projection
    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # Create the map object
    fov_map = at.fov.create_map(projection_obj, fov_data)
    assert isinstance(fov_map, FOV) is True

    # check __str__ and __repr__ for Mosaic type
    print_str = str(fov_map)
    assert print_str != ""
    assert isinstance(str(fov_map), str) is True
    assert isinstance(repr(fov_map), str) is True
    fov_map.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

@pytest.mark.tools
def test_multi_data(at, capsys):

    # create two FOVData objects for THEMIS and REGO
    fov_data_themis = at.fov.create_data(sites=['atha', 'gill'], instrument_array='themis_asi')
    fov_data_rego = at.fov.create_data(instrument_array='rego')

    # create projection
    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # Create the map object
    fov_map = at.fov.create_map(projection_obj, [fov_data_themis, fov_data_rego])
    assert isinstance(fov_map, FOV) is True

    # check __str__ and __repr__ for Mosaic type
    print_str = str(fov_map)
    assert print_str != ""
    assert isinstance(str(fov_map), str) is True
    assert isinstance(repr(fov_map), str) is True
    fov_map.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

@pytest.mark.tools
def test_no_data(at, capsys):

    # create projection
    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # Create the map object
    fov_map = at.fov.create_map(projection_obj)
    assert isinstance(fov_map, FOV) is True

    # check __str__ and __repr__ for Mosaic type
    print_str = str(fov_map)
    assert print_str != ""
    assert isinstance(str(fov_map), str) is True
    assert isinstance(repr(fov_map), str) is True
    fov_map.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""
