import pytest
import datetime
import random
import string
import pyaurorax
from pyaurorax.conjunctions import Conjunction


@pytest.mark.conjunctions
def test_conjunctions_search_object():
    # set up params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 6, 59, 59)
    ground_params = [
        {"programs": ["themis-asi"]}
    ]
    space_params = [
        {"programs": ["swarm"]}
    ]
    events_params = [
        {"programs": ["events"]}
    ]
    distance = 200

    # create search object
    s = pyaurorax.conjunctions.Search(start,
                                      end,
                                      ground=ground_params,
                                      space=space_params,
                                      events=events_params,
                                      distance=distance)

    # check to make sure type is correct
    assert type(s) is pyaurorax.conjunctions.Search


@pytest.mark.conjunctions
def test_conjunctions_search_query_property():
    # set up params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 6, 59, 59)
    ground_params = [
        {"programs": ["themis-asi"]}
    ]
    space_params = [
        {"programs": ["swarm"]}
    ]
    events_params = [
        {"programs": ["events"]}
    ]
    distance = 200

    # create object
    s = pyaurorax.conjunctions.Search(start,
                                      end,
                                      ground=ground_params,
                                      space=space_params,
                                      events=events_params,
                                      distance=distance)

    # try to get the query parameter
    try:
        _ = s.query
        assert True
    except Exception:
        assert False


@pytest.mark.conjunctions
def test_conjunctions_search_object_with_advanced_distances():
    # set up params
    start = datetime.datetime(2019, 2, 5, 0, 0, 0)
    end = datetime.datetime(2019, 2, 5, 23, 59, 59)
    ground_params = [
        {"programs": ["themis-asi"]}
    ]
    space_params = [
        {"programs": ["swarm"]},
        {"programs": ["themis"]}
    ]
    advanced_distances = {
        "ground1-space1": 200,
        "space1-space2": 500
    }

    # create object
    s = pyaurorax.conjunctions.Search(start,
                                      end,
                                      advanced_distances,
                                      ground=ground_params,
                                      space=space_params)

    # try to get the query param
    try:
        _ = s.query
        assert True
    except Exception:
        assert False


@pytest.mark.conjunctions
@pytest.mark.parametrize("num_ground_blocks,num_space_blocks,num_events_blocks,should_pass",
                         [
                             (5, 5, 0, True),
                             (5, 6, 0, False),
                             (6, 5, 0, False),
                             (5, 4, 1, True),
                             (5, 5, 1, False),
                             (5, 4, 2, False),
                             (0, 5, 5, True),
                             (5, 0, 5, True),
                             (0, 5, 6, False),
                             (11, 0, 0, False),
                             (0, 11, 0, False),
                             (0, 0, 11, False),
                             (10, 0, 0, True),
                             (0, 10, 0, True),
                             (0, 0, 10, True)
                         ])
def test_conjunctions_too_many_criteria_blocks(num_ground_blocks,
                                               num_space_blocks,
                                               num_events_blocks,
                                               should_pass):
    # set basic search params
    start = datetime.datetime(2019, 1, 1, 0, 0, 0)
    end = datetime.datetime(2019, 1, 31, 23, 59, 59)
    distance = 300

    # set ground
    ground = []
    for _ in range(0, num_ground_blocks):
        random_str = ''.join(random.sample(string.ascii_lowercase, 10))
        ground.append({"programs": [random_str]})

    # set space
    space = []
    for _ in range(0, num_space_blocks):
        random_str = ''.join(random.sample(string.ascii_lowercase, 10))
        space.append({"programs": [random_str]})

    # set events
    events = []
    for _ in range(0, num_events_blocks):
        random_str = ''.join(random.sample(string.ascii_lowercase, 10))
        events.append({"programs": [random_str]})

    # create search object
    s = pyaurorax.conjunctions.Search(start,
                                      end,
                                      distance,
                                      ground=ground,
                                      space=space,
                                      events=events)

    # check the criteria block count
    try:
        s.check_criteria_block_count_validity()
        exception_raised = False
    except pyaurorax.exceptions.AuroraXBadParametersException:
        exception_raised = True

    # check if the test should pass or fail
    if (should_pass is True):
        if (exception_raised is True):
            assert False
        else:
            assert True
    else:
        if (exception_raised is True):
            assert True
        else:
            assert False


