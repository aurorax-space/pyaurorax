import pytest
import pyaurorax
import datetime
import numpy as np


@pytest.mark.util
def test_convert_nbtrace_northern():
    # set timestamp
    timestamp = datetime.datetime(2020, 1, 1, 0, 0, 0)

    lat = 56
    lon = 20

    # set geographic lat/lon
    geo_location = pyaurorax.Location(lat=lat, lon=lon)
    nbtrace = pyaurorax.util.ground_geo_to_nbtrace(geo_location, timestamp)

    assert np.floor(nbtrace.lat) == lat and np.floor(nbtrace.lon) == lon


@pytest.mark.util
def test_convert_nbtrace_southern():
    # set timestamp
    timestamp = datetime.datetime(2020, 1, 1, 0, 0, 0)

    lat = 56
    lon = 20

    # set geographic lat/lon
    geo_location = pyaurorax.Location(lat=-lat, lon=lon)
    nbtrace = pyaurorax.util.ground_geo_to_nbtrace(geo_location, timestamp)

    assert np.floor(nbtrace.lat) == 58 and np.floor(nbtrace.lon) == -9


@pytest.mark.util
def test_convert_sbtrace_northern():
    # set timestamp
    timestamp = datetime.datetime(2020, 1, 1, 0, 0, 0)

    lat = -56
    lon = 20

    # set geographic lat/lon
    geo_location = pyaurorax.Location(lat=lat, lon=lon)
    sbtrace = pyaurorax.util.ground_geo_to_sbtrace(geo_location, timestamp)

    assert np.floor(sbtrace.lat) == lat and np.floor(sbtrace.lon) == lon


@pytest.mark.util
def test_convert_sbtrace_southern():
    # set timestamp
    timestamp = datetime.datetime(2020, 1, 1, 0, 0, 0)

    lat = -56
    lon = 20

    # set geographic lat/lon
    geo_location = pyaurorax.Location(lat=-lat, lon=lon)
    sbtrace = pyaurorax.util.ground_geo_to_sbtrace(geo_location, timestamp)

    assert np.floor(sbtrace.lat) == -48 and np.floor(sbtrace.lon) == 39
