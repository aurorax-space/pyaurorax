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
from typing import Union, Optional, Literal, Sequence
from ....data.ucalgary import Skymap


def geo(images: np.ndarray,
        skymap: Skymap,
        altitude_km: Union[int, float],
        lonlat_bounds: Sequence[Union[int, float]],
        metric: Literal["mean", "median", "sum"] = "median",
        n_channels: Optional[int] = None) -> np.ndarray:
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

    Returns:
        A numpy.ndarray containing the metrics computed within elevation range, for all image frames.

    Raises:
        ValueError: issue encountered with value supplied in parameter
    """

    # Select individual lats/lons from list
    lon_0 = lonlat_bounds[0]
    lon_1 = lonlat_bounds[1]
    lat_0 = lonlat_bounds[2]
    lat_1 = lonlat_bounds[3]

    # Determine if we are using single or 3 channel
    images = np.squeeze(images)
    if n_channels is not None:
        n_channels = n_channels
    else:
        n_channels = 1
        if (len(images.shape) == 3):
            # single channel
            n_channels = 1
        elif (len(images.shape) == 4):
            # three channel
            n_channels = 3

    # Ensure that coordinates are valid
    if lat_0 > 90 or lat_0 < -90:
        raise ValueError("Invalid Latitude: " + str(lat_0))
    elif lat_1 > 90 or lat_1 < -90:
        raise ValueError("Invalid Latitude: " + str(lat_1))
    elif lon_0 > 360 or lon_0 < -180:
        raise ValueError("Invalid Longitude: " + str(lon_0))
    elif lon_1 > 360 or lon_1 < -180:
        raise ValueError("Invalid Longitude: " + str(lon_1))

    # Convert(0,360) longitudes to (-180,180) if entered as such
    if lon_0 > 180:
        lon_0 -= 360.0
    if lon_1 > 180:
        lon_1 -= 360.0

    # Ensure that coordinates are properly ordered
    if lat_0 > lat_1:
        lat_0, lat_1 = lat_1, lat_0
    if lon_0 > lon_1:
        lon_0, lon_1 = lon_1, lon_0

    # Ensure that this is a valid polygon
    if (lat_0 == lat_1) or (lon_0 == lon_1):
        raise ValueError("Polygon defined with zero area.")

    # Obtain lat/lon arrays from skymap
    if (altitude_km * 1000.0 in skymap.full_map_altitude):
        altitude_idx = np.where(altitude_km * 1000.0 == skymap.full_map_altitude)

        lats = np.squeeze(skymap.full_map_latitude[altitude_idx, :, :])
        lons = np.squeeze(skymap.full_map_longitude[altitude_idx, :, :])
        lons[np.where(lons > 180)] -= 360.0  # Fix skymap to be in (-180,180) format

    else:
        # Make sure altitude is in range that can be interpolated
        if (altitude_km * 1000.0 < skymap.full_map_altitude[0]) or (altitude_km * 1000.0 > skymap.full_map_altitude[2]):
            raise ValueError("Altitude " + str(altitude_km) + " outside valid range of " +
                             str((skymap.full_map_altitude[0] / 1000.0, skymap.full_map_altitude[2] / 1000.0)))

        # Initialze empty lat/lon arrays
        lats = np.full(np.squeeze(skymap.full_map_latitude[0, :, :]).shape, np.nan, dtype=skymap.full_map_latitude[0, :, :].dtype)
        lons = lats.copy()

        # Interpolate lats and lons at desired altitude
        for i in range(skymap.full_map_latitude.shape[1]):
            for j in range(skymap.full_map_latitude.shape[2]):
                lats[i, j] = np.interp(altitude_km * 1000.0, skymap.full_map_altitude, skymap.full_map_latitude[:, i, j])
                lons[i, j] = np.interp(altitude_km * 1000.0, skymap.full_map_altitude, skymap.full_map_longitude[:, i, j])

        lons[np.where(lons > 180)] -= 360.0  # Fix skymap to be in (-180,180) format

    # Obtain indices into skymap within lat/lon range
    bound_idx = np.where(np.logical_and.reduce((lats > float(lat_0), lats < float(lat_1), lons > float(lon_0), lons < float(lon_1))))

    # If boundaries contain no data, raise error
    if len(bound_idx[0]) == 0 or len(bound_idx[1]) == 0:
        raise ValueError("No data within desired bounds.")

    # Convert from skymap coords to image coords
    bound_idx = tuple(i - 1 for i in bound_idx)
    bound_idx = tuple(np.maximum(idx, 0) for idx in bound_idx)

    # Slice out the bounded data
    if n_channels == 1:
        bound_data = images[bound_idx[0], bound_idx[1], :]
    elif n_channels == 3:
        bound_data = images[bound_idx[0], bound_idx[1], :, :]
    else:
        raise ValueError("Unrecognized image format with shape: " + str(images.shape))

    # Compute metric of interest
    if metric == 'median':
        result = np.median(bound_data, axis=0)
    elif metric == 'mean':
        result = np.mean(bound_data, axis=0)
    elif metric == 'sum':
        result = np.sum(bound_data, axis=0)
    else:
        raise ValueError("Metric " + str(metric) + " is not recognized.")

    return result