@pytest.mark.conjunctions
def test_conjunctions_search_synchronous():
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

    # do search
    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      distance,
                                      ground=ground_params,
                                      space=space_params,
                                      verbose=False)

    # check to make sure we got at least one result, and the
    # first result is a Conjunction object
    assert len(s.data) > 0 and type(s.data[0]) is Conjunction


@pytest.mark.conjunctions
def test_conjunctions_search_synchronous_with_response_format():
    # set up params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 23, 59, 59)
    ground_params = [
        {
            "programs": ["themis-asi"],
            "platforms": ["gillam"]
        }
    ]
    space_params = [
        {"programs": ["swarm", "themis"]},
    ]
    distance = 300
    response_format = {
        "conjunction_type": True,
        "start": True,
        "end": True,
        "min_distance": True,
        "closest_epoch": True,
        "data_sources": {
            "identifier": True
        }
    }

    # do synchronous search
    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      distance,
                                      ground=ground_params,
                                      space=space_params,
                                      verbose=False,
                                      response_format=response_format)

    # check to make sure there is at least one conjunction found, and
    # the "max_distance" key is not in the first conjunction (since
    # we didn't ask for it)
    assert len(s.data) > 0 and \
        type(s.data[0]) is dict and \
        "max_distance" not in s.data[0].keys()


@pytest.mark.conjunctions
def test_conjunctions_search_synchronous_events_and_space():
    # set up params
    start = datetime.datetime(2008, 3, 1, 0, 0, 0)
    end = datetime.datetime(2008, 3, 1, 23, 59, 59)
    space_params = [
        {"programs": ["swarm", "themis"]},
    ]
    events_params = [
        {
            "programs": ["events"],
            "platforms": ["toshi"],
            "instrument_types": ["substorm onsets"]
        }
    ]
    distance = 500

    # do synchronous search
    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      distance,
                                      space=space_params,
                                      events=events_params,
                                      verbose=False)

    # check to make sure we got at least one result, and the
    # first result is a Conjunction object
    assert len(s.data) > 0 and type(s.data[0]) is Conjunction


@pytest.mark.conjunctions
def test_conjunctions_search_asynchronous():
    # set up params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 6, 59, 59)
    ground_params = [
        {"programs": ["themis-asi"]}
    ]
    space_params = [
        {"programs": ["swarm"]}
    ]
    distance = 100

    # so asynchronous search
    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      distance,
                                      ground=ground_params,
                                      space=space_params,
                                      return_immediately=True)

    # wait for the request to finish, get the data once done
    s.wait()
    s.get_data()

    # check to make sure we got at least one result, and the
    # first result is a Conjunction object
    assert len(s.data) > 0 and type(s.data[0]) is Conjunction


@pytest.mark.conjunctions
def test_conjunctions_search_asynchronous_cancel():
    # set up params
    start = datetime.datetime(2019, 1, 1, 0, 0, 0)
    end = datetime.datetime(2019, 12, 31, 23, 59, 59)
    ground_params = [
        {"programs": ["themis-asi"]}
    ]
    space_params = [
        {"programs": ["swarm"]}
    ]
    conjunction_types = [pyaurorax.conjunctions.CONJUNCTION_TYPE_SBTRACE]
    distance = 100

    # do asynchronous search
    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      distance,
                                      ground=ground_params,
                                      space=space_params,
                                      conjunction_types=conjunction_types,
                                      return_immediately=True)

    # cancel request
    result = s.cancel(wait=True)

    # check to make sure it has been cancelled
    assert result == 1


