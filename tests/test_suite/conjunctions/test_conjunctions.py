import pytest
import datetime
import random
import string
import pyaurorax
from pyaurorax.conjunctions import Conjunction


@pytest.mark.conjunctions
def test_conjunctions_search_object():
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

    s = pyaurorax.conjunctions.Search(start,
                                      end,
                                      ground=ground_params,
                                      space=space_params,
                                      events=events_params,
                                      distance=distance)

    assert type(s) is pyaurorax.conjunctions.Search


@pytest.mark.conjunctions
def test_conjunctions_search_query_property():
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

    s = pyaurorax.conjunctions.Search(start,
                                      end,
                                      ground=ground_params,
                                      space=space_params,
                                      events=events_params,
                                      distance=distance)
    try:
        _ = s.query
        assert True
    except Exception:
        assert False


@pytest.mark.conjunctions
def test_conjunctions_search_object_with_advanced_distances():
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

    s = pyaurorax.conjunctions.Search(start,
                                      end,
                                      advanced_distances,
                                      ground=ground_params,
                                      space=space_params)
    try:
        _ = s.query
        assert True
    except Exception:
        assert False


@pytest.mark.conjunctions
def test_conjunctions_search_asynchronous():
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 6, 59, 59)
    ground_params = [
        {"programs": ["themis-asi"]}
    ]
    space_params = [
        {"programs": ["swarm"]}
    ]
    distance = 100

    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      distance,
                                      ground=ground_params,
                                      space=space_params,
                                      return_immediately=True)

    s.wait()
    s.get_data()

    assert len(s.data) > 0 and type(s.data[0]) is Conjunction


@pytest.mark.conjunctions
def test_conjunctions_search_synchronous():
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 4, 23, 59, 59)
    ground_params = [
        {"programs": ["themis-asi"]},
        {"platforms": ["gillam"]}
    ]
    space_params = [
        {"programs": ["swarm"]},
        {"programs": ["themis"]}
    ]
    distance = 300

    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      distance,
                                      ground=ground_params,
                                      space=space_params,
                                      verbose=False)

    assert len(s.data) > 0 and type(s.data[0]) is Conjunction


@pytest.mark.conjunctions
def test_conjunctions_search_synchronous_with_response_format():
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 4, 23, 59, 59)
    ground_params = [
        {"programs": ["themis-asi"]},
        {"platforms": ["gillam"]}
    ]
    space_params = [
        {"programs": ["swarm"]},
        {"programs": ["themis"]}
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

    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      distance,
                                      ground=ground_params,
                                      space=space_params,
                                      verbose=False,
                                      response_format=response_format)

    assert len(s.data) > 0 and \
        type(s.data[0]) is dict and \
        "max_distance" not in s.data[0].keys()


@pytest.mark.conjunctions
def test_conjunctions_search_synchronous_with_metadata_filters():
    start = datetime.datetime(2019, 3, 1, 0, 0, 0)
    end = datetime.datetime(2019, 3, 31, 23, 59, 59)
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

    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      distance,
                                      ground=ground_params,
                                      space=space_params,
                                      return_immediately=True)
    s.wait()
    s.get_data()

    assert len(s.data) > 0 and type(s.data[0]) is Conjunction


@pytest.mark.conjunctions
def test_conjunctions_search_space_only_with_hemispheres():
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

    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      distance,
                                      space=space_params,
                                      return_immediately=True)
    s.wait()
    s.get_data()

    assert len(s.data) > 0 and type(s.data[0]) is Conjunction


@pytest.mark.conjunctions
def test_conjunctions_search_with_advanced_distances():
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

    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      advanced_distances,
                                      ground=ground_params,
                                      space=space_params,
                                      return_immediately=True)
    s.wait()
    s.get_data()

    query_distance_keys = s.query["max_distances"].keys()
    distances_set = ["ground1-space1", "ground1-space2", "space1-space2"]
    g1s1_distance_set = s.query["max_distances"]["ground1-space1"] == advanced_distances["ground1-space1"]
    s1s2_distance_set = s.query["max_distances"]["space1-space2"] == advanced_distances["space1-space2"]

    assert all(x in query_distance_keys for x in distances_set) and \
        g1s1_distance_set and s1s2_distance_set and len(s.data) > 0


@pytest.mark.conjunctions
def test_conjunctions_search_with_conjunction_types():
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

    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      distance,
                                      ground=ground_params,
                                      space=space_params,
                                      conjunction_types=conjunction_type,
                                      return_immediately=True)
    s.wait()
    s.get_data()

    assert len(s.data) > 0 and s.data[0].conjunction_type == pyaurorax.conjunctions.CONJUNCTION_TYPE_SBTRACE


@pytest.mark.conjunctions
def test_conjunctions_cancel_search():
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

    s = pyaurorax.conjunctions.Search(start,
                                      end,
                                      distance,
                                      ground=ground_params,
                                      space=space_params,
                                      conjunction_types=conjunction_types)
    s.execute()

    result = s.cancel(wait=True)

    assert result == 1


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

    # init search object
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
def test_conjunctions_search_with_epoch_precision():
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

    # test 60s precision (default)
    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      distance,
                                      ground=ground_params,
                                      space=space_params,
                                      epoch_search_precision=60)
    assert len(s.data) != 0

    # test 30s precision
    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      distance,
                                      ground=ground_params,
                                      space=space_params,
                                      epoch_search_precision=30)
    assert len(s.data) != 0
