# Copyright 2024 University of Calgary
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
import datetime
import random
import string
from pyaurorax.search import Conjunction, ConjunctionSearch, CONJUNCTION_TYPE_SBTRACE
from pyaurorax import AuroraXError


@pytest.mark.search_conjunctions
def test_conjunctions_search_object(aurorax):
    # set up params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 6, 59, 59)
    ground_params = [{"programs": ["themis-asi"]}]
    space_params = [{"programs": ["swarm"]}]
    events_params = [{"programs": ["events"]}]
    distance = 200

    # create search object
    s = ConjunctionSearch(
        aurorax,
        start,
        end,
        ground=ground_params,
        space=space_params,
        events=events_params,
        distance=distance,
    )

    # check to make sure type is correct
    assert isinstance(s, ConjunctionSearch) is True


@pytest.mark.search_conjunctions
def test_conjunctions_search_query_property(aurorax):
    # set up params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 6, 59, 59)
    ground_params = [{"programs": ["themis-asi"]}]
    space_params = [{"programs": ["swarm"]}]
    events_params = [{"programs": ["events"]}]
    distance = 200

    # create object
    s = ConjunctionSearch(
        aurorax,
        start,
        end,
        ground=ground_params,
        space=space_params,
        events=events_params,
        distance=distance,
    )

    # try to get the query parameter
    assert "query" in dir(s)
    assert s.query is not None


@pytest.mark.search_conjunctions
def test_conjunctions_search_object_with_advanced_distances(aurorax):
    # set up params
    start = datetime.datetime(2019, 2, 5, 0, 0, 0)
    end = datetime.datetime(2019, 2, 5, 23, 59, 59)
    ground_params = [{"programs": ["themis-asi"]}]
    space_params = [{"programs": ["swarm"]}, {"programs": ["themis"]}]
    advanced_distances = {"ground1-space1": 200, "space1-space2": 500}

    # create object
    s = ConjunctionSearch(aurorax, start, end, advanced_distances, ground=ground_params, space=space_params)

    # try to get the query parameter
    assert "query" in dir(s)
    assert s.query is not None


@pytest.mark.search_conjunctions
@pytest.mark.parametrize("num_ground_blocks,num_space_blocks,num_events_blocks,should_pass", [(5, 5, 0, True), (5, 6, 0, False), (6, 5, 0, False),
                                                                                              (5, 4, 1, True), (5, 5, 1, False), (5, 4, 2, False),
                                                                                              (0, 5, 5, True), (5, 0, 5, True), (0, 5, 6, False),
                                                                                              (11, 0, 0, False), (0, 11, 0, False), (0, 0, 11, False),
                                                                                              (10, 0, 0, True), (0, 10, 0, True), (0, 0, 10, True)])
def test_conjunctions_too_many_criteria_blocks(aurorax, num_ground_blocks, num_space_blocks, num_events_blocks, should_pass):
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
    s = ConjunctionSearch(aurorax, start, end, distance, ground=ground, space=space, events=events)

    # check the criteria block count
    try:
        s.check_criteria_block_count_validity()
        exception_raised = False
    except AuroraXError:
        exception_raised = True

    # check if the test should pass or fail
    if (should_pass is True and exception_raised is True):
        raise AssertionError("Test should pass but exception was encountered")
    elif (should_pass is False and exception_raised is False):
        raise AssertionError("Test should not pass but exception was not encountered")


@pytest.mark.search_conjunctions
def test_conjunctions_search_synchronous(aurorax):
    # set params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 23, 59, 59)
    ground_params = [{"programs": ["themis-asi"]}]
    space_params = [{"programs": ["swarm", "themis"]}]
    distance = 500

    # do search
    s = aurorax.search.conjunctions.search(
        start,
        end,
        distance,
        ground=ground_params,
        space=space_params,
        verbose=False,
    )

    # check to make sure we got at least one result, and the
    # first result is a Conjunction object
    assert len(s.data) > 0
    assert isinstance(s.data[0], Conjunction) is True


@pytest.mark.search_conjunctions
def test_conjunctions_search_synchronous_with_response_format(aurorax):
    # set up params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 23, 59, 59)
    ground_params = [{"programs": ["themis-asi"], "platforms": ["gillam"]}]
    space_params = [{"programs": ["swarm", "themis"]}]
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
    s = aurorax.search.conjunctions.search(start,
                                           end,
                                           distance,
                                           ground=ground_params,
                                           space=space_params,
                                           verbose=False,
                                           response_format=response_format)

    # do checks on response data
    assert len(s.data) > 0
    assert isinstance(s.data[0], dict) is True
    for key in s.data[0].keys():
        assert key in response_format.keys()


