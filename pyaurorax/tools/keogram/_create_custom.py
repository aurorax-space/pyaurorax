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
import aacgmv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from typing import List, Literal, Union, Optional
from ..classes.keogram import Keogram
from ...data.ucalgary import Skymap


# Helper function that returns all array indices within
# the polygon defined by input vertices.
def __indices_in_polygon(vertices, image_shape):
    """
    Function to obtain all indices of an array/image, within the 
    polygon defined by input list of ordered vertices.
    """
    # Create a Path object using the vertices
    path = Path(vertices)

    # Create a grid of points covering the image shape
    x, y = np.meshgrid(np.arange(image_shape[1]), np.arange(image_shape[0]))
    points = np.vstack((x.flatten(), y.flatten())).T

    # Create a mask indicating which points are inside the polygon
    mask = path.contains_points(points).reshape(image_shape)

    # Get all indices inside or on the boundary of the polygon
    indices_inside = np.argwhere(mask)

    return indices_inside


def __haversine_distances(target_lat, target_lon, lat_array, lon_array):
    """
    Computes the distance on the globe between target lat/lon,
    and all points defined by lat/lon arrays.
    """
    # Earth radius (meters)
    r = 6371000.0

    # Convert degrees to radians
    phi1 = np.radians(target_lat)
    phi2 = np.radians(lat_array)
    delta_phi = np.radians(lat_array - target_lat)
    delta_lambda = np.radians(lon_array - target_lon)

    # Haversine formula
    a = np.sin(delta_phi / 2.0)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    return r * c


# Helper function for handling magnetic lat/lon inputs
def __convert_latlon_to_ccd(lon_locs, lat_locs, timestamp, skymap: Skymap, altitude_km, magnetic):
    """
    Function for handling lat/lon inputs. Takes the lat/lon
    locations, and uses a skymap to convert those locations
    to CCD (image index) coordinates.
    """
    # Obtain lat/lon arrays from skymap
    if (altitude_km * 1000.0 in skymap.full_map_altitude):
        altitude_idx = np.where(altitude_km * 1000.0 == skymap.full_map_altitude)

        lats = np.squeeze(skymap.full_map_latitude[altitude_idx, :, :])
        lons = np.squeeze(skymap.full_map_longitude[altitude_idx, :, :])
        lons[np.where(lons > 180)] -= 360.0

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

    # Convert skymap to magnetic coords if necessary
    if magnetic:
        mag_lats, mag_lons, mag_alts = aacgmv2.convert_latlon_arr(lats.flatten(),
                                                                  lons.flatten(), (lons * 0.0).flatten(),
                                                                  timestamp[0],
                                                                  method_code='G2A')
        lats = np.reshape(mag_lats, lats.shape)
        lons = np.reshape(mag_lons, lons.shape)

    # Iterate through each target point
    x_locs = []
    y_locs = []
    for target_lat, target_lon in zip(lat_locs, lon_locs):

        # Make sure lat/lon falls within skymap
        if target_lat < np.nanmin(lats) or target_lat > np.nanmax(lats):
            continue
            raise ValueError(f"Latitude {target_lat} is outside this skymap's valid range of {(np.nanmin(lats),np.nanmax(lats))}.")
        if target_lon < np.nanmin(lons) or target_lon > np.nanmax(lons):
            continue
            raise ValueError(f"Longitude {target_lon} is outside this skymap's valid range of {(np.nanmin(lons),np.nanmax(lons))}.")

        # Compute haversine distance between all points in skymap
        haversine_diff = __haversine_distances(target_lat, target_lon, lats, lons)

        # Obtain the skymap indices of the nearest point
        nan_mask = np.isnan(haversine_diff)
        masked_data = np.ma.masked_array(haversine_diff, mask=nan_mask)
        nearest_indices = np.unravel_index(np.ma.argmin(masked_data), haversine_diff.shape)

        # Convert indices to CCD Coordinates
        y_loc = nearest_indices[0] - 1
        if y_loc < 0:
            y_loc = 0
        x_loc = nearest_indices[1] - 1
        if x_loc < 0:
            x_loc = 0

        x_locs.append(x_loc)
        y_locs.append(y_loc)

    x_locs = np.array(x_locs)
    y_locs = np.array(y_locs)

    return x_locs, y_locs


