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
Extract various metrics from a given bounding box.
"""

import datetime
import numpy as np
from typing import Sequence, Union, Literal, Optional
from ....data.ucalgary import Skymap
from ._azimuth import azimuth as func_azimuth
from ._ccd import ccd as func_ccd
from ._elevation import elevation as func_elevation
from ._geo import geo as func_geo
from ._mag import mag as func_mag

__all__ = ["ExtractMetricManager"]


class ExtractMetricManager:
    """
    The ExtractMetricManager object is initialized within every PyAuroraX object. It acts as a way to 
    access the submodules and carry over configuration information in the super class.
    """

    def __init__(self, aurorax_obj):
        self.__aurorax_obj = aurorax_obj

    def azimuth(self,
                images: np.ndarray,
                skymap: Skymap,
                azimuth_bounds: Sequence[Union[int, float]],
                metric: Literal["mean", "median", "sum"] = "median",
                n_channels: Optional[int] = None,
                show_preview: bool = False) -> np.ndarray:
        """
        Compute a metric of image data within an azimuthal boundary.

        Args:
            images (numpy.ndarray): 
                A set of images. Normally this would come directly from a data `read` call, but can also
                be any arbitrary set of images. It is anticipated that the order of axes is [rows, cols, num_images]
                or [row, cols, channels, num_images].
            
            skymap (pyaurorax.data.ucalgary.Skymap): 
                The skymap corresponding to the image data.

            azimuth_bounds (Sequence[int, float]): 
                A 2-element sequence specifying the azimuthal bounds from which to extract the metric. 
                Anticipated order is [az_min, az_max].

            metric (str): 
                The name of the metric that is to be computed for the bounded area. Valid metrics are `mean`,
                `median`, `sum`. Default is `median`.

            n_channels (int): 
                By default, function will assume the type of data passed as input - this argument can be used
                to manually specify the number of channels contained in image data.

            show_preview (bool): 
                Plot a preview of the bounded area.

        Returns:
            A numpy.ndarray containing the metrics computed within azimuth range, for all image frames.

        Raises:
            ValueError: issue encountered with value supplied in parameter
        """
        return func_azimuth(self.__aurorax_obj, images, skymap, azimuth_bounds, metric, n_channels, show_preview)

    def ccd(self,
            images: np.ndarray,
            ccd_bounds: Sequence[int],
            metric: Literal["mean", "median", "sum"] = "median",
            n_channels: Optional[int] = None,
            show_preview: bool = False) -> np.ndarray:
        """
        Compute a metric of image data within a CCD boundary.

        Args:
            images (numpy.ndarray): 
                A set of images. Normally this would come directly from a data `read` call, but can also
                be any arbitrary set of images. It is anticipated that the order of axes is [rows, cols, num_images]
                or [row, cols, channels, num_images].
            
            ccd_bounds (List[int]): 
                A 4-element sequence specifying the (inclusive) CCD bounds from which to extract the metric. 
                Anticipated order is [x0, x1, y0, y1].

            metric (str): 
                The name of the metric that is to be computed for the bounded area. Valid metrics are `mean`,
                `median`, `sum`. Defaults to `median`.

            n_channels (int): 
                By default, function will assume the type of data passed as input - this argument can be used
                to manually specify the number of channels contained in image data.
            
            show_preview (bool): 
                Plot a preview of the bounded area.

        Returns:
            A numpy.ndarray containing the metrics computed within CCD bounds, for all image frames.

        Raises:
            ValueError: issue encountered with value supplied in parameter
        """
        return func_ccd(self.__aurorax_obj, images, ccd_bounds, metric, n_channels, show_preview)

    def elevation(self,
                  images: np.ndarray,
                  skymap: Skymap,
                  elevation_bounds: Sequence[Union[int, float]],
                  metric: Literal["mean", "median", "sum"] = "median",
                  n_channels: Optional[int] = None,
                  show_preview: bool = False) -> np.ndarray:
        """
        Compute a metric of image data within an elevation boundary.

        Args:
            images (numpy.ndarray): 
                A set of images. Normally this would come directly from a data `read` call, but can also
                be any arbitrary set of images. It is anticipated that the order of axes is [rows, cols, num_images]
                or [row, cols, channels, num_images].
            
            skymap (pyaurorax.data.ucalgary.Skymap): 
                The skymap corresponding to the image data.

            elevation_bounds (Sequence): 
                A 2-element sequence specifying the elevation bounds from which to extract the metric. 
                Anticipated order is [el_min, el_max].

            metric (str): 
                The name of the metric that is to be computed for the bounded area. Valid metrics are `mean`,
                `median`, `sum`. Default is `median`.

            n_channels (int): 
                By default, function will assume the type of data passed as input - this argument can be used
                to manually specify the number of channels contained in image data.
            
            show_preview (bool): 
                Plot a preview of the bounded area.


        Returns:
            A numpy.ndarray containing the metrics computed within elevation range, for all image frames.

        Raises:
            ValueError: issue encountered with value supplied in parameter
        """
        return func_elevation(self.__aurorax_obj, images, skymap, elevation_bounds, metric, n_channels, show_preview)

    def geo(self,
            images: np.ndarray,
            skymap: Skymap,
            altitude_km: Union[int, float],
            lonlat_bounds: Sequence[Union[int, float]],
            metric: Literal["mean", "median", "sum"] = "median",
            n_channels: Optional[int] = None,
            show_preview: bool = False) -> np.ndarray:
        """
        Compute a metric of image data within a geographic lat/lon boundary.

        Args:
            images (numpy.ndarray): 
                A set of images. Normally this would come directly from a data `read` call, but can also
                be any arbitrary set of images. It is anticipated that the order of axes is [rows, cols, num_images]
                or [row, cols, channels, num_images].
            
            skymap (pyaurorax.data.ucalgary.Skymap): 
                The skymap corresponding to the image data.
            
            altitude_km (int or float): 
                The altitude of the image data in kilometers.

            lonlat_bounds (Sequence): 
                A 4-element sequence specifying the lat/lon bounds from which to extract the metric. 
                Anticipated order is [lon_0, lon_1, lat_0, lat_1].

            metric (str): 
                The name of the metric that is to be computed for the bounded area. Valid metrics are `mean`,
                `median`, `sum`. Default is `median`.

            n_channels (int): 
                By default, function will assume the type of data passed as input - this argument can be used
                to manually specify the number of channels contained in image data.
            
            show_preview (bool): 
                Plot a preview of the bounded area.

        Returns:
            A numpy.ndarray containing the metrics computed within elevation range, for all image frames.

        Raises:
            ValueError: issue encountered with value supplied in parameter
        """
        return func_geo(self.__aurorax_obj, images, skymap, altitude_km, lonlat_bounds, metric, n_channels, show_preview)

    def mag(self,
            images: np.ndarray,
            timestamp: datetime.datetime,
            skymap: Skymap,
            altitude_km: Union[int, float],
            lonlat_bounds: Sequence[Union[int, float]],
            metric: Literal["mean", "median", "sum"] = "median",
            n_channels: Optional[int] = None,
            show_preview: bool = False) -> np.ndarray:
        """
        Compute a metric of image data within a magnetic lat/lon boundary.

        Args:
            images (numpy.ndarray): 
                A set of images. Normally this would come directly from a data `read` call, but can also
                be any arbitrary set of images. It is anticipated that the order of axes is [rows, cols, num_images]
                or [row, cols, channels, num_images].
            
            timestamp (List[datetime.datetime]): 
                A list of timestamps corresponding to each image.
            
            skymap (pyaurorax.data.ucalgary.Skymap): 
                The skymap corresponding to the image data.
            
            altitude_km (int or float): 
                The altitude of the image data in kilometers.

            lonlat_bounds (Sequence): 
                A 4-element sequence specifying the magnetic lat/lon bounds from which to extract the metric. 
                Anticipated order is [lon_0, lon_1, lat_0, lat_1].

            metric (str): 
                The name of the metric that is to be computed for the bounded area. Valid metrics are `mean`,
                `median`, `sum`. Default is `median`.

            n_channels (int): 
                By default, function will assume the type of data passed as input - this argument can be used
                to manually specify the number of channels contained in image data.

            show_preview (bool): 
                Plot a preview of the bounded area.

        Returns:
            A numpy.ndarray containing the metrics computed within elevation range, for all image frames.

        Raises:
            ValueError: issue encountered with value supplied in parameter
        """
        return func_mag(self.__aurorax_obj, images, timestamp, skymap, altitude_km, lonlat_bounds, metric, n_channels, show_preview)
