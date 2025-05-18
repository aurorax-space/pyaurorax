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
import warnings
import numpy as np


@pytest.mark.tools
@pytest.mark.parametrize("emission", ["blue", "hbeta", "green", "red"])
@pytest.mark.parametrize("spect_loc", [140, 145])
@pytest.mark.parametrize("minute", [9, 32])
def test_simple(at, trex_spect_keogram_data, emission, spect_loc, minute):

    # get spect data
    data = trex_spect_keogram_data["raw_data"]

    # get single intensities at a point in time
    t_0 = datetime.datetime(2021, 2, 16, 9, minute, 0)

    intensity = at.spectra.get_intensity(data, t_0, spect_loc, spect_emission=emission)
    assert isinstance(intensity, np.floating)


@pytest.mark.tools
@pytest.mark.parametrize("emission", ["blue", "hbeta", "green", "red"])
@pytest.mark.parametrize("spect_loc", [140, 145])
def test_full_hour(at, trex_spect_keogram_data, emission, spect_loc):

    # get spect data
    data = trex_spect_keogram_data["raw_data"]
    timestamp = data.timestamp

    # get list of intensities over time
    intensity = at.spectra.get_intensity(data, timestamp, spect_loc, spect_emission=emission)
    assert isinstance(intensity, list) is True
    assert (len(intensity) == len(timestamp)) is True


@pytest.mark.tools
@pytest.mark.parametrize("spect_loc", [140, 145])
def test_manual_emissions(at, trex_spect_keogram_data, spect_loc):

    # get spect data
    data = trex_spect_keogram_data["raw_data"]
    t_0 = datetime.datetime(2021, 2, 16, 9, 30, 0)

    # Attempt to get intensity for a band without specifying background
    with warnings.catch_warnings(record=True) as w:
        intensity = at.spectra.get_intensity(data, t_0, spect_loc, spect_band=[560.0, 565.0])
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "Wavelength band supplied without background band. No background subtraction will be performed." in str(w[-1].message)
    assert isinstance(intensity, np.floating)

    # Get band with background band
    intensity = at.spectra.get_intensity(data, t_0, spect_loc, spect_band=[560.0, 565.0], spect_band_bg=[567.0, 569.0])
    assert isinstance(intensity, np.floating)


@pytest.mark.tools
def test_input_errors(at, trex_spect_keogram_data):

    # get spect data
    data = trex_spect_keogram_data["raw_data"]
    t_0 = datetime.datetime(2021, 2, 16, 9, 30, 0)

    # improperly call the function with no bands specifies
    with pytest.raises(ValueError) as e_info:
        _ = at.spectra.get_intensity(data, t_0, 180)

    assert ("Please supply either spect_emission to choose which emission line " +
            "to integrate, or pass in a spect_band (and optionally spect_band_bg)" +
            " to manually select the wavelength range to integrate over") in str(e_info)

    # improperly try to pull out intensity using string and manual band specification
    with pytest.raises(ValueError) as e_info:
        _ = at.spectra.get_intensity(data, t_0, 180, spect_emission="green", spect_band=[550.0, 560.0])

    assert ("Only one of spect_emission and spect_band may be used to select the wavelength range for integration of spectra.") in str(e_info)

    # improperly try to pull out intensity using string and manual band background specification
    with pytest.raises(ValueError) as e_info:
        _ = at.spectra.get_intensity(data, t_0, 180, spect_emission="green", spect_band_bg=[550.0, 560.0])

    assert ("Only one of spect_emission and spect_band/spect_band_bg may be used to select the wavelength range for integration of spectra."
            ) in str(e_info)

    # improperly try to pull out intensity using string and manual band background specification
    with pytest.raises(ValueError) as e_info:
        _ = at.spectra.get_intensity(data, t_0, 180, spect_emission="green", spect_band_bg=[550.0, 560.0])

    assert ("Only one of spect_emission and spect_band/spect_band_bg may be used to select the wavelength range for integration of spectra."
            ) in str(e_info)

    # call with timestamp that doesn't correspond to data
    wrong_t = datetime.datetime(2020, 2, 16, 9, 30, 0)
    with pytest.raises(ValueError) as e_info:
        _ = at.spectra.get_intensity(data, wrong_t, 180, spect_emission="green")

    assert (f"Input does not contain data for requested timestamp: {wrong_t.strftime('%Y-%m-%d %H:%M:%S')}.") in str(e_info)
