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
import pyproj

# SSCWeb traces field lines on a spherical Earth of this radius and stops at 100 km
EARTH_RADIUS_KM = 6371.2

# Create transformer object:
#   WGS84 Earth-centred Earth-fixed Cartesian (4978) to WGS84 geodetic lat/lon/height (4979)
_transformer = pyproj.Transformer.from_crs("EPSG:4978", "EPSG:4979", always_xy=True)


def geocentric_to_geodetic(lats, lons, altitude_km):

    # to float arrays; None and NaN pass through as NaN
    lats = np.asarray(lats, dtype=float)
    lons = np.asarray(lons, dtype=float)
    if (lats.shape != lons.shape):
        raise ValueError("lats and lons must have the same shape")

    # spherical geocentric to Cartesian, in metres
    r_m = (EARTH_RADIUS_KM + altitude_km) * 1000.0
    lat_rad = np.radians(lats)
    lon_rad = np.radians(lons)
    x = r_m * np.cos(lat_rad) * np.cos(lon_rad)
    y = r_m * np.cos(lat_rad) * np.sin(lon_rad)
    z = r_m * np.sin(lat_rad)

    # Cartesian to geodetic; the height is discarded
    geodetic_lons, geodetic_lats, _ = _transformer.transform(x, y, z)
    return np.asarray(geodetic_lats), np.asarray(geodetic_lons)
