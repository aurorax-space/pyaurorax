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
from pyaurorax.search import (
    ConjunctionSearch,
    GroundCriteriaBlock,
    SpaceCriteriaBlock,
    EventsCriteriaBlock,
    CustomLocationsCriteriaBlock,
)
from pyaurorax import AuroraXError


@pytest.mark.search_ro
@pytest.mark.parametrize("test_dict", [
    {
        "ground": [GroundCriteriaBlock(programs=["themis-asi"])],
        "space": [SpaceCriteriaBlock(programs=["swarm"])],
    },
    {
        "ground": [GroundCriteriaBlock(programs=["themis-asi"])],
        "space": [SpaceCriteriaBlock(programs=["swarm"])],
        "events": [EventsCriteriaBlock()],
    },
    {
        "custom": [CustomLocationsCriteriaBlock(locations=[(51.05, -114.)])],
        "space": [SpaceCriteriaBlock(programs=["swarm"])],
    },
    {
        "ground": [GroundCriteriaBlock(programs=["themis-asi"]),
                   GroundCriteriaBlock(programs=["go-canada"], instrument_types=["riometer"])],
        "space": [SpaceCriteriaBlock(programs=["swarm"])],
    },
])
def test_create_object(aurorax, test_dict, capsys):
    # set up params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 6, 59, 59)
    distance = 200

    # create search object
    s = ConjunctionSearch(
        aurorax,
        start,
        end,
        ground=test_dict["ground"] if "ground" in test_dict else [],
        space=test_dict["space"] if "space" in test_dict else [],
        events=test_dict["events"] if "events" in test_dict else [],
        custom_locations=test_dict["custom_locations"] if "custom_locations" in test_dict else [],
        distance=distance,
    )

    # check
    assert isinstance(s, ConjunctionSearch) is True
    assert s.query is not None and s.query != ""

    # check __str__ and __repr__ for ConjunctionSearch type
    print_str = str(s)
    assert print_str != ""
    assert isinstance(str(s), str) is True
    assert isinstance(repr(s), str) is True
    s.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # check describe function
    description = s.describe()
    print(description)
    assert description != ""


@pytest.mark.search_ro
def test_create_object_with_advanced_distances(aurorax, capsys):
    # set up params
    start = datetime.datetime(2019, 2, 5, 0, 0, 0)
    end = datetime.datetime(2019, 2, 5, 23, 59, 59)
    ground = [GroundCriteriaBlock(programs=["themis-asi"])]
    space = [SpaceCriteriaBlock(programs=["swarm"]), SpaceCriteriaBlock(programs=["themis"])]
    advanced_distances = aurorax.search.conjunctions.create_advanced_distance_combos(ground=1, space=2)
    advanced_distances["space1-space2"] = 500
    advanced_distances["ground1-space1"] = 200

    # create object
    s = ConjunctionSearch(aurorax, start, end, advanced_distances, ground=ground, space=space)

    # check
    assert isinstance(s, ConjunctionSearch) is True
    assert s.query is not None and s.query != ""

    # check __str__ and __repr__ for ConjunctionSearch type
    print_str = str(s)
    assert print_str != ""
    assert isinstance(str(s), str) is True
    assert isinstance(repr(s), str) is True
    s.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # check describe function
    description = s.describe()
    assert description != ""


@pytest.mark.search_ro
def test_create_response_format_template(aurorax):
    response_format = aurorax.search.conjunctions.create_response_format_template()
    assert isinstance(response_format, dict) is True