@pytest.mark.search_conjunctions
def test_conjunctions_search_synchronous_events_and_space(aurorax):
    # set up params
    start = datetime.datetime(2008, 3, 1, 0, 0, 0)
    end = datetime.datetime(2008, 3, 1, 23, 59, 59)
    space_params = [{"programs": ["swarm", "themis"]}]
    events_params = [{"programs": ["events"], "instrument_types": ["substorm onset"]}]
    distance = 500

    # do synchronous search
    s = aurorax.search.conjunctions.search(
        start,
        end,
        distance,
        space=space_params,
        events=events_params,
        verbose=False,
    )

    # check to make sure we got at least one result, and the
    # first result is a Conjunction object
    assert len(s.data) > 0
    assert isinstance(s.data[0], Conjunction)


@pytest.mark.search_conjunctions
def test_conjunctions_search_asynchronous(aurorax):
    # set up params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 6, 59, 59)
    ground_params = [{"programs": ["themis-asi"]}]
    space_params = [{"programs": ["swarm"]}]
    distance = 100

    # so asynchronous search
    s = aurorax.search.conjunctions.search(
        start,
        end,
        distance,
        ground=ground_params,
        space=space_params,
        return_immediately=True,
    )

    # wait for the request to finish, get the data once done
    s.wait()
    s.get_data()

    # check to make sure we got at least one result, and the
    # first result is a Conjunction object
    assert len(s.data) > 0
    assert isinstance(s.data[0], Conjunction) is True


@pytest.mark.search_conjunctions
def test_conjunctions_search_asynchronous_cancel(aurorax):
    # set up params
    start = datetime.datetime(2019, 1, 1, 0, 0, 0)
    end = datetime.datetime(2019, 12, 31, 23, 59, 59)
    ground_params = [{"programs": ["themis-asi"]}]
    space_params = [{"programs": ["swarm"]}]
    conjunction_types = [CONJUNCTION_TYPE_SBTRACE]
    distance = 100

    # do asynchronous search
    s = aurorax.search.conjunctions.search(start,
                                           end,
                                           distance,
                                           ground=ground_params,
                                           space=space_params,
                                           conjunction_types=conjunction_types,
                                           return_immediately=True)

    # cancel request
    result = s.cancel(wait=True)

    # check to make sure it has been cancelled
    assert result == 0


