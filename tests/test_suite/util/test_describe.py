import pytest
import pyaurorax
import datetime


@pytest.mark.util
def test_describe_conjunction_search():
    # set params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 23, 59, 59)
    ground_params = [
        {"programs": ["themis-asi"]},
    ]
    space_params = [
        {"programs": ["swarm", "themis"]},
    ]
    distance = 500
    expected_response_str = "Find conjunctions of type (nbtrace) with epoch precision " \
        "of 60 seconds between data sources of ground1=(program in (themis-asi)) AND " \
        "space1=(program in (swarm, themis)) WHERE epochs are between 2020-01-01T00:00:00 " \
        "AND 2020-01-01T23:59:59 UTC HAVING max distances between location points of " \
        "ground1-space1=500 km."

    # create search object
    s = pyaurorax.conjunctions.Search(start,
                                      end,
                                      distance,
                                      ground=ground_params,
                                      space=space_params)

    # get describe string
    describe_str = pyaurorax.util.describe_conjunction_search(s)

    # test response
    if (describe_str is not None and describe_str == expected_response_str):
        assert True
    else:
        assert False


@pytest.mark.util
def test_describe_data_products_search():
    # set params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 2, 23, 59, 59)
    programs = ["auroramax"]
    data_product_types = [pyaurorax.DATA_PRODUCT_TYPE_KEOGRAM]
    expected_response_str = "Find data_products for ((program in (auroramax) filtered by " \
        "metadata ()) AND  data_product_metadata_filters []) AND data_product start >= " \
        "2020-01-01T00:00 UTC AND data_product end <= 2020-01-02T23:59:59 UTC AND " \
        "data_product_type in (keogram)"

    # create search object
    s = pyaurorax.data_products.Search(start,
                                       end,
                                       programs=programs,
                                       data_product_types=data_product_types)

    # get describe string
    describe_str = pyaurorax.util.describe_data_products_search(s)

    # test response
    if (describe_str is not None and describe_str == expected_response_str):
        assert True
    else:
        assert False


@pytest.mark.util
def test_describe_ephemeris_search():
    # set params
    start = datetime.datetime(2019, 1, 1, 0, 0, 0)
    end = datetime.datetime(2019, 1, 1, 0, 59, 59)
    programs = ["swarm"]
    platforms = ["swarma"]
    instrument_types = ["footprint"]
    expected_response_str = "Find ephemeris for ((program in (swarm) AND platform in (swarma) " \
        "AND instrument_type in (footprint) filtered by metadata ()) AND  ephemeris_metadata_filters " \
        "[])  AND epoch between 2019-01-01T00:00 and 2019-01-01T00:59:59 UTC"

    # create search object
    s = pyaurorax.ephemeris.Search(start,
                                   end,
                                   programs=programs,
                                   platforms=platforms,
                                   instrument_types=instrument_types)

    # get describe string
    describe_str = pyaurorax.util.describe_ephemeris_search(s)
    print(describe_str)

    # test response
    if (describe_str is not None and describe_str == expected_response_str):
        assert True
    else:
        assert False
