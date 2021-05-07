import aurorax
import datetime
from numpy import floor


def test_convert_nbtrace_northern():
    # set timestamp
    timestamp = datetime.datetime(2020, 1, 1, 0, 0, 0)

    lat = 56
    lon = 20

    # set geographic lat/lon
    geo_location = aurorax.Location(lat=lat, lon=lon)
    nbtrace = aurorax.util.ground_geo_to_nbtrace(geo_location, timestamp)

    assert floor(nbtrace.lat) == lat and floor(nbtrace.lon) == lon


def test_convert_nbtrace_southern():
    # set timestamp
    timestamp = datetime.datetime(2020, 1, 1, 0, 0, 0)

    lat = 56
    lon = 20

    # set geographic lat/lon
    geo_location = aurorax.Location(lat=-lat, lon=lon)
    nbtrace = aurorax.util.ground_geo_to_nbtrace(geo_location, timestamp)

    assert floor(nbtrace.lat) == 58 and floor(nbtrace.lon) == -9


def test_convert_sbtrace_northern():
    # set timestamp
    timestamp = datetime.datetime(2020, 1, 1, 0, 0, 0)

    lat = -56
    lon = 20

    # set geographic lat/lon
    geo_location = aurorax.Location(lat=lat, lon=lon)
    sbtrace = aurorax.util.ground_geo_to_sbtrace(geo_location, timestamp)

    assert floor(sbtrace.lat) == lat and floor(sbtrace.lon) == lon


def test_convert_sbtrace_southern():
    # set timestamp
    timestamp = datetime.datetime(2020, 1, 1, 0, 0, 0)

    lat = -56
    lon = 20

    # set geographic lat/lon
    geo_location = aurorax.Location(lat=-lat, lon=lon)
    sbtrace = aurorax.util.ground_geo_to_sbtrace(geo_location, timestamp)

    assert floor(sbtrace.lat) == -48 and floor(sbtrace.lon) == 39