@pytest.mark.search_conjunctions
def test_conjunctions_search_asynchronous_with_response_format(aurorax):
    # set up params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 23, 59, 59)
    ground_params = [{"programs": ["themis-asi"], "platforms": ["gillam"]}]
    space_params = [{"programs": ["swarm", "themis"]}]
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
    s = aurorax.search.conjunctions.search(start,
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
    assert len(s.data) > 0
    assert isinstance(s.data[0], dict)
    for key in s.data[0].keys():
        assert key in response_format.keys()


@pytest.mark.search_conjunctions
def test_conjunctions_search_asynchronous_events_and_space(aurorax):
    # set up params
    start = datetime.datetime(2008, 3, 1, 0, 0, 0)
    end = datetime.datetime(2008, 3, 1, 23, 59, 59)
    space_params = [{"programs": ["swarm", "themis"]}]
    events_params = [{"programs": ["events"], "instrument_types": ["substorm onset"]}]
    distance = 500

    # do asynchronous search
    s = aurorax.search.conjunctions.search(
        start,
        end,
        distance,
        space=space_params,
        events=events_params,
        verbose=False,
        return_immediately=True,
    )

    # wait for the request to finish, get the data once done
    s.wait()
    s.get_data()

    # check to make sure we got at least one result, and the
    # first result is a Conjunction object
    assert len(s.data) > 0
    assert isinstance(s.data[0], Conjunction) is True


@pytest.mark.search_conjunctions
def test_conjunctions_search_asynchronous_with_metadata_filters(aurorax):
    # set up params
    start = datetime.datetime(2019, 3, 27, 0, 0, 0)
    end = datetime.datetime(2019, 3, 27, 23, 59, 59)
    ground_params = [{
        "programs": ["themis-asi"],
        "ephemeris_metadata_filters": {
            "logical_operator": "AND",
            "expressions": [{
                "key": "ml_cloud_v1",
                "operator": "=",
                "values": ["not classified as cloud"]
            }]
        }
    }]
    space_params = [{
        "programs": ["swarm"],
        "ephemeris_metadata_filters": {
            "logical_operator": "AND",
            "expressions": [{
                "key": "nbtrace_region",
                "operator": "=",
                "values": ["north polar cap"]
            }]
        }
    }]
    distance = 300

    # do asynchronous search
    s = aurorax.search.conjunctions.search(
        start,
        end,
        distance,
        ground=ground_params,
        space=space_params,
        return_immediately=True,
    )

    # wait for the request to finish, get the data once done
    s.wait()
    s.get_data()

    # check to make sure we got at least one result, and the
    # first result is a Conjunction object
    assert len(s.data) > 0
    assert isinstance(s.data[0], Conjunction)


@pytest.mark.search_conjunctions
def test_conjunctions_search_asynchronous_space_only_with_hemispheres(aurorax):
    # set up params
    start = datetime.datetime(2019, 2, 1, 0, 0, 0)
    end = datetime.datetime(2019, 2, 1, 23, 59, 59)
    space_params = [{"programs": ["swarm"], "hemisphere": ["southern"]}, {"programs": ["themis"], "hemisphere": ["northern"]}]
    distance = 300

    # do asynchronous search
    s = aurorax.search.conjunctions.search(start, end, distance, space=space_params, return_immediately=True)

    # wait for the request to finish, get the data once done
    s.wait()
    s.get_data()

    # check to make sure we got at least one result, and the
    # first result is a Conjunction object
    assert len(s.data) > 0
    assert isinstance(s.data[0], Conjunction) is True


@pytest.mark.search_conjunctions
def test_conjunctions_search_asynchronous_with_advanced_distances(aurorax):
    # set up params
    start = datetime.datetime(2019, 2, 5, 0, 0, 0)
    end = datetime.datetime(2019, 2, 5, 23, 59, 59)
    ground_params = [{"programs": ["themis-asi"]}]
    space_params = [{"programs": ["swarm"]}, {"programs": ["themis"]}]
    advanced_distances = {"ground1-space1": 200, "space1-space2": 500}

    # do asynchronous search
    s = aurorax.search.conjunctions.search(
        start,
        end,
        advanced_distances,
        ground=ground_params,
        space=space_params,
        return_immediately=True,
    )

    # wait for the request to finish, get the data once done
    s.wait()
    s.get_data()

    # compare the distances
    query_distance_keys = s.query["max_distances"].keys()
    distances_set = ["ground1-space1", "ground1-space2", "space1-space2"]
    g1s1_distance_set = s.query["max_distances"]["ground1-space1"] == advanced_distances["ground1-space1"]
    s1s2_distance_set = s.query["max_distances"]["space1-space2"] == advanced_distances["space1-space2"]

    # do checks
    assert all(x in query_distance_keys for x in distances_set) and g1s1_distance_set and s1s2_distance_set and len(s.data) > 0


@pytest.mark.search_conjunctions
def test_conjunctions_search_asynchronous_with_conjunction_types(aurorax):
    # set up params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 23, 59, 59)
    ground_params = [{"programs": ["themis-asi"]}]
    space_params = [{"programs": ["swarm"]}]
    conjunction_type = [CONJUNCTION_TYPE_SBTRACE]
    distance = 100

    # do asynchronous search
    s = aurorax.search.conjunctions.search(start,
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
    assert len(s.data) > 0
    assert s.data[0].conjunction_type == CONJUNCTION_TYPE_SBTRACE


@pytest.mark.search_conjunctions
def test_conjunction_search_describe(aurorax):
    # set params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 23, 59, 59)
    ground_params = [{"programs": ["themis-asi"]}]
    space_params = [{"programs": ["swarm", "themis"]}]
    distance = 500
    expected_response_str = "Find conjunctions of type (nbtrace) with epoch precision " \
        "of 60 seconds between data sources of ground1=(program in (themis-asi)) AND " \
        "space1=(program in (swarm, themis)) WHERE epochs are between 2020-01-01T00:00:00 " \
        "AND 2020-01-01T23:59:59 UTC HAVING max distances between location points of " \
        "ground1-space1=500 km."

    # create search object
    s = ConjunctionSearch(aurorax, start, end, distance, ground=ground_params, space=space_params)

    # get describe string
    describe_str = aurorax.search.conjunctions.describe(s)

    # test response
    assert describe_str is not None
    assert describe_str == expected_response_str


@pytest.mark.search_conjunctions
def test_get_request_url(aurorax):
    request_id = "testing-request-id"
    expected_url = aurorax.api_base_url + "/api/v1/conjunctions/requests/" + request_id
    returned_url = aurorax.search.conjunctions.get_request_url(request_id)
    assert returned_url == expected_url
