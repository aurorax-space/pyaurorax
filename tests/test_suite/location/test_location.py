import pytest
import pyaurorax


@pytest.mark.location
def test_create_location_object():
    loc = pyaurorax.Location(lat=51, lon=-110)
    assert loc.lat == 51.0 and loc.lon == -110.0


@pytest.mark.location
def test_create_empty_location_object():
    loc = pyaurorax.Location(lat=None, lon=None)
    assert loc.lat is None and loc.lon is None


@pytest.mark.location
def test_create_invalid_location_object():
    with pytest.raises(ValueError):
        pyaurorax.Location(lat=51, lon=None)
