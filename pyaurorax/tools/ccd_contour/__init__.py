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
Obtain contours in pixel coordinates from a skymap for plotting over CCD images.
"""

import datetime
import numpy as np
from typing import Optional, Union, Tuple
from ...data.ucalgary import Skymap
from ._azimuth import azimuth as func_azimuth
from ._elevation import elevation as func_elevation
from ._geo import geo as func_geo
from ._mag import mag as func_mag

__all__ = ["CCDContourManager"]


class CCDContourManager:
    """
    The CCDContourManager object is initialized within every PyAuroraX object. It acts as a way to 
    access the submodules and carry over configuration information in the super class.
    """

    def __init__(self):
        pass

    def azimuth(self,
                skymap: Skymap,
                constant_azimuth: Union[int, float],
                min_elevation: Optional[Union[int, float]] = None,
                max_elevation: Optional[Union[int, float]] = None,
                n_points: Optional[int] = None,
                remove_edge_cases: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """
        Obtain CCD Coordinates of a line of constant latitude.

        Args:
            skymap (pyaurorax.data.ucalgary.Skymap): 
                The skymap corresponding to the CCD image data to generate contours for.

            constant_azimuth (int or float): 
                The azimuth angle, in degrees, to create contour of.

            min_elevation (int or float): 
                Optionally specify the elevation angle at which contour begins. Defaults to 5.
            
            max_elevation (int or float): 
                Optionally specify the elevation angle at which contour begins. Defaults to 90.

            n_points (int or float): 
                Optionally specify the number of points used to define a contour. By default
                a reasonable value is selected automatically.

            remove_edge_cases (bool): 
                Due to the nature of skymaps, often, around the edge of CCD data, contours will
                have often undesired behaviour due to being bounded within the CCD range. The result
                is flattened contours along the edge of CCD boundaries. This is completely expected,
                and these points are removed by default, completely for aesthetic choices. Set this 
                keyword to False to keep all points in the contour.
                
        Returns:
            A tuple (x_pix, y_pix) of numpy arrays containing the coordinates, in pixel units, of
            the azimuth contour.

        Raises:
            ValueError: invalid azimuth supplied.
        """
        return func_azimuth(skymap, constant_azimuth, min_elevation, max_elevation, n_points, remove_edge_cases)

    def elevation(self,
                  skymap: Skymap,
                  constant_elevation: Union[int, float],
                  n_points: Optional[int] = None,
                  remove_edge_cases: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """
        Obtain CCD Coordinates of a line of constant elevation.

        Args:
            skymap (pyaurorax.data.ucalgary.Skymap): 
                The skymap corresponding to the CCD image data to generate contours for.

            constant_elevation (int or float): 
                The elevation angle, in degrees from the horizon, to create contour of.

            n_points (int or float): 
                Optionally specify the number of points used to define a contour. By default
                a reasonable value is selected automatically.

            remove_edge_cases (bool): 
                Due to the nature of skymaps, often, around the edge of CCD data, contours will
                have often undesired behaviour due to being bounded within the CCD range. The result
                is flattened contours along the edge of CCD boundaries. This is completely expected,
                and these points are removed by default, completely for aesthetic choices. Set this 
                keyword to False to keep all points in the contour.
                
        Returns:
            A tuple (x_pix, y_pix) of numpy arrays containing the coordinates, in pixel units, of
            the elevation contour.

        Raises:
            ValueError: invalid elevation supplied.
        """
        return func_elevation(skymap, constant_elevation, n_points, remove_edge_cases)

    def geo(self,
            skymap: Skymap,
            altitude_km: Union[int, float],
            contour_lats: Optional[Union[np.ndarray, list]] = None,
            contour_lons: Optional[Union[np.ndarray, list]] = None,
            constant_lat: Optional[Union[float, int]] = None,
            constant_lon: Optional[Union[float, int]] = None,
            n_points: Optional[int] = None,
            remove_edge_cases: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """
        Obtain CCD Coordinates of a line of constant geographic latitude, constant geographic longitude, or a custom contour
        defined in geographic coordinates.

        Args:
            skymap (pyaurorax.data.ucalgary.Skymap): 
                The skymap corresponding to the CCD image data to generate contours for.

            altitude_km (int or float): 
                The altitude of the image data to create contours for, in kilometers.

            contour_lats (ndarray or list): 
                    Sequence of geographic latitudes defining a contour.
                
            contour_lons (ndarray or list): 
                Sequence of geographic longitudes defining a contour.

            constant_lat (float or int): 
                Geographic Latitude at which to create line of constant latitude.
            
            constant_lon (float or int): 
                Geographic Longitude at which to create line of constant longitude.

            n_points (int or float): 
                Optionally specify the number of points used to define a contour. By default
                a reasonable value is selected automatically.
            
            remove_edge_cases (bool): 
                Due to the nature of skymaps, often, around the edge of CCD data, contours will
                have often undesired behaviour due to being bounded within the CCD range. The result
                is flattened contours along the edge of CCD boundaries. This is completely expected,
                and these points are removed by default, completely for aesthetic choices. Set this 
                keyword to False to keep all points in the contour.
                
        Returns:
            A tuple (x_pix, y_pix) of numpy arrays containing the coordinates, in pixel units, of
            the elevation contour.

        Raises:
            ValueError: invalid elevation supplied.
        """
        return func_geo(skymap, altitude_km, contour_lats, contour_lons, constant_lat, constant_lon, n_points, remove_edge_cases)

    def mag(self,
            skymap: Skymap,
            timestamp: datetime.datetime,
            altitude_km: Union[int, float],
            contour_lats: Optional[Union[np.ndarray, list]] = None,
            contour_lons: Optional[Union[np.ndarray, list]] = None,
            constant_lat: Optional[Union[float, int]] = None,
            constant_lon: Optional[Union[float, int]] = None,
            n_points: Optional[int] = None,
            remove_edge_cases: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """
        Obtain CCD Coordinates of a line of constant magnetic latitude, constant magnetic longitude, or a custom contour
        defined in magnetic coordinates.

        Args:
            skymap (pyaurorax.data.ucalgary.Skymap): 
                The skymap corresponding to the CCD image data to generate contours for.

            timestamp (datetime.datetime): 
                The timestamp used for AACGM Conversions.

            altitude_km (int or float): 
                The altitude of the image data to create contours for, in kilometers.

            contour_lats (ndarray or list): 
                    Sequence of magnetic latitudes defining a contour.
                
            contour_lons (ndarray or list): 
                Sequence of magnetic longitudes defining a contour.

            constant_lat (float or int): 
                Magnetic Latitude at which to create line of constant latitude.
            
            constant_lon (float or int): 
                Magnetic Longitude at which to create line of constant longitude.

            n_points (int or float): 
                Optionally specify the number of points used to define a contour. By default
                a reasonable value is selected automatically.
            
            remove_edge_cases (bool): 
                Due to the nature of skymaps, often, around the edge of CCD data, contours will
                have often undesired behaviour due to being bounded within the CCD range. The result
                is flattened contours along the edge of CCD boundaries. This is completely expected,
                and these points are removed by default, completely for aesthetic choices. Set this 
                keyword to False to keep all points in the contour.
                
        Returns:
            A tuple (x_pix, y_pix) of numpy arrays containing the coordinates, in pixel units, of
            the elevation contour.

        Raises:
            ValueError: invalid elevation supplied.
        """
        return func_mag(skymap, timestamp, altitude_km, contour_lats, contour_lons, constant_lat, constant_lon, n_points, remove_edge_cases)
