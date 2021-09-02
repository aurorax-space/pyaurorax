from aurorax.conjunctions import Conjunction
import aurorax
import datetime


def test_search_conjunctions_asynchronous():
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 6, 59, 59)
    ground_params = [{
        "programs": ["themis-asi"]
    }]
    space_params = [{
        "programs": ["swarm"]
    }]
    distance = 100

    s = aurorax.conjunctions.search_async(
        start=start, end=end, ground=ground_params, space=space_params, default_distance=distance)

    s.wait()
    s.get_data()

    assert len(s.data) > 0 and type(s.data[0]) is Conjunction


def test_search_multi_conjunctions_synchronous():
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 4, 23, 59, 59)
    ground_params = [{
        "programs": ["themis-asi"]
    },
        {
        "platforms": ["gillam"]
    }]
    space_params = [{
        "programs": ["swarm"]
    },
        {
        "programs": ["themis"]
    }]
    distance = 300

    s = aurorax.conjunctions.search(start=start, end=end, ground=ground_params,
                                    space=space_params, default_distance=distance, verbose=False)

    assert len(s.data) > 0 and type(s.data[0]) is Conjunction


def test_create_conjunction_object():
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 6, 59, 59)
    ground_params = [{
        "programs": ["themis-asi"]
    }]
    space_params = [{
        "programs": ["swarm"]
    }]
    distance = 200

    c = aurorax.conjunctions.search_async(
        start=start, end=end, ground=ground_params, space=space_params, default_distance=distance)
    c.wait()
    c.get_data()
    if len(c.data) == 0:
        assert False

    assert type(c.data[0]) is Conjunction


def test_search_conjunctions_with_metadata_filters():
    start = datetime.datetime(2019, 3, 1, 0, 0, 0)
    end = datetime.datetime(2019, 3, 31, 23, 59, 59)
    ground_params = [{
        "programs": ["themis-asi"],
        "ephemeris_metadata_filters": [
            {
                "key": "ml_cloud_v1",
                "operator": "=",
                "values": [
                    "not classified as cloud"
                ]
            }
        ]
    }]
    space_params = [{
        "programs": ["swarm"],
        "ephemeris_metadata_filters": [
            {
                "key": "nbtrace_region",
                "operator": "=",
                "values": [
                    "north polar cap"
                ]
            }
        ]
    }]

    s = aurorax.conjunctions.search_async(
        start=start, end=end, ground=ground_params, space=space_params, default_distance=300)
    s.wait()
    s.get_data()

    assert len(s.data) > 0 and type(s.data[0]) is Conjunction


def test_search_conjunctions_space_only_with_hemispheres():
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

    s = aurorax.conjunctions.search_async(
        start=start, end=end, ground=[], space=space_params)
    s.wait()
    s.get_data()

    assert len(s.data) > 0 and type(s.data[0]) is Conjunction


def test_search_conjunctions_with_max_distances():
    start = datetime.datetime(2019, 2, 5, 0, 0, 0)
    end = datetime.datetime(2019, 2, 5, 23, 59, 59)
    ground_params = [
        {
            "programs": ["themis-asi"]
        }
    ]
    space_params = [
        {
            "programs": ["swarm"]
        },
        {
            "programs": ["themis"]
        }
    ]
    distances = {
        "ground1-space1": 200,
        "space1-space2": 500
    }

    s = aurorax.conjunctions.search_async(
        start=start, end=end, ground=ground_params, space=space_params, max_distances=distances)
    s.wait()
    s.get_data()

    query_distance_keys = s.query["max_distances"].keys()
    distances_set = ["ground1-space1", "ground1-space2", "space1-space2"]
    g1s1_distance_set = s.query["max_distances"]["ground1-space1"] == distances["ground1-space1"]
    s1s2_distance_set = s.query["max_distances"]["space1-space2"] == distances["space1-space2"]

    assert all(x in query_distance_keys for x in distances_set) and g1s1_distance_set and s1s2_distance_set and len(
        s.data) > 0


def test_search_conjunctions_with_conjunction_types():
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 23, 59, 59)
    ground_params = [{
        "programs": ["themis-asi"]
    }]
    space_params = [{
        "programs": ["swarm"]
    }]
    conjunction_type = ["sbtrace"]
    distance = 100

    s = aurorax.conjunctions.search_async(start=start, end=end, ground=ground_params,
                                          space=space_params, default_distance=distance, conjunction_types=conjunction_type)
    s.wait()
    s.get_data()

    assert len(s.data) > 0 and s.data[0].conjunction_type == "sbtrace"


def test_cancel_conjunction_search():
    start = datetime.datetime(2019, 1, 1, 0, 0, 0)
    end = datetime.datetime(2019, 12, 31, 23, 59, 59)
    ground_params = [{
        "programs": ["themis-asi"]
    }]
    space_params = [{
        "programs": ["swarm"]
    }]
    conjunction_type = ["sbtrace"]
    distance = 100

    s = aurorax.conjunctions.Search(
        start, end, ground_params, space_params, conjunction_type, default_distance=distance)
    s.execute()

    result = s.cancel(wait=True)

    assert result == 1