def create_custom(
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
            The altitude of the image data, in km, to use in georeferencing when working in goegraphic
            or magnetic coordinates.

        metric (str): 
            The metric used to compute values for each keogram pixel. Valid options are "median", "mean",
            and "sum". Defaults to "median".
        
    Returns:
        A `pyaurorax.tools.Keogram` object.

    Raises:
    """

    # If using CCD coordinates we don't need a skymao or altitude
    if (coordinate_system == 'ccd') and (skymap is not None or altitude_km is not None):
        raise ValueError("Confliction in passing a Skymap in when working in CCD coordinates. Skymap is obsolete.")

    # convert any lists to np.arrays  and check shape
    x_locs = np.array(x_locs)
    y_locs = np.array(y_locs)

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

    # Initialize empty keogram array
    keo_arr = np.squeeze(np.full((x_locs.shape[0] - 1, len(timestamp), n_channels), 0))

    if len(x_locs.shape) != 1:
        raise ValueError(f"X coordinates may not be multidimensional. Sequence passed with shape {x_locs.shape}")
    if len(y_locs.shape) != 1:
        raise ValueError(f"Y coordinates may not be multidimensional. Sequence passed with shape {y_locs.shape}")
    if len(x_locs.shape) != len(y_locs.shape):
        raise ValueError(f"X and Y coordinates must have same length. Sequences passed with shapes {x_locs.shape} and {y_locs.shape}")

    # Convert lat/lon coordinates to CCD
    if coordinate_system == 'mag':
        if (skymap is None or altitude_km is None):
            raise ValueError("When magnetic coordinates, a Skymap object and Altitude must be passed in through the skymap argument.")
        x_locs, y_locs = __convert_latlon_to_ccd(x_locs, y_locs, timestamp, skymap, altitude_km, magnetic=True)
    elif coordinate_system == 'geo':
        if (skymap is None or altitude_km is None):
            raise ValueError("When geographic coordinates, a Skymap object and Altitude must be passed in through the skymap argument.")
        x_locs, y_locs = __convert_latlon_to_ccd(x_locs, y_locs, timestamp, skymap, altitude_km, magnetic=False)

    # We will use the first image as a preview
    if n_channels == 1:
        preview_img = images.copy()[:, :, 0]
    else:
        preview_img = images.copy()[:, :, :, 0]

    # Now working in CCD Coordinates
    x_max = images.shape[1] - 1
    y_max = images.shape[0] - 1

    # Remove any points that are not within the image CCD
    parsed_x_locs = []
    parsed_y_locs = []
    for i in range(x_locs.shape[0]):
        x = x_locs[i]
        y = y_locs[i]

        if x < 0 or x > x_max:
            continue
        if y < 0 or y > y_max:
            continue

        parsed_x_locs.append(x)
        parsed_y_locs.append(y)
    x_locs = np.array(parsed_x_locs)
    y_locs = np.array(parsed_y_locs)

    # Make sure all supplied points are within image bounds # NOTE: This should be good to remove as it shouldn't hit, testing needed
    if len(np.where(np.logical_or(x_locs < 0, x_locs > x_max))[0]) != 0:
        raise ValueError("The following CCD coordinates passed in through x_locs are outside of the CCD image range: " +
                         str(x_locs[np.where(np.logical_or(x_locs < 0, x_locs > x_max))]))
    if len(np.where(np.logical_or(y_locs < 0, y_locs > y_max))[0]) != 0:
        raise ValueError("The following CCD coordinates passed in through y_locs are outside of the CCD image range: " +
                         str(y_locs[np.where(np.logical_or(y_locs < 0, y_locs > y_max))]))

    # Iterate points in pairs of two
    path_counter = 0
    for i in range(x_locs.shape[0] - 1):

        # Points of concern for this iteration
        x_0 = x_locs[i]
        x_1 = x_locs[i + 1]
        y_0 = y_locs[i]
        y_1 = y_locs[i + 1]

        # Compute the unit vector between the two points
        dx = x_1 - x_0
        dy = y_1 - y_0
        length = np.sqrt(dx**2 + dy**2)
        if length == 0:
            continue

        dx /= length
        dy /= length

        # Compute orthogonal unit vector
        perp_dx = -dy
        perp_dy = dx

        # Calculate (+/-) offsets for each perpendicular direction
        offset1_x = perp_dx * width / 2
        offset1_y = perp_dy * width / 2
        offset2_x = -perp_dx * width / 2
        offset2_y = -perp_dy * width / 2

        # Calculate vertices in correct order for this polygon
        vertex1 = (int(x_0 + offset1_x), int(y_0 + offset1_y))
        vertex2 = (int(x_1 + offset1_x), int(y_1 + offset1_y))
        vertex3 = (int(x_1 + offset2_x), int(y_1 + offset2_y))
        vertex4 = (int(x_0 + offset2_x), int(y_0 + offset2_y))

        # Append vertices in the correct order to form a closed polygon
        vertices = [vertex1, vertex2, vertex3, vertex4]

        # Obtain the indexes into the image of this polygon
        indices_inside = __indices_in_polygon(vertices, (images.shape[0], images.shape[1]))

        if np.any(np.array(indices_inside.shape) == 0):
            continue

        row_idx, col_idx = zip(*indices_inside)

        if n_channels == 1:
            # Update the preview image
            preview_img[row_idx, col_idx] = np.iinfo(preview_img.dtype).max

            # Extract metric from all images and add to keogram
            if metric == 'median':
                pixel_keogram = np.median(images[row_idx, col_idx, :], axis=0)
            elif metric == 'mean':
                pixel_keogram = np.mean(images[row_idx, col_idx, :], axis=0)
            elif metric == 'sum':
                pixel_keogram = np.sum(images[row_idx, col_idx, :], axis=0)
            keo_arr[i, :] = pixel_keogram
        elif n_channels == 3:
            # Update the preview image
            preview_img[row_idx, col_idx, :] = np.iinfo(preview_img.dtype).max

            # Extract metric from all images and add to keogram
            if metric == 'median':
                r_pixel_keogram = np.floor(np.median(images[row_idx, col_idx, 0, :], axis=0))
                g_pixel_keogram = np.floor(np.median(images[row_idx, col_idx, 1, :], axis=0))
                b_pixel_keogram = np.floor(np.median(images[row_idx, col_idx, 2, :], axis=0))
            elif metric == 'mean':
                r_pixel_keogram = np.floor(np.mean(images[row_idx, col_idx, 0, :], axis=0))
                g_pixel_keogram = np.floor(np.mean(images[row_idx, col_idx, 1, :], axis=0))
                b_pixel_keogram = np.floor(np.mean(images[row_idx, col_idx, 2, :], axis=0))
            elif metric == 'sum':
                r_pixel_keogram = np.floor(np.sum(images[row_idx, col_idx, 0, :], axis=0))
                g_pixel_keogram = np.floor(np.sum(images[row_idx, col_idx, 1, :], axis=0))
                b_pixel_keogram = np.floor(np.sum(images[row_idx, col_idx, 2, :], axis=0))

            keo_arr[i, :, 0] = r_pixel_keogram
            keo_arr[i, :, 1] = g_pixel_keogram
            keo_arr[i, :, 2] = b_pixel_keogram

        path_counter += 1

    if path_counter == 0:
        raise ValueError("Could not form keogram path. First ensure that coordinates are within image range. Then " +
                         "try increasing 'width' or decreasing number of points in input coordinates.")

    # Create keogram object
    keo_obj = Keogram(data=keo_arr, timestamp=timestamp, instrument_type='asi')

    if preview:
        plt.figure()
        plt.imshow(preview_img, cmap='gray', origin='lower')
        plt.axis("off")
        plt.title("Keogram Domain Preview")
        plt.show()

    return keo_obj
