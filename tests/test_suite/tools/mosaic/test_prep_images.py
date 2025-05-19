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
from pyaurorax.tools import MosaicData


@pytest.mark.tools
def test_simple(at, themis_mosaic_data, capsys):

    # init
    data = themis_mosaic_data["raw_data"]

    prepped_data = at.mosaic.prep_images(data)

    assert isinstance(prepped_data, MosaicData)

    # check __str__ and __repr__ for Mosaic type
    print_str = str(prepped_data)
    assert print_str != ""
    assert isinstance(str(prepped_data), str) is True
    assert isinstance(repr(prepped_data), str) is True
    prepped_data.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.tools
def test_other_args(at, trex_spect_mosaic_data, capsys):

    # init
    data = trex_spect_mosaic_data["raw_data"]

    prepped_data = at.mosaic.prep_images(data, data_attribute='data', spect_emission="blue")

    assert isinstance(prepped_data, MosaicData)

    # check __str__ and __repr__ for Mosaic type
    print_str = str(prepped_data)
    assert print_str != ""
    assert isinstance(str(prepped_data), str) is True
    assert isinstance(repr(prepped_data), str) is True
    prepped_data.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.tools
def test_spect_args(at, trex_spect_mosaic_data, capsys):

    # init
    data = trex_spect_mosaic_data["raw_data"]

    prepped_data = at.mosaic.prep_images(data, data_attribute='data', spect_emission="blue", spect_band=[450.0, 460.0], spect_band_bg=[465.0, 470.0])

    assert isinstance(prepped_data, MosaicData)

    # check __str__ and __repr__ for Mosaic type
    print_str = str(prepped_data)
    assert print_str != ""
    assert isinstance(str(prepped_data), str) is True
    assert isinstance(repr(prepped_data), str) is True
    prepped_data.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    with warnings.catch_warnings(record=True) as w:
        prepped_data = at.mosaic.prep_images(data, spect_emission="blue", spect_band=[450.0, 460.0])
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "Wavelength band supplied without background band. No background subtraction will be performed." in str(w[-1].message)

    assert isinstance(prepped_data, MosaicData)

    # check __str__ and __repr__ for Mosaic type
    print_str = str(prepped_data)
    assert print_str != ""
    assert isinstance(str(prepped_data), str) is True
    assert isinstance(repr(prepped_data), str) is True
    prepped_data.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.tools
def test_bad_data_shape(at, trex_spect_mosaic_data, capsys):

    # init
    data = trex_spect_mosaic_data["raw_data"]

    # Attempt to pass in a reshaped image
    data[0].data = data[0].data[:, :, :, 0:5]
    with pytest.raises(ValueError) as e_info:

        _ = at.mosaic.prep_images(data, data_attribute='data', spect_emission="blue", spect_band=[450.0, 460.0], spect_band_bg=[465.0, 470.0])

    assert ("Number of frames does not match number of timestamp records. There are") in str(e_info)


@pytest.mark.tools
def test_bad_calibrated_data_shape(at, trex_spect_mosaic_data, capsys):

    # init
    data = trex_spect_mosaic_data["raw_data"]

    # Attempt to pass in a reshaped calibrated image
    data[0].calibrated_data = data[0].data[:, :, :, 0:5]
    with pytest.raises(ValueError) as e_info:

        _ = at.mosaic.prep_images(data,
                                  data_attribute='calibrated_data',
                                  spect_emission="blue",
                                  spect_band=[450.0, 460.0],
                                  spect_band_bg=[465.0, 470.0])

    assert ("Number of frames does not match number of timestamp records. There are") in str(e_info)


@pytest.mark.tools
def test_input_errors(at, trex_spect_mosaic_data, capsys):

    # init
    data = trex_spect_mosaic_data["raw_data"]

    # Attempt to pass in a reshaped calibrated image
    data[0].calibrated_data = data[0].data[:, :, :, 0:5]
    with pytest.raises(ValueError) as e_info:

        _ = at.mosaic.prep_images(data, data_attribute='some_string', spect_emission="blue", spect_band=[450.0, 460.0], spect_band_bg=[465.0, 470.0])

    assert ("Invalid 'data_attribute' parameter. Must be either 'data' or 'calibrated_data'.") in str(e_info)


@pytest.mark.tools
def test_duplicate_data(at, trex_rgb_burst_keogram_data, capsys):

    # init
    data = trex_rgb_burst_keogram_data["raw_data"]
    data.data = data.data[:, :, :, 0:25]
    data.metadata = data.metadata[0:25]
    data.timestamp = data.timestamp[0:25]

    with warnings.catch_warnings(record=True) as w:
        prepped_data = at.mosaic.prep_images([data, data])
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "Same site between differing networks detected. Omitting additional" in str(w[-1].message)

    assert isinstance(prepped_data, MosaicData)

    # check __str__ and __repr__ for Mosaic type
    print_str = str(prepped_data)
    assert print_str != ""
    assert isinstance(str(prepped_data), str) is True
    assert isinstance(repr(prepped_data), str) is True
    prepped_data.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.tools
def test_prep_burst_data(at, trex_rgb_burst_keogram_data, capsys):

    # init
    data = trex_rgb_burst_keogram_data["raw_data"]
    data.data = data.data[:, :, :, 0:25]
    data.metadata = data.metadata[0:25]
    data.timestamp = data.timestamp[0:25]

    # Attempt to pass in a reshaped calibrated image

    prepped_data = at.mosaic.prep_images([data])

    assert isinstance(prepped_data, MosaicData)

    # check __str__ and __repr__ for Mosaic type
    print_str = str(prepped_data)
    assert print_str != ""
    assert isinstance(str(prepped_data), str) is True
    assert isinstance(repr(prepped_data), str) is True
    prepped_data.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""
