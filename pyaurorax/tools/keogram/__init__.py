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
"""
Generate keograms.
"""

import datetime
import numpy as np
from typing import Optional, List, Literal, Tuple, Union
from ..classes.keogram import Keogram
from ...data.ucalgary import Skymap
from ._create import create as func_create
from ._create_custom import create_custom as func_create_custom

__all__ = ["KeogramManager"]


class KeogramManager:
    """
    The KeogramManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    def __init__(self):
        pass

    def create(self,
               images: np.ndarray,
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
            ValueError: issues encountered with supplied parameters
        """
        return func_create(images, timestamp, axis, spectra, wavelength, spect_emission, spect_band, spect_band_bg)

    def create_custom(
        self,
        images: np.ndarray,
        timestamp: List[datetime.datetime],
        coordinate_system: Literal["ccd", "geo", "mag"],
        width: int,
        x_locs: Union[List[Union[float, int]], np.ndarray],
        y_locs: Union[List[Union[float, int]], np.ndarray],
        preview: bool = False,
        skymap: Optional[Skymap] = None,
        altitude_km: Optional[Union[float, int]] = None,
        metric: Literal["mean", "median", "sum"] = "median",
    ) -> Keogram:
        """
        Create a keogram, from a custom slice of a set of images. The slice used is defined by a set of points, 
        in CCD, geographic, or geomagnetic coordinates, within the bounds of the image data. Keogram is created
        from the bottom up, meaning the first point will correspond to the bottom of the keogram data.

        Args:
            images (numpy.ndarray): 
                A set of images. Normally this would come directly from a data `read` call, but can also 
                be any arbitrary set of images. It is anticipated that the order of axes is [rows, cols, num_images]
                or [row, cols, channels, num_images]. If it is not, then be sure to specify the `axis` parameter
                accordingly.

            timestamp (List[datetime.datetime]): 
                A list of timestamps corresponding to each image.
            
            coordinate_system (str): 
                The coordinate system in which input points are defined. Valid options are "ccd", "geo", or "mag".
            
            width (int): 
                Width of the desired keogram slice, in CCD pixel units.

            x_locs (Sequence[float, int]): 
                Sequence of points giving the x-coordinates that define a path through the image data, from
                which to build the keogram.

            y_locs (Sequence[float, int]): 
                Sequence of points giving the y-coordinates that define a path through the image data, from
                which to build the keogram.

            preview (Optional[bool]): 
                When True, the first frame in images will be displayed, with the keogram slice plotted.

            skymap (Skymap): 
                The skymap to use in georeferencing when working in geographic or magnetic coordinates.

            altitude_km (float, int): 
                The altitude of the image data, in km, to use in georeferencing when working in geographic
                or magnetic coordinates.

            metric (str): 
                The metric used to compute values for each keogram pixel. Valid options are "median", "mean",
                and "sum". Defaults to "median".
            
        Returns:
            A `pyaurorax.tools.Keogram` object.

        Raises:
            ValueError: issues encountered with supplied parameters
        """
        return func_create_custom(images, timestamp, coordinate_system, width, x_locs, y_locs, preview, skymap, altitude_km, metric)
