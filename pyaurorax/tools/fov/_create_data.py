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

import math
import numpy as np
import datetime
import aacgmv2
from pyproj import Geod
from ..classes.fov import FOVData
from ..._util import show_warning


# Helper function that computes the fov for an imager (ASI or spectrograph)
# at a given location, assuming some altitude and masking below min_elevation
def __compute_fov_contour(lat, lon, height_km, min_elevation, spectrograph=False):

    # Ellipsoid Parameters for WGS 1984 model of Earth
    a = 6378137.0
    f1 = 298.257223563

    f = 1.0 / f1
    e2 = f * (2.0 - f)
    e_minus = (1.0 - f)**2
    deg2rad = math.pi / 180.0
    rad2deg = 180.0 / math.pi

    # Convert from geodetic coordinates
    h = 0.0
    phi = lat * deg2rad
    n_phi = a / math.sqrt(1.0 - e2 * math.sin(phi)**2)

    # To Cartesian coordinates
    lam = lon * deg2rad
    c_phi = math.cos(phi)
    s_phi = math.sin(phi)
    x = (n_phi + h) * c_phi * math.cos(lam)
    y = (n_phi + h) * c_phi * math.sin(lam)
    z = (e_minus * n_phi + h) * s_phi

    result = np.array([x, y, z])

    s_lam = math.sin(lam)
    c_lam = math.cos(lam)
    east = np.array([-s_lam, c_lam, 0.0])
    down = np.array([-c_phi * c_lam, -c_phi * s_lam, -s_phi])
    north = np.array([-c_lam * s_phi, -s_lam * s_phi, c_phi])

    el = min_elevation * deg2rad

    # Non-Spherical Earth
    re = 6371.2
    rho0 = height_km * (2 * re + height_km) / (2 * re * math.sin(min_elevation * deg2rad))
    rho = height_km * (2 * re + height_km) / (2 * re * math.sin(min_elevation * deg2rad) + rho0)

    # Create empty array for lat/lon at every 1deg along 360deg azimuth range
    azimuth_angle = np.linspace(0, 360, num=361)
    fov_latlon = np.zeros((2, len(azimuth_angle)))

    # Iterate through every desired point
    for idx in range(0, len(azimuth_angle)):

        # Adjust aim for this point along FoV
        az = azimuth_angle[idx] * deg2rad
        aim = north * math.cos(az) * math.cos(el) + east * math.sin(az) * math.cos(el) - down * math.sin(el)

        # Map from Cartesian back to geodetic for this iteration's point
        point_cartesian = result + aim * rho * (1.0 * 10**3)
        x = point_cartesian[0]
        y = point_cartesian[1]
        z = point_cartesian[2]

        lam = math.atan2(y, x)
        r = math.sqrt(x**2 + y**2)

        phi = 0.0
        n_phi = 0.0

        for _ in range(0, 5):
            phi = math.atan((z + n_phi * e2 * math.sin(phi)) / r)
            n_phi = a / math.sqrt(1.0 - e2 * (math.sin(phi))**2)

        h = r / math.cos(phi) - n_phi

        point_lat = phi * rad2deg
        point_lon = lam * rad2deg

        fov_latlon[0, idx] = point_lat
        fov_latlon[1, idx] = point_lon

    # If this was done for an ASI, we are done
    if spectrograph:

        # set up WGS84 ellipsoid from pyproj
        geod = Geod(ellps="WGS84")

        # Otherwise, we need to find the bisecting line through the FoV that is aligned
        # with magnetic North
        mag_lat, _, _ = aacgmv2.convert_latlon_arr(fov_latlon[0, :],
                                                   fov_latlon[1, :],
                                                   fov_latlon[1, :] * 0.0,
                                                   datetime.datetime.today(),
                                                   method_code="A2G")

        # Point of FoV contour aligned with magnetic North
        mag_north_bin = np.argmax(np.flip(mag_lat))

        # Point opposite to magnetic North point on FoV contour
        mag_south_bin = np.argmin(np.flip(mag_lat))

        # Number of points in spect FOV determined dynamically based on elevation threshold
        n_points = 180 - 2 * (int(min_elevation) - 1)

        # Geodetic lat lon of points of magnetic North and South on FoV contour will be
        # the start and end points of the spectrograph FoV contour
        lat_max = fov_latlon[0, mag_north_bin]
        lon_max = fov_latlon[1, mag_north_bin]
        lat_min = fov_latlon[0, mag_south_bin]
        lon_min = fov_latlon[1, mag_south_bin]

        interior_points = geod.npts(lon_min, lat_min, lon_max, lat_max, n_points)
        lons = [lon_min] + [pt[0] for pt in interior_points] + [lon_max]
        lats = [lat_min] + [pt[1] for pt in interior_points] + [lat_max]

        # Re-initialize fov_coordinate array and fill
        fov_latlon = np.zeros((2, n_points + 2))
        fov_latlon[0, :] = lats
        fov_latlon[1, :] = lons

    return fov_latlon


