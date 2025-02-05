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
from pyaurorax.search import ConjunctionSearch
from pyaurorax import AuroraXError


@pytest.mark.search_ro
def test_create_object(aurorax):
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

    # check
    assert isinstance(s, ConjunctionSearch) is True
    assert s.query is not None and s.query != ""


@pytest.mark.search_ro
def test_with_advanced_distances(aurorax):
    # set up params
    start = datetime.datetime(2019, 2, 5, 0, 0, 0)
    end = datetime.datetime(2019, 2, 5, 23, 59, 59)
    ground_params = [{"programs": ["themis-asi"]}]
    space_params = [{"programs": ["swarm"]}, {"programs": ["themis"]}]
    advanced_distances = {"ground1-space1": 200, "space1-space2": 500}

    # create object
    s = ConjunctionSearch(aurorax, start, end, advanced_distances, ground=ground_params, space=space_params)

    # check
    assert isinstance(s, ConjunctionSearch) is True
    assert s.query is not None and s.query != ""


@pytest.mark.search_ro
@pytest.mark.parametrize("num_ground_blocks,num_space_blocks,num_events_blocks,should_pass", [
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
    (0, 0, 10, True),
])
def test_too_many_criteria_blocks(aurorax, num_ground_blocks, num_space_blocks, num_events_blocks, should_pass):
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
