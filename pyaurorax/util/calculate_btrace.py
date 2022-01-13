"""
Helper functions for calculating the north and south B-trace geographic
locations for ground-based instruments.
"""

import datetime
import warnings
from typing import Dict
from ..location import Location

# import aacgmv2 if installed
try:
    import aacgmv2
    __aacgm_found = True
except ModuleNotFoundError:
    __aacgm_found = False

# pdoc init
__pdoc__: Dict = {}


def __calculate_btrace(geo_location: Location, dt: datetime.datetime) -> Location:
    # convert to magnetic coordinates
    mag_location = aacgmv2.convert_latlon(geo_location.lat,
                                          geo_location.lon,
                                          0.0,
                                          dt,
                                          method_code="G2A")

    # change magnetic latitude to other hemisphere
    mag_location = (mag_location[0] * -1.0,
                    mag_location[1],
                    mag_location[2])

    # convert magnetic coordinates back to geographic
    btrace_aacgm = aacgmv2.convert_latlon(mag_location[0],
                                          mag_location[1],
                                          mag_location[2],
                                          dt,
                                          method_code="A2G")

    # return as Location object
    return Location(lat=btrace_aacgm[0], lon=btrace_aacgm[1])


def ground_geo_to_nbtrace(geo_location: Location,
                          timestamp: datetime.datetime) -> Location:
    """
    Convert geographic location to North B-Trace geographic
    location

    The timestamp is required because when calculating the B-trace
    values, the location is converted into geomagnetic coordinates.
    This conversion is different based on the timestamp since the
    magnetic coordinates change over time.

    Note: aacgmv2 must be installed. To install it, you can run
    "python -m pip install pyaurorax[aacgmv2]".

    Args:
        geo_location: a Location object representing the
            geographic location
        dt: timestamp for this set of lat and lons

    Returns:
        the north B-trace location as a Location object
    """
    # check to make sure aacgmv2 is installed
    if (__aacgm_found is False):
        warnings.warn("The aacgmv2 package is not installed, so an unchanged "
                      "location object will be returned. For this function to "
                      "work, please install it using 'pip install pyaurorax[aacgmv2]'.")
        return geo_location

    # check if location is in northern hemisphere
    if (geo_location.lat is not None and geo_location.lat >= 0.0):
        # northern hemisphere, north b-trace is the same as geographic location
        return geo_location

    # calculate South B-trace and return
    sbtrace = __calculate_btrace(geo_location, timestamp)
    return sbtrace


def ground_geo_to_sbtrace(geo_location: Location,
                          timestamp: datetime.datetime) -> Location:
    """
    Convert geographic location to South B-Trace geographic
    location

    The timestamp is required because when calculating the B-trace
    values, the location is converted into geomagnetic coordinates.
    This conversion is different based on the timestamp since the
    magnetic coordinates change over time.

    Note: aacgmv2 must be installed. To install it, you can run
    "python -m pip install pyaurorax[aacgmv2]".

    Args:
        geo_location: a Location object representing the
            geographic location
        dt: timestamp for this set of lat and lons

    Returns:
        the south B-trace location as a Location object
    """
    # check to make sure aacgmv2 is installed
    if (__aacgm_found is False):
        warnings.warn("The aacgmv2 package is not installed, so an unchanged "
                      "location object will be returned. For this function to "
                      "work, please install it using 'pip install pyaurorax[aacgmv2]'.")
        return geo_location

    # check if location is in southern hemisphere
    if (geo_location.lat is not None and geo_location.lat < 0.0):
        # southern hemisphere, south b-trace is the same as geographic location
        return geo_location

    # calculate North B-trace and return
    nbtrace = __calculate_btrace(geo_location, timestamp)
    return nbtrace
