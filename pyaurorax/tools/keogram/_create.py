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

import datetime
import warnings
import numpy as np
from typing import List, Literal, Optional, Tuple
from ..classes.keogram import Keogram


def create(images: np.ndarray,
           timestamp: List[datetime.datetime],
           axis: int = 0,
           spectra: bool = False,
           wavelength: Optional[np.ndarray] = None,
           spect_emission: Literal["green", "red", "blue", "hbeta"] = "green",
           spect_band: Optional[Tuple[float, float]] = None,
           spect_band_bg: Optional[Tuple[float, float]] = None) -> Keogram:
    """
    Create a keogram from a set of images.

    Args:
        images (numpy.ndarray): 
            A set of images. Normally this would come directly from a data `read` call, but can also 
            be any arbitrary set of images. It is anticipated that the order of axes is [rows, cols, num_images]
            or [row, cols, channels, num_images]. If it is not, then be sure to specify the `axis` parameter
            accordingly.

        timestamp (List[datetime.datetime]): 
            A list of timestamps corresponding to each image.

        axis (int): 
            The axis to extract the keogram slice from. Default is `0`, meaning the rows (or Y) axis.

        spectra (bool): 
            Make a keogram out of spectrograph data, for a specific emission. Defaults to False (ASI data).

        wavelength (numpy.ndarray): 
            The wavelength array corresponding to spectrograph data. If spectra=True, this parameter
            must be supplied.

        spect_emission (str): 
            The emission (green, red, blue, hbeta) to prepare from spectrograph data. Default is 
            'green' (557.7 nm emission).

        spect_band (Tuple[float]): 
            Manual selection of the wavelength region to integrate for obtaining emissions. Use this
            to prepare emissions that are not available in spect_emission.

        spect_band_bg (Tuple[float]): 
            Manual selection of the wavelength region to subtract from integration for manually
            chosen emissions, via the spect_band argument.

    Returns:
        A `pyaurorax.tools.Keogram` object.

    Raises:
        ValueError: issue with supplied parameters.
    """

    # First check if we are dealing with spectrograph data
    if spectra:

        instrument_type = 'spectrograph'
        middle_column_idx = None

        if axis != 0:
            raise ValueError(f"Cannot create keogram for spectrograph data along axis other than 0, received axis: {axis}.")
        if wavelength is None:
            raise ValueError("Parameter 'wavelength' must be supplied when using spectrograph data.")

        # Determine integration bounds for spectrograph data
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

        # Check if manual integration bands were supplied
        if spect_band is not None:
            wavelength_range = spect_band
            if spect_band_bg is None:
                warnings.warn(
                    "Wavelength band supplied without background band. No background subtraction will be performed.",
                    stacklevel=1,
                )
                wavelength_bg_range = None
            else:
                wavelength_bg_range = spect_band_bg

        # Extract wavelength from metadata, and get integration indices
        int_w = np.where((wavelength >= wavelength_range[0]) & (wavelength <= wavelength_range[1]))
        if wavelength_bg_range is not None:
            int_bg_w = np.where((wavelength >= wavelength_bg_range[0]) & (wavelength <= wavelength_bg_range[1]))

        # Integrate all spectrograph pixels to get emission
        n_wavelengths_in_spectra = images.shape[0]
        n_spatial_bins = images.shape[1]
        n_timestamps_in_spectra = images.shape[2]
        n_wavelengths = wavelength.shape[0]
        n_timestamps = len(timestamp)

        if n_timestamps != n_timestamps_in_spectra:
            raise ValueError(f"Mismatched timestamp dimensions. Received {n_timestamps} "
                             f"timestamps for spectrograph data with {n_timestamps_in_spectra} timestamps.")

        if n_wavelengths != n_wavelengths_in_spectra:
            raise ValueError(f"Mismatched wavelength dimensions. Received {n_wavelengths} "
                             f"wavelengths for spectrograph data with {n_wavelengths_in_spectra} wavelengths.")

        # set y-axis
        ccd_y = np.arange(0, n_spatial_bins)

        # Initialize keogram array
        keo_arr = np.full([n_spatial_bins, n_timestamps], 0, dtype=images.dtype)

        # Iterate through each timestamp and compute emissions for all spatial bins
        for i in range(0, n_timestamps):

            # Integrate over wavelengths to get Rayleighs
            iter_spectra = images[:, :, i]

            rayleighs = np.trapz(iter_spectra[int_w[0], :], x=wavelength[int_w[0]], axis=0)

            if wavelength_bg_range is not None:
                if int_bg_w is not None:  #type: ignore
                    rayleighs -= np.trapz(
                        iter_spectra[int_bg_w[0], :],  #type: ignore
                        x=wavelength[int_bg_w[0]],  #type: ignore
                        axis=0)

            rayleighs = np.nan_to_num(rayleighs, nan=0.0)
            rayleighs[np.where(rayleighs < 0.0)] = 0.0

            keo_arr[:, i] = rayleighs

    # Otherwise, for ASI data, slice keogram as required
    else:
        instrument_type = 'asi'

        # set y axis
        ccd_y = np.arange(0, images.shape[axis])

        # determine if we are single or 3 channel
        n_channels = 1
        if (len(images.shape) == 3):
            # single channel
            n_channels = 1
        elif (len(images.shape) == 4):
            # three channel
            n_channels = 3
        else:
            ValueError("Unable to determine number of channels based on the supplied images. Make sure you are supplying a " +
                       "[rows,cols,images] or [rows,cols,channels,images] sized array.")

        # initialize keogram data
        n_rows = images.shape[0]
        n_imgs = images.shape[-1]
        if (n_channels == 1):
            keo_arr = np.full([n_rows, n_imgs], 0, dtype=images.dtype)
        else:
            keo_arr = np.full([n_rows, n_imgs, n_channels], 0, dtype=images.dtype)

        # extract the keogram slices
        middle_column_idx = int(np.floor((images.shape[1]) / 2 - 1))
        for img_idx in range(0, n_imgs):
            if (n_channels == 1):
                # single channel
                frame = images[:, :, img_idx]
                frame_middle_slice = frame[:, middle_column_idx]
                keo_arr[:, img_idx] = frame_middle_slice
            else:
                # 3-channel
                frame = images[:, :, :, img_idx]
                frame_middle_slice = frame[:, middle_column_idx, :]
                keo_arr[:, img_idx, :] = frame_middle_slice

    # create the keogram object
    keo_obj = Keogram(data=keo_arr, slice_idx=middle_column_idx, timestamp=timestamp, ccd_y=ccd_y, instrument_type=instrument_type)

    # return
    return keo_obj