@pytest.mark.conjunctions
def test_conjunctions_search_asynchronous_with_response_format():
    # set up params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 23, 59, 59)
    ground_params = [
        {
            "programs": ["themis-asi"],
            "platforms": ["gillam"]
        }
    ]
    space_params = [
        {"programs": ["swarm", "themis"]},
    ]
    distance = 300
    response_format = {
        "conjunction_type": True,
        "start": True,
        "end": True,
        "min_distance": True,
        "closest_epoch": True,
        "data_sources": {
            "identifier": True
        }
    }

    # do asynchronous search
    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      distance,
                                      ground=ground_params,
                                      space=space_params,
                                      verbose=False,
                                      response_format=response_format,
                                      return_immediately=True)

    # wait for the request to finish, get the data once done
    s.wait()
    s.get_data()

    # check to make sure there is at least one conjunction found, and
    # the "max_distance" key is not in the first conjunction (since
    # we didn't ask for it)
    assert len(s.data) > 0 and \
        type(s.data[0]) is dict and \
        "max_distance" not in s.data[0].keys()


@pytest.mark.conjunctions
def test_conjunctions_search_asynchronous_events_and_space():
    # set up params
    start = datetime.datetime(2008, 3, 1, 0, 0, 0)
    end = datetime.datetime(2008, 3, 1, 23, 59, 59)
    space_params = [
        {"programs": ["swarm", "themis"]},
    ]
    events_params = [
        {
            "programs": ["events"],
            "platforms": ["toshi"],
            "instrument_types": ["substorm onsets"]
        }
    ]
    distance = 500

    # do asynchronous search
    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      distance,
                                      space=space_params,
                                      events=events_params,
                                      verbose=False,
                                      return_immediately=True)

    # wait for the request to finish, get the data once done
    s.wait()
    s.get_data()

    # check to make sure we got at least one result, and the
    # first result is a Conjunction object
    assert len(s.data) > 0 and type(s.data[0]) is Conjunction


@pytest.mark.conjunctions
def test_conjunctions_search_asynchronous_with_metadata_filters():
    # set up params
    start = datetime.datetime(2019, 3, 27, 0, 0, 0)
    end = datetime.datetime(2019, 3, 27, 23, 59, 59)
    ground_params = [
        {
            "programs": ["themis-asi"],
            "ephemeris_metadata_filters": {
                "logical_operator": "AND",
                "expressions": [
                    {
                        "key": "ml_cloud_v1",
                        "operator": "=",
                        "values": [
                            "not classified as cloud"
                        ]
                    }
                ]
            }
        }
    ]
    space_params = [
        {
            "programs": ["swarm"],
            "ephemeris_metadata_filters": {
                "logical_operator": "AND",
                "expressions": [
                    {
                        "key": "nbtrace_region",
                        "operator": "=",
                        "values": [
                            "north polar cap"
                        ]
                    }
                ]
            }
        }
    ]
    distance = 300

    # do asynchronous search
    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      distance,
                                      ground=ground_params,
                                      space=space_params,
                                      return_immediately=True)

    # wait for the request to finish, get the data once done
    s.wait()
    s.get_data()

    # check to make sure we got at least one result, and the
    # first result is a Conjunction object
    assert len(s.data) > 0 and type(s.data[0]) is Conjunction


@pytest.mark.conjunctions
def test_conjunctions_search_asynchronous_space_only_with_hemispheres():
    # set up params
    start = datetime.datetime(2019, 2, 1, 0, 0, 0)
    end = datetime.datetime(2019, 2, 1, 23, 59, 59)
    space_params = [
        {
            "programs": ["swarm"],
            "hemisphere": ["southern"]
        },
        {
            "programs": ["themis"],
            "hemisphere": ["northern"]
        }
    ]
    distance = 300

    # do asynchronous search
    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      distance,
                                      space=space_params,
                                      return_immediately=True)

    # wait for the request to finish, get the data once done
    s.wait()
    s.get_data()

    # check to make sure we got at least one result, and the
    # first result is a Conjunction object
    assert len(s.data) > 0 and type(s.data[0]) is Conjunction


