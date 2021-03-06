import datetime
from aurorax import Location
import aacgmv2


def __calculate_btrace(geo_location, dt):
    # convert to magnetic coordinates
    mag_location = aacgmv2.convert_latlon(geo_location.lat,
                                          geo_location.lon,
                                          0.0,
                                          dt,
                                          method_code="G2A")

    # change magnetic latitude to other hemisphere
    mag_location = (
        mag_location[0] * -1.0,
        mag_location[1],
        mag_location[2]
    )

    # convert magnetic coordinates back to geographic
    btrace_aacgm = aacgmv2.convert_latlon(mag_location[0],
                                          mag_location[1],
                                          mag_location[2],
                                          dt,
                                          method_code="A2G")

    # return as Location object
    return Location(lat=btrace_aacgm[0], lon=btrace_aacgm[1])


def ground_geo_to_nbtrace(geo_location: Location, timestamp: datetime.datetime) -> Location:
    """
    Convert geographic location to North B-Trace geographic location

    :param geo_location: geographic location
    :type geo_location: Location
    :param dt: timestamp
    :type dt: datetime.datetime

    :return: north B-trace location
    :rtype: Location
    """
    # check if location is in northern hemisphere
    if (geo_location.lat >= 0):
        # northern hemisphere, north b-trace is the same as geographic location
        return geo_location

    # calculate South B-trace and return
    sbtrace = __calculate_btrace(geo_location, timestamp)
    return sbtrace


def ground_geo_to_sbtrace(geo_location: Location, timestamp: datetime.datetime) -> Location:
    """
    Convert geographic location to South B-Trace geographic location

    :param geo_location: geographic location
    :type geo_location: Location
    :param dt: timestamp
    :type dt: datetime.datetime

    :return: south B-trace location
    :rtype: Location
    """
    # check if location is in southern hemisphere
    if (geo_location.lat < 0):
        # southern hemisphere, south b-trace is the same as geographic location
        return geo_location

    # calculate North B-trace and return
    nbtrace = __calculate_btrace(geo_location, timestamp)
    return nbtrace
