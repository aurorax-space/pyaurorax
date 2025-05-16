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
from pyaurorax.tools import Keogram


@pytest.mark.tools
def test_simple(at, themis_keogram_data, capsys):
    # create the keogram object
    data = themis_keogram_data["raw_data"].data
    timestamp = themis_keogram_data["raw_data"].timestamp
    keogram = at.keogram.create(data, timestamp)
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
def test_spect_errors(at, trex_spect_keogram_data):
    # get data
    data = trex_spect_keogram_data["raw_data"].data
    meta = trex_spect_keogram_data["raw_data"].metadata
    timestamp = trex_spect_keogram_data["raw_data"].timestamp

    # improperly try to create a keogram of spect data along non-zero axis
    with pytest.raises(ValueError) as e_info:
        _ = at.keogram.create(data, timestamp, axis=1, spectra=True, wavelength=meta[0]["wavelength"])

    assert ("Cannot create keogram for spectrograph data along axis other than 0, received axis:") in str(e_info)

    # improperly try to create spect keogram without passing wavelength
    with pytest.raises(ValueError) as e_info:
        _ = at.keogram.create(data, timestamp, spectra=True)

    assert ("Parameter 'wavelength' must be supplied when using spectrograph data.") in str(e_info)

    # attempt to create keogram with incorrect timestamp list
    with pytest.raises(ValueError) as e_info:
        _ = at.keogram.create(data, timestamp[0:50], spectra=True, wavelength=meta[0]["wavelength"])

    assert ("Mismatched timestamp dimensions. Received" in str(e_info)) and ("timestamps for spectrograph data with" in str(e_info))

    # attempt to create keogram with incorrect wavelength list
    with pytest.raises(ValueError) as e_info:
        _ = at.keogram.create(data, timestamp, spectra=True, wavelength=meta[0]["wavelength"][0:50])

    assert ("Mismatched wavelength dimensions. Received" in str(e_info)) and ("wavelengths for spectrograph data with" in str(e_info))


@pytest.mark.tools
def test_incorrect_data_size(at, themis_keogram_data):

    # get data
    data = themis_keogram_data["raw_data"].data
    timestamp = themis_keogram_data["raw_data"].timestamp

    # improperly try to create a keogram of single frame of ASI data
    single_frame_data = data[:, :, 0]
    single_frame_timestamp = timestamp[0]
    with pytest.raises(ValueError) as e_info:
        _ = at.keogram.create(single_frame_data, single_frame_timestamp)

    assert ("Unable to determine number of channels based on the supplied images. Make sure you are supplying a " +
            "[rows,cols,images] or [rows,cols,channels,images] sized array.") in str(e_info)


@pytest.mark.tools
def test_manual_spect_band(at, trex_spect_keogram_data, capsys):

    # create the keogram object with only a manual spect band
    data = trex_spect_keogram_data["raw_data"].data
    meta = trex_spect_keogram_data["raw_data"].metadata
    timestamp = trex_spect_keogram_data["raw_data"].timestamp

    # check that warning is raised for spect band without baground
    with warnings.catch_warnings(record=True) as w:
        keogram = at.keogram.create(data, timestamp, spectra=True, wavelength=meta[0]["wavelength"], spect_band=[560.0, 564.0])
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "Wavelength band supplied without background band. No background subtraction will be performed." in str(w[-1].message)

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

    # create the keogram object with a manual spect band and bg_band
    data = trex_spect_keogram_data["raw_data"].data
    meta = trex_spect_keogram_data["raw_data"].metadata
    timestamp = trex_spect_keogram_data["raw_data"].timestamp
    keogram = at.keogram.create(data,
                                timestamp,
                                spectra=True,
                                wavelength=meta[0]["wavelength"],
                                spect_band=[560.0, 564.0],
                                spect_band_bg=[559.0, 559.5])
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