@pytest.mark.conjunctions
def test_conjunctions_search_asynchronous_with_advanced_distances():
    # set up params
    start = datetime.datetime(2019, 2, 5, 0, 0, 0)
    end = datetime.datetime(2019, 2, 5, 23, 59, 59)
    ground_params = [
        {"programs": ["themis-asi"]}
    ]
    space_params = [
        {"programs": ["swarm"]},
        {"programs": ["themis"]}
    ]
    advanced_distances = {
        "ground1-space1": 200,
        "space1-space2": 500
    }

    # do asynchronous search
    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      advanced_distances,
                                      ground=ground_params,
                                      space=space_params,
                                      return_immediately=True)

    # wait for the request to finish, get the data once done
    s.wait()
    s.get_data()

    # compare the distances
    query_distance_keys = s.query["max_distances"].keys()
    distances_set = ["ground1-space1", "ground1-space2", "space1-space2"]
    g1s1_distance_set = s.query["max_distances"]["ground1-space1"] == advanced_distances["ground1-space1"]
    s1s2_distance_set = s.query["max_distances"]["space1-space2"] == advanced_distances["space1-space2"]

    # do checks
    assert all(x in query_distance_keys for x in distances_set) and \
        g1s1_distance_set and s1s2_distance_set and len(s.data) > 0


@pytest.mark.conjunctions
def test_conjunctions_search_asynchronous_with_conjunction_types():
    # set up params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 23, 59, 59)
    ground_params = [
        {"programs": ["themis-asi"]}
    ]
    space_params = [
        {"programs": ["swarm"]}
    ]
    conjunction_type = [pyaurorax.conjunctions.CONJUNCTION_TYPE_SBTRACE]
    distance = 100

    # do asynchronous search
    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      distance,
                                      ground=ground_params,
                                      space=space_params,
                                      conjunction_types=conjunction_type,
                                      return_immediately=True)

    # wait for the request to finish, get the data once done
    s.wait()
    s.get_data()

    # check that conjunctions were cound and the conjunction type of
    # the first is south b-trace
    assert len(s.data) > 0 and \
        s.data[0].conjunction_type == pyaurorax.conjunctions.CONJUNCTION_TYPE_SBTRACE


@pytest.mark.conjunctions
@pytest.mark.parametrize("precision_value", [30, 60])
def test_conjunctions_search_asynchronous_with_epoch_precision(precision_value):
    # set up params
    start = datetime.datetime(2008, 1, 1, 0, 0, 0)
    end = datetime.datetime(2008, 1, 1, 23, 59, 59)
    ground_params = [
        {
            "programs": ["themis-asi"],
            "instrument_types": ["panchromatic ASI"]
        }
    ]
    space_params = [
        {
            "programs": ["themis"],
            "instrument_types": ["footprint"]
        }
    ]
    distance = 500

    # do asynchronous search
    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      distance,
                                      ground=ground_params,
                                      space=space_params,
                                      epoch_search_precision=precision_value)

    # wait for the request to finish, get the data once done
    s.wait()
    s.get_data()

    # check to make sure we got at least one result, and the
    # first result is a Conjunction object
    assert len(s.data) > 0 and type(s.data[0]) is Conjunction


@pytest.mark.conjunctions
def test_conjunction_search_describe():
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
    describe_str = pyaurorax.conjunctions.describe(s)

    # test response
    if (describe_str is not None and describe_str == expected_response_str):
        assert True
    else:
        assert False


@pytest.mark.conjunctions
def test_get_request_url():
    request_id = "testing-request-id"
    expected_url = pyaurorax.api.get_base_url() + "/api/v1/conjunctions/requests/" + request_id
    returned_url = pyaurorax.conjunctions.get_request_url(request_id)
    assert returned_url == expected_url