@pytest.mark.search_ro
@pytest.mark.parametrize("num_ground,num_space,num_events,num_custom,success", [
    (5, 5, 0, 0, True),
    (5, 6, 0, 0, False),
    (6, 5, 0, 0, False),
    (5, 4, 1, 0, True),
    (5, 5, 1, 0, False),
    (5, 4, 2, 0, False),
    (0, 5, 5, 0, True),
    (5, 0, 5, 0, True),
    (0, 5, 6, 0, False),
    (11, 0, 0, 0, False),
    (0, 11, 0, 0, False),
    (0, 0, 11, 0, False),
    (10, 0, 0, 0, True),
    (0, 10, 0, 0, True),
    (0, 0, 10, 0, True),
    (2, 2, 2, 2, True),
    (2, 2, 3, 3, True),
    (2, 2, 3, 4, False),
    (0, 0, 0, 10, True),
    (0, 0, 0, 11, False),
])
def test_too_many_criteria_blocks(aurorax, num_ground, num_space, num_events, num_custom, success):
    # set basic search params
    start = datetime.datetime(2019, 1, 1, 0, 0, 0)
    end = datetime.datetime(2019, 1, 31, 23, 59, 59)
    distance = 300

    # set ground
    ground = []
    for _ in range(0, num_ground):
        random_str = ''.join(random.sample(string.ascii_lowercase, 10))
        ground.append(GroundCriteriaBlock(programs=[random_str]))

    # set space
    space = []
    for _ in range(0, num_space):
        random_str = ''.join(random.sample(string.ascii_lowercase, 10))
        space.append(SpaceCriteriaBlock(programs=[random_str]))

    # set events
    events = []
    for _ in range(0, num_events):
        random_str = ''.join(random.sample(string.ascii_lowercase, 10))
        events.append(EventsCriteriaBlock(platforms=[random_str]))

    # set custom
    custom = []
    for _ in range(0, num_custom):
        random_str = ''.join(random.sample(string.ascii_lowercase, 10))
        custom.append(CustomLocationsCriteriaBlock(locations=[(50., 50.)]))

    # create search object
    s = ConjunctionSearch(aurorax, start, end, distance, ground=ground, space=space, events=events, custom_locations=custom)

    # check the criteria block count
    try:
        s.check_criteria_block_count_validity()
        exception_raised = False
    except AuroraXError:
        exception_raised = True

    # check if the test should pass or fail
    if (success is True and exception_raised is True):
        raise AssertionError("Test should pass but exception was encountered")
    elif (success is False and exception_raised is False):
        raise AssertionError("Test should not pass but exception was not encountered")


@pytest.mark.search_ro
def test_bad_ground_criteria_blocks(aurorax):
    # set basic search params
    start = datetime.datetime(2019, 1, 1, 0, 0, 0)
    end = datetime.datetime(2019, 1, 31, 23, 59, 59)
    distance = 300

    # set criteria blocks
    ground = [SpaceCriteriaBlock(programs=["themis-asi"])]

    # create object
    with pytest.raises(ValueError) as e_info:
        _ = ConjunctionSearch(aurorax, start, end, distance, ground=ground)  # type: ignore
    assert "A SpaceCriteriaBlock object was found in the 'ground' parameter" in str(e_info)


@pytest.mark.search_ro
def test_bad_space_criteria_blocks(aurorax):
    # set basic search params
    start = datetime.datetime(2019, 1, 1, 0, 0, 0)
    end = datetime.datetime(2019, 1, 31, 23, 59, 59)
    distance = 300

    # set criteria blocks
    space = [GroundCriteriaBlock(programs=["themis-asi"])]

    # create object
    with pytest.raises(ValueError) as e_info:
        _ = ConjunctionSearch(aurorax, start, end, distance, space=space)  # type: ignore
    assert "A GroundCriteriaBlock object was found in the 'space' parameter" in str(e_info)


@pytest.mark.search_ro
def test_bad_events_criteria_blocks(aurorax):
    # set basic search params
    start = datetime.datetime(2019, 1, 1, 0, 0, 0)
    end = datetime.datetime(2019, 1, 31, 23, 59, 59)
    distance = 300

    # set criteria blocks
    events = [GroundCriteriaBlock(programs=["themis-asi"])]

    # create object
    with pytest.raises(ValueError) as e_info:
        _ = ConjunctionSearch(aurorax, start, end, distance, events=events)  # type: ignore
    assert "A GroundCriteriaBlock object was found in the 'events' parameter" in str(e_info)


@pytest.mark.search_ro
def test_bad_custom_criteria_blocks(aurorax):
    # set basic search params
    start = datetime.datetime(2019, 1, 1, 0, 0, 0)
    end = datetime.datetime(2019, 1, 31, 23, 59, 59)
    distance = 300

    # set criteria blocks
    custom = [EventsCriteriaBlock(platforms=["something"])]

    # create object
    with pytest.raises(ValueError) as e_info:
        _ = ConjunctionSearch(aurorax, start, end, distance, custom_locations=custom)  # type: ignore
    assert "A EventsCriteriaBlock object was found in the 'custom_locations' parameter" in str(e_info)
