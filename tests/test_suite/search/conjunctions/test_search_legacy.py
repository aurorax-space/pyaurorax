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
from pyaurorax.search import Conjunction, CONJUNCTION_TYPE_SBTRACE


@pytest.mark.search_ro
def test_simple(aurorax):
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

    # check
    assert len(s.data) > 0
    assert isinstance(s.data[0], Conjunction) is True


@pytest.mark.search_ro
def test_with_response_format(aurorax):
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


@pytest.mark.search_ro
def test_events_and_space(aurorax):
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


@pytest.mark.search_ro
def test_async(aurorax):
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


@pytest.mark.search_ro
def test_async_cancel(aurorax):
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


@pytest.mark.search_ro
def test_async_with_response_format(aurorax):
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


@pytest.mark.search_ro
def test_async_events_and_space(aurorax):
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


@pytest.mark.search_ro
def test_async_with_metadata_filters(aurorax):
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


@pytest.mark.search_ro
def test_async_space_only_with_hemispheres(aurorax):
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


@pytest.mark.search_ro
def test_async_with_advanced_distances(aurorax):
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


@pytest.mark.search_ro
def test_async_with_conjunction_types(aurorax):
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
