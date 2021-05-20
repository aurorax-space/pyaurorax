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

    s = aurorax.conjunctions.search_async(start=start, end=end, ground=ground_params, space=space_params, default_distance=distance)
    s.execute()
    s.wait()
    s.get_data()

    assert type(s.data) is list and len(s.data) > 0

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

    s = aurorax.conjunctions.search(start=start, end=end, ground=ground_params, space=space_params, default_distance=distance, verbose=True)

    assert type(s.data) is list and len(s.data) > 0

def test_create_conjunction_object():
    assert False

def test_search_conjunctions_with_metadata_filters():
    assert False

def test_search_conjunctions_with_hemispheres():
    assert False

def test_search_conjunctions_with_max_distances():
    assert False

def test_search_conjunctions_space_only():
    assert False

def test_search_conjunctions_with_conjunction_types():
    assert False