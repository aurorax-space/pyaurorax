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


def geo(skymap, altitude_km, contour_lats, contour_lons, constant_lat, constant_lon, n_points, remove_edge_cases):
    # Check that multiple contours are not defined based on arguments passed
    if (contour_lats is None) != (contour_lons is None):
        raise ValueError("When defining a custom contour, both 'contour_lats' and 'contour_lons' must be supplied.")
    if sum([((contour_lats is not None) and (contour_lons is not None)), (constant_lat is not None), (constant_lon is not None)]) > 1:
        raise ValueError("Only one contour can be defined per call: Pass only one of " +
                         "'contour_lats & contour_lons', 'constant_lat', or 'constant_lon'.")
    if sum([((contour_lats is not None) and (contour_lons is not None)), (constant_lat is not None), (constant_lon is not None)]) == 0:
        raise ValueError("No contour defined in input: Pass one of 'contour_lats & contour_lons', 'constant_lat', or 'constant_lon'.")

    # Obtain lat/lon arrays from skymap at desired altitude
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

    # First handle case of a contour of constant latitude:
    if (constant_lat is not None):
        # First check that the supplied latitude is valid for this skymap
        if (constant_lat < np.nanmin(lats)) or (constant_lat > np.nanmax(lats)):  # pragma: nocover
            raise ValueError(f"Latitude {constant_lat} does not coincide with input skymap: latitude range " +
                             f"at {altitude_km} km is {np.nanmin(lats), np.nanmax(lats)}.")

        # Get the longitude bounds of the skymap
        min_skymap_lon, max_skymap_lon = np.nanmin(lons), np.nanmax(lons)

        # Determine the step in longitudes for grabbing target lat, based on n_points
        if (n_points is None):
            n_points = round((lats.shape[0] - 1) / 5.12)

        # Iterate though longitude ranges
        iteration_lons = np.linspace(min_skymap_lon, max_skymap_lon, n_points)
        x_list = []
        y_list = []
        for i in range(len(iteration_lons) - 1):
            # Get lon domain for current iteration through skymap
            lon_min = iteration_lons[i]
            lon_max = iteration_lons[i + 1]

            # Get indices of this longitude slice
            lon_slice_idx = np.logical_and(lons >= lon_min, lons < lon_max)

            # Get index of pixel nearest to target elevation
            masked_lats = np.where(lon_slice_idx, lats, np.nan)
            diffs = np.abs(masked_lats - constant_lat)
            y, x = np.where(diffs == np.nanmin(diffs))

            if x.shape == (0, ) or y.shape == (0, ):  # pragma: nocover
                continue

            # Add to master lists
            x_list.append(x[0])
            y_list.append(y[0])

        if (remove_edge_cases is True):
            # Remove any points lying on the edge of CCD bounds and return
            x_list = np.array(x_list)
            y_list = np.array(y_list)
            edge_case_idx = np.where(np.logical_and.reduce([x_list > 0, x_list < lats.shape[1] - 1, y_list > 0, y_list < lats.shape[0] - 1]))
            x_list = x_list[edge_case_idx]
            y_list = y_list[edge_case_idx]
            return (x_list, y_list)
        else:
            # Convert to arrays, return
            return (np.array(x_list), np.array(y_list))

    # Next handle case of a contour of constant longitude:
    elif (constant_lon is not None):
        # First check that the supplied longitude is valid for this skymap
        if (constant_lon < np.nanmin(lons)) or (constant_lon > np.nanmax(lons)):  # pragma: nocover
            raise ValueError(f"Longitude {constant_lat} does not coincide with input skymap: longitude range " +
                             f"at {altitude_km} km is {np.nanmin(lons), np.nanmax(lons)}.")

        # Get the latitude bounds of the skymap
        min_skymap_lat, max_skymap_lat = np.nanmin(lats), np.nanmax(lats)

        # Determine the step in longitudes for grabbing target lat, based on n_points
        if (n_points is None):
            n_points = round((lats.shape[0] - 1) / 5.12)

        # Iterate though latitude ranges
        iteration_lats = np.linspace(min_skymap_lat, max_skymap_lat, n_points)
        x_list = []
        y_list = []
        for i in range(len(iteration_lats) - 1):
            # Get lon domain for current iteration through skymap
            lat_min = iteration_lats[i]
            lat_max = iteration_lats[i + 1]

            # Get indices of this longitude slice
            lat_slice_idx = np.logical_and(lats >= lat_min, lats < lat_max)

            # Get index of pixel nearest to target elevation
            masked_lons = np.where(lat_slice_idx, lons, np.nan)
            diffs = np.abs(masked_lons - constant_lon)
            y, x = np.where(diffs == np.nanmin(diffs))

            if x.shape == (0, ) or y.shape == (0, ):  # pragma: nocover
                continue

            # Add to master lists
            x_list.append(x[0])
            y_list.append(y[0])

        if (remove_edge_cases is True):
            # Remove any points lying on the edge of CCD bounds and return
            x_list = np.array(x_list)
            y_list = np.array(y_list)
            edge_case_idx = np.where(np.logical_and.reduce([x_list > 0, x_list < lats.shape[1] - 1, y_list > 0, y_list < lats.shape[0] - 1]))
            x_list = x_list[edge_case_idx]
            y_list = y_list[edge_case_idx]
            return (x_list, y_list)
        else:
            # Convert to arrays, return
            return (np.array(x_list), np.array(y_list))

    # Finally, handle case of a custom contour
    elif (contour_lats is not None) and (contour_lons is not None):
        # Convert lists to ndarrays if necessary
        if (isinstance(contour_lats, list)):
            contour_lats = np.asarray(contour_lats)
        if (isinstance(contour_lons, list)):
            contour_lons = np.asarray(contour_lons)

        # Remove any invalid lat/lon pairs
        invalid_mask = (contour_lons < np.nanmin(lons)) | (contour_lons > np.nanmax(lons)) | (contour_lats < np.nanmin(lats)) | (contour_lats
                                                                                                                                 > np.nanmax(lats))

        # Filter out invalid contour points
        valid_contour_lats = contour_lats[~invalid_mask]
        valid_contour_lons = contour_lons[~invalid_mask]

        # Get the latitude bounds of the skymap
        # Iterate through each target point
        x_list = []
        y_list = []
        for target_lat, target_lon in zip(valid_contour_lats, valid_contour_lons):
            # Make sure lat/lon falls within skymap
            if target_lat < np.nanmin(lats) or target_lat > np.nanmax(lats):  # pragma: nocover
                raise ValueError(f"Latitude {target_lat} is outside this skymap's valid range of {(np.nanmin(lats),np.nanmax(lats))}.")
            if target_lon < np.nanmin(lons) or target_lon > np.nanmax(lons):  # pragma: nocover
                raise ValueError(f"Longitude {target_lon} is outside this skymap's valid range of {(np.nanmin(lons),np.nanmax(lons))}.")

            # Compute haversine distance between all points in skymap
            haversine_diff = __haversine_distances(target_lat, target_lon, lats, lons)

            # Obtain the skymap indices of the nearest point
            nan_mask = np.isnan(haversine_diff)
            masked_data = np.ma.masked_array(haversine_diff, mask=nan_mask)
            nearest_indices = np.unravel_index(np.ma.argmin(masked_data), haversine_diff.shape)

            # Convert indices to CCD Coordinates
            y_loc = nearest_indices[0] - 1
            if y_loc < 0:  # pragma: nocover
                y_loc = 0
            x_loc = nearest_indices[1] - 1
            if x_loc < 0:  # pragma: nocover
                x_loc = 0

            x_list.append(x_loc)
            y_list.append(y_loc)

        if (remove_edge_cases is True):
            # Remove any points lying on the edge of CCD bounds and return
            x_list = np.array(x_list)
            y_list = np.array(y_list)
            edge_case_idx = np.where(np.logical_and.reduce([x_list > 0, x_list < lats.shape[1] - 1, y_list > 0, y_list < lats.shape[0] - 1]))
            x_list = x_list[edge_case_idx]
            y_list = y_list[edge_case_idx]
            return (x_list, y_list)
        else:
            # Convert to arrays, return
            return (np.array(x_list), np.array(y_list))

    else:  # pragma: nocover
        # This shouldn't occur, but typing claims there is a missed case somewhere that could not be identified...
        raise ValueError("Something unexpected happened, please verify your inputs are in expected format. Otherwise, contact the PyAuroraX team.")
