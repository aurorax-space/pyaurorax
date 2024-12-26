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
from typing import Union, Tuple, Optional
from ...data.ucalgary import Skymap


def azimuth(skymap: Skymap,
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

        constant_elevation (int or float): 
            The elevation angle, in degrees from the horizon, to create contour of.

        min_elevation (int or float): 
            Optionally specify the elevation angle at which contour begins. Defaults to 5.
        
        min_elevation (int or float): 
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

    # First check that azimuth is valid
    if constant_azimuth < 0 or constant_azimuth > 360:
        raise ValueError(f"Azimuth of {constant_azimuth} is outside of valid range (0,360).")

    # Check that min/max elevations are valid if supplied
    if (min_elevation is not None):
        if (min_elevation < 0) or (min_elevation > 90):
            raise ValueError(f"Min_elevation of {min_elevation} is outside of valid range (0,90).")
    if (max_elevation is not None):
        if (max_elevation < 0) or (max_elevation > 90):
            raise ValueError(f"Minimum elevation of {min_elevation} is outside of valid range (0,90).")
    if (min_elevation is not None) and (max_elevation is not None):
        if (min_elevation >= max_elevation):
            raise ValueError(f"Min_elevation of {min_elevation} is outside of valid range (0,90).")

    # Pull azimuth and elevation arrays from skymap
    azimuth = skymap.full_azimuth
    elevation = skymap.full_elevation

    # Check if azimuth is None (in case someone tries this with a spectrograph skymap)
    if (azimuth is None):
        raise ValueError("Skymap's 'azimuth' value is None, cannot perform this function")

    # 360 degrees is just zero in skymap
    if constant_azimuth == 360:
        constant_azimuth = 0

    # Take a guess at a good number of points if None is supplied
    if n_points is None:
        step = 1
    else:
        step = 90 / n_points

    # Set bounds of elevation based on input
    if min_elevation is None:
        min_elevation = 5
    if max_elevation is None:
        max_elevation = 90

    # Iterate through elevation array in steps
    x_list = []
    y_list = []
    for el_min in np.arange(min_elevation, max_elevation + 1, step):

        # Get indices of this elevation slice
        el_max = el_min + step
        el_slice_idx = np.logical_and(elevation >= el_min, elevation < el_max)

        # Get index of pixel nearest to target azimuth
        masked_azimuth = np.where(el_slice_idx, azimuth, np.nan)
        diffs = np.abs(masked_azimuth - constant_azimuth)
        y, x = np.where(diffs == np.nanmin(diffs))

        if x.shape == (0, ) or y.shape == (0, ):
            continue

        # Add to master lists
        x_list.append(x[0])
        y_list.append(y[0])

    if remove_edge_cases:
        # Remove any points lying on the edge of CCD bounds and return
        x_list = np.array(x_list)
        y_list = np.array(y_list)
        edge_case_idx = np.where(np.logical_and.reduce([x_list > 0, x_list < elevation.shape[1] - 1, y_list > 0, y_list < elevation.shape[0] - 1]))
        x_list = x_list[edge_case_idx]
        y_list = y_list[edge_case_idx]
        return (x_list, y_list)
    else:
        # Convert to arrays, return
        return (np.array(x_list), np.array(y_list))
