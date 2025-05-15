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
from pyaurorax.tools import FOVData


@pytest.mark.tools
def test_themis_sites(at, capsys):

    # create FOVData for two THEMIS sites
    fov_data = at.fov.create_data(sites=['atha', 'gill'], instrument_array='themis_asi')
    assert isinstance(fov_data, FOVData) is True

    # check __str__ and __repr__ for Mosaic type
    print_str = str(fov_data)
    assert print_str != ""
    assert isinstance(str(fov_data), str) is True
    assert isinstance(repr(fov_data), str) is True
    fov_data.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


def test_all_rego(at, capsys):

    # create FOVData for all REGO sites
    fov_data = at.fov.create_data(instrument_array='rego')
    assert isinstance(fov_data, FOVData) is True

    # check __str__ and __repr__ for Mosaic type
    print_str = str(fov_data)
    assert print_str != ""
    assert isinstance(str(fov_data), str) is True
    assert isinstance(repr(fov_data), str) is True
    fov_data.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


def test_spect(at, capsys):

    # create FOVData for two THEMIS sites
    fov_data = at.fov.create_data(instrument_array='trex_spectrograph', height_km=147)
    assert isinstance(fov_data, FOVData) is True

    # check __str__ and __repr__ for Mosaic type
    print_str = str(fov_data)
    assert print_str != ""
    assert isinstance(str(fov_data), str) is True
    assert isinstance(repr(fov_data), str) is True
    fov_data.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


def test_with_tuple_sites(at, capsys):

    # create FOVData for two THEMIS sites
    fov_data = at.fov.create_data(sites=['atha', 'gill', ("custom_1", 63.43, -123.45)], instrument_array='themis_asi')
    assert isinstance(fov_data, FOVData) is True

    # check __str__ and __repr__ for Mosaic type
    print_str = str(fov_data)
    assert print_str != ""
    assert isinstance(str(fov_data), str) is True
    assert isinstance(repr(fov_data), str) is True
    fov_data.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # check that warning is raised for no instrument_array and no height_km
    with warnings.catch_warnings(record=True) as w:
        fov_data = at.fov.create_data(sites=[("custom1", 65.0, -120.0)])

    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "Defaulting to height_km = 110.0. Specify 'instrument_array' or 'height_km' parameters to map FOVs at a different altitude." in str(
        w[-1].message)
    assert isinstance(fov_data, FOVData) is True

    # check __str__ and __repr__ for Mosaic type
    print_str = str(fov_data)
    assert print_str != ""
    assert isinstance(str(fov_data), str) is True
    assert isinstance(repr(fov_data), str) is True
    fov_data.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


def test_improper_inputs(at):

    # attempt to create FOVData with site names without specifying instrument
    with pytest.raises(ValueError) as e_info:
        _ = at.fov.create_data(sites=['atha', 'gill'])

    assert "If specifying sites by site_uid string, instrument_array must also be supplied" in str(e_info)

    # attempt to create FOVData with unkown site name for THEMIS
    with pytest.raises(ValueError) as e_info:
        _ = at.fov.create_data(sites=['daws'], instrument_array='themis_asi')

    assert "Could not find requested site_uid" in str(e_info) and "for instrument_array" in str(e_info)

    # attempt to pass only a lat/lon tuple to create FOVData
    with pytest.raises(ValueError) as e_info:
        _ = at.fov.create_data(sites=[(64.0, -120.0)])

    assert "Improper site format for input" in str(e_info) and "Specifying a site by a tuple requires format ('site_uid', lat, lon)." in str(e_info)

    # attempt to pass an invalid latitude
    with pytest.raises(ValueError) as e_info:
        _ = at.fov.create_data(sites=[("custom1", 120.0, 65.0)])

    assert "Latitude" in str(e_info) and "is outside of the valid range [-90, 90]." in str(e_info)

    # attempt to pass an invalid longitude
    with pytest.raises(ValueError) as e_info:
        _ = at.fov.create_data(sites=[("custom1", 60.0, 220.0)])

    assert "Longitude" in str(e_info) and "is outside of the valid range [-180, 180]." in str(e_info)

    # attempt to pass an invalid height
    with pytest.raises(ValueError) as e_info:
        _ = at.fov.create_data(sites=[("custom1", 60.0, -135.0)], height_km=1050.0)

    assert "Received 'height_km' of" in str(e_info) and ", outside the valid range [10.0, 1000.0]." in str(e_info)

    # attempt to pass an invalid elevation_mask
    with pytest.raises(ValueError) as e_info:
        _ = at.fov.create_data(sites=[("custom1", 60.0, 135.0)], min_elevation=92.4, height_km=110.0)

    assert "Received 'min_elevation' of " in str(e_info) and ", outside the valid range [0.0, 90.0]." in str(e_info)
