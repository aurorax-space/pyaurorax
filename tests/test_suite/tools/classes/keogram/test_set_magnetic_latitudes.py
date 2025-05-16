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
import datetime
import numpy as np
from pyaurorax.tools import Keogram


@pytest.mark.tools
def test_simple(at, themis_keogram_data, capsys):
    # create the keogram object
    data = themis_keogram_data["raw_data"].data
    timestamp = themis_keogram_data["raw_data"].timestamp
    keogram = at.keogram.create(data, timestamp)
    assert isinstance(keogram, Keogram) is True
    assert keogram.data.shape[-1] == data.shape[-1]

    # set latitudes
    skymap_data = themis_keogram_data["skymap"]
    keogram.set_magnetic_latitudes(skymap_data, timestamp[0])

    # check __str__ and __repr__ for Keogram type
    print_str = str(keogram)
    assert print_str != ""
    assert isinstance(str(keogram), str) is True
    assert isinstance(repr(keogram), str) is True
    keogram.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.tools
@pytest.mark.parametrize("altitude", [110, 115])
def test_altitude(at, themis_keogram_data, altitude):
    # create the keogram object
    data = themis_keogram_data["raw_data"].data
    timestamp = themis_keogram_data["raw_data"].timestamp
    keogram = at.keogram.create(data, timestamp)
    assert isinstance(keogram, Keogram) is True
    assert keogram.data.shape[-1] == data.shape[-1]

    # add lats
    skymap_data = themis_keogram_data["skymap"]
    keogram.set_magnetic_latitudes(skymap_data, timestamp[0], altitude_km=altitude)


@pytest.mark.tools
def test_bad_altitude(at, themis_keogram_data):
    # create the keogram object
    data = themis_keogram_data["raw_data"].data
    timestamp = themis_keogram_data["raw_data"].timestamp
    keogram = at.keogram.create(data, timestamp)
    assert isinstance(keogram, Keogram) is True
    assert keogram.data.shape[-1] == data.shape[-1]

    # add lats
    skymap_data = themis_keogram_data["skymap"]
    altitude = 1000
    with pytest.raises(ValueError) as e_info:
        keogram.set_magnetic_latitudes(skymap_data, timestamp[0], altitude_km=altitude)
    assert "Altitude" in str(e_info) and "outside valid range" in str(e_info)


@pytest.mark.tools
def test_set_mag_on_custom_keo(at, themis_keogram_data):
    # create the custom keogram object
    data = themis_keogram_data["raw_data"].data
    timestamp = themis_keogram_data["raw_data"].timestamp

    # define a curve in CCD space
    ccd_y = np.linspace(0, 255, 50)
    ccd_x = 127.5 + 80 * np.sin(np.pi * ccd_y / 255)

    # create the custom keogram
    custom_keogram = at.keogram.create_custom(
        data,
        timestamp,
        coordinate_system="ccd",
        width=2,
        x_locs=ccd_x,
        y_locs=ccd_y,
    )

    assert isinstance(custom_keogram, Keogram) is True
    assert custom_keogram.data.shape[-1] == data.shape[-1]

    # incorrectly try to set lats on custom keogram
    skymap_data = themis_keogram_data["skymap"]
    with pytest.raises(ValueError) as e_info:
        custom_keogram.set_magnetic_latitudes(timestamp, skymap_data, altitude_km=110)

    assert ("Unable to set the magnetic latitudes since the slice_idx is None. If this keogram" in str(e_info)
            and ("this is expected and performing this action is not supported at this time.") in str(e_info))


@pytest.mark.tools
def test_set_mag_on_spect(at, trex_spect_keogram_data, capsys):

    # create the keogram object
    data = trex_spect_keogram_data["raw_data"].data
    meta = trex_spect_keogram_data["raw_data"].metadata
    timestamp = trex_spect_keogram_data["raw_data"].timestamp
    keogram = at.keogram.create(data, timestamp, spectra=True, wavelength=meta[0]["wavelength"])
    assert isinstance(keogram, Keogram) is True
    assert keogram.data.shape[-1] == data.shape[-1]

    # add lats
    skymap_data = trex_spect_keogram_data["skymap"]
    keogram.set_magnetic_latitudes(skymap_data, datetime.datetime.today())

    # check __str__ and __repr__ for Keogram type
    print_str = str(keogram)
    assert print_str != ""
    assert isinstance(str(keogram), str) is True
    assert isinstance(repr(keogram), str) is True
    keogram.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # Repeat, but specifying an altitude
    skymap_data = trex_spect_keogram_data["skymap"]
    keogram.set_magnetic_latitudes(skymap_data, datetime.datetime.today(), altitude_km=110.0)

    # check __str__ and __repr__ for Keogram type
    print_str = str(keogram)
    assert print_str != ""
    assert isinstance(str(keogram), str) is True
    assert isinstance(repr(keogram), str) is True
    keogram.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""
