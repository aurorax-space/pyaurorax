import pytest
import pyaurorax
import datetime


@pytest.mark.availability
def test_ephemeris_availability():
    # set params
    start_date = datetime.datetime(2019, 1, 1)
    end_date = datetime.date(2019, 1, 2)
    program = "swarm"
    platform = "swarma"
    instrument_type = "footprint"

    # get availability
    availability = pyaurorax.availability.ephemeris(start_date,
                                                    end_date,
                                                    program=program,
                                                    platform=platform,
                                                    instrument_type=instrument_type,
                                                    slow=False)

    # check
    assert type(availability) is list \
        and len(availability) > 0 \
        and type(availability[0]) is pyaurorax.availability.AvailabilityResult \
        and availability[0].data_source.program == "swarm"


@pytest.mark.availability
def test_data_product_availability():
    # set params
    start_date = datetime.datetime(2019, 1, 1)
    end_date = datetime.date(2019, 1, 2)
    program = "trex"
    instrument_type = "RGB ASI"

    # get availability
    availability = pyaurorax.availability.data_products(start_date,
                                                        end_date,
                                                        program=program,
                                                        instrument_type=instrument_type,
                                                        slow=True)

    # check
    assert type(availability) is list \
        and len(availability) > 0 \
        and type(availability[0]) is pyaurorax.availability.AvailabilityResult \
        and availability[0].data_source.program == "trex"