def create_data(aurorax_obj, sites, instrument_array, height_km, min_elevation, color, linewidth, linestyle):

    # First, check that we have enough information to create the FoVs with the given inputs
    if not isinstance(sites, list):
        sites = [sites]

    site_dict = {}

    # First, if no sites are provided, we just get all sites for the provided 'instrument_array'
    if sites[0] is None:

        # Get all site records for this instrument
        result = aurorax_obj.data.ucalgary.list_observatories(instrument_array)

        for r in result:
            site_dict[r.uid] = (r.geodetic_latitude, r.geodetic_longitude)

    # Otherwise, iterate through each site provided
    else:
        for site in sites:

            # If site is a string giving site_uid then we use the API to get lat/lon
            if isinstance(site, str):

                # If we're given site_uid codes we need to know the instrument_array
                if instrument_array is None:
                    raise ValueError(
                        "If specifying sites by site_uid string, instrument_array must also be supplied (e.g., instrument_array='themis_asi').")

                # Get the site location of this site_uid for the chosen instrument_array, from the API
                result = aurorax_obj.data.ucalgary.list_observatories(instrument_array, uid=site)

                # Check if a site record was actually returned
                if len(result) == 0:
                    raise ValueError(f"Could not find requested site_uid '{site}' for instrument_array '{instrument_array}'.")
                else:
                    site_record = result[0]

                # Add this record to the dictionary
                site_dict[site_record.uid] = (site_record.geodetic_latitude, site_record.geodetic_longitude)

            elif isinstance(site, tuple):

                # If the site is passed as a Tuple, it should be in format ("site_uid", lat, lon)
                if (len(site) != 3) or (not isinstance(site[0], str)) or (not isinstance(site[1], float)) or (not isinstance(site[2], float)):
                    raise ValueError(f"Improper site format for input {site}. Specifying a site by a tuple requires format ('site_uid', lat, lon).")

                # Extract pieces of manual site specification
                custom_uid = site[0]
                custom_lat = site[1]
                custom_lon = site[2]

                # Check that lats and lons are in valid range
                if (custom_lat > 90.0) or (custom_lat < -90.0):
                    raise ValueError(f"Latitude {custom_lat} for site {site} is outside of the valid range [-90, 90].")

                if (custom_lon > 180.0) or (custom_lon < -180.0):
                    raise ValueError(f"Longitude {custom_lon} for site {site} is outside of the valid range [-180, 180].")

                # If everything is valid, add this record to the dictionary
                site_dict[custom_uid] = (custom_lat, custom_lon)

    # Next, ensure height_km is valid if supplied and decide on what to use if not supplied.
    if height_km is None:

        # If no instrument is selected, assume 110 km
        if instrument_array is None:
            height_km = 110.0
            show_warning("Defaulting to height_km = 110.0. Specify 'instrument_array' or 'height_km' parameters" +
                         " to map FOVs at a different altitude.",
                         stacklevel=1)

        # Nominal height for REGO is 230 km and for all other instruments is 110 km
        else:
            if instrument_array == "rego":
                height_km = 230.0
            else:
                height_km = 110.0

    # Check that height_km is reasonable
    if (height_km < 10.0) or (height_km > 1000.0):
        raise ValueError(f"Received 'height_km' of {height_km}, outside the valid range [10.0, 1000.0].")

    # Check that min_elevation is valid
    if (min_elevation < 0.0) or (min_elevation > 90.0):
        raise ValueError(f"Received 'min_elevation' of {min_elevation}, outside the valid range [0.0, 90.0].")

    # Create site_uid list and dictionaries to hold fov coords and shapes, to put in the FOVData object
    site_uid_list = []
    fovs = {}
    fovs_dimensions = {}

    # Now, site dict contains all of the site_uids and corresponding (lat, lon) pairs we want to get data
    # for, along with the altitude and minimum elevation to map FoVs at. Now, we iterate through each site
    for site_uid, site_latlon in site_dict.items():

        # Call helper function to map the actual FoV
        if instrument_array == "trex_spectrograph":
            fov_latlon = __compute_fov_contour(site_latlon[0], site_latlon[1], height_km, min_elevation, spectrograph=True)
        else:
            fov_latlon = __compute_fov_contour(site_latlon[0], site_latlon[1], height_km, min_elevation)

        site_uid_list.append(site_uid)
        fovs[site_uid] = fov_latlon
        fovs_dimensions[site_uid] = fov_latlon.shape

    # Create and return the FOVData object
    return FOVData(site_uid_list=site_uid_list,
                   fovs=fovs,
                   fovs_dimensions=fovs_dimensions,
                   instrument_array=instrument_array,
                   color=color,
                   linewidth=linewidth,
                   linestyle=linestyle,
                   data_availability=None,
                   aurorax_obj=aurorax_obj)
