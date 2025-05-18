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

import numpy as np
from ..._util import show_warning


def get_intensity(spect_data, timestamp, spect_loc, spect_emission, spect_band, spect_band_bg):

    # The user must either choose to integrate based on one of the default emissions using spect_emission
    # or pass in a manual spect_band (and optionally spect_band_bg for the background)
    if (spect_emission is None) and (spect_band is None):
        raise ValueError("Please supply either spect_emission to choose which emission line to integrate, or pass " +
                         "in a spect_band (and optionally spect_band_bg) to manually select the wavelength range to integrate over")

    if (spect_emission is not None) and ((spect_band is not None) or (spect_band_bg is not None)):
        if spect_band is not None:
            raise ValueError("Only one of spect_emission and spect_band may be used to select the wavelength range for integration of spectra.")
        elif spect_band_bg is not None:
            raise ValueError(
                "Only one of spect_emission and spect_band/spect_band_bg may be used to select the wavelength range for integration of spectra.")

    # Determine integration bounds for spectrograph data
    if (spect_emission is not None):
        wavelength_range = {
            'green': [557.0 - 1.5, 557.0 + 1.5],
            'red': [630.0 - 1.5, 630.0 + 1.5],
            'blue': [427.8 - 3.0, 427.8 + 0.5],
            'hbeta': [486.1 - 1.5, 486.1 + 1.5]
        }[spect_emission]

        wavelength_bg_range = {
            'green': [552.0 - 1.5, 552.0 + 1.5],
            'red': [625.0 - 1.5, 625.0 + 1.5],
            'blue': [430.0 - 1.0, 430.0 + 1.0],
            'hbeta': [480.0 - 1.0, 480.0 + 1.0]
        }[spect_emission]

    elif (spect_band is not None):
        wavelength_range = spect_band
        if spect_band_bg is None:
            show_warning(
                "Wavelength band supplied without background band. No background subtraction will be performed.",
                stacklevel=1,
            )
            wavelength_bg_range = None
        else:
            wavelength_bg_range = spect_band_bg
    else:
        raise ValueError("Please supply either spect_emission to choose which emission line to integrate, or pass " +  # pragma: nocover
                         "in a spect_band (and optionally spect_band_bg) to manually select the wavelength range to integrate over")

    # Convert input timestamps to list if required
    if (not isinstance(timestamp, list)):
        timestamp = [timestamp]

    # Extract spectrograph data from Data object
    spectra = spect_data.data
    spect_data_timestamps = np.array(spect_data.timestamp)
    wavelength = spect_data.metadata[0]['wavelength']

    # Get integration region (wavelength range) indices
    int_w = (np.where((wavelength >= wavelength_range[0]) & (wavelength <= wavelength_range[1])))[0]
    if (wavelength_bg_range is not None):
        int_bg_w = (np.where((wavelength >= wavelength_bg_range[0]) & (wavelength <= wavelength_bg_range[1])))[0]
    else:
        int_bg_w = None

    # Check that valid integration indices were found
    if (len(int_w)) == 0:
        raise ValueError(f"Invalid integration range ({spect_band}) for spect_band. Ensure range is within " +
                         "the wavelength range of the spectrograph data, which is [{wavelength[0]},{wavelength[-1]}]")

    absolute_intensity = []

    # Iterate through all requested spectra
    for i in range(len(timestamp)):

        # Get the spect spatial bin index and timestamp idx
        ts = timestamp[i]
        epoch_idx = (np.where(spect_data_timestamps == ts))[0]

        # Check for issues with supplied location / time
        if len(epoch_idx) == 0:
            raise ValueError(f"Input does not contain data for requested timestamp: {ts.strftime('%Y-%m-%d %H:%M:%S')}.")
        if len(epoch_idx) > 1:
            raise ValueError(f"Input contains multiple data points for requested timestamp: {ts.strftime('%Y-%m-%d %H:%M:%S')}.")  # pragma: nocover

        # Slice out the spectrum of interest
        spectrum = np.squeeze(spectra[:, spect_loc, epoch_idx])
        rayleighs = np.trapezoid(spectrum[int_w], x=wavelength[int_w])

        if wavelength_bg_range is not None:
            if int_bg_w is not None:
                rayleighs -= np.trapezoid(spectrum[int_bg_w], x=wavelength[int_bg_w])

        absolute_intensity.append(rayleighs)

    # Return as a list, unless it's a single element - then return as a scalar
    if len(absolute_intensity) == 1:
        return absolute_intensity[0]
    else:
        return absolute_intensity
