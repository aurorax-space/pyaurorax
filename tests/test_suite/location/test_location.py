import aurorax
import pytest


def test_create_location_object():
    loc = aurorax.Location(lat=51, lon=-110)

    assert loc.lat == 51.0 and loc.lon == -110.0


def test_create_empty_location_object():
    loc = aurorax.Location(lat=None, lon=None)

    assert loc.lat is None and loc.lon is None


def test_create_invalid_location_object():
    with pytest.raises(ValueError):
        aurorax.Location(lat=51, lon=None)
