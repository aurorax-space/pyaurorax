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
def test_simple(aurorax, capsys):
    # set timeframe and distance
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 6, 59, 59)
    distance = 500

    # set criteria blocks
    ground = [aurorax.search.GroundCriteriaBlock(programs=["themis-asi"])]
    space = [aurorax.search.SpaceCriteriaBlock(programs=["swarm"])]

    # perform search
    s = aurorax.search.conjunctions.search(start, end, distance, ground=ground, space=space, verbose=True)
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # check results
    assert len(s.data) > 0
    assert isinstance(s.data[0], Conjunction) is True

    # check __str__ and __repr__ for ConjunctionSearch type
    print_str = str(s)
    assert print_str != ""
    assert isinstance(str(s), str) is True
    assert isinstance(repr(s), str) is True
    s.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # check __str__ and __repr__ for Conjunction type
    print_str = str(s.data[0])
    assert print_str != ""
    assert isinstance(str(s.data[0]), str) is True
    assert isinstance(repr(s.data[0]), str) is True
    s.data[0].pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.search_ro
def test_simple_no_results(aurorax, capsys):
    # set timeframe and distance
    start = datetime.datetime(1990, 1, 1, 0, 0, 0)
    end = datetime.datetime(1990, 1, 1, 0, 59, 59)
    distance = 200

    # set criteria blocks
    ground = [aurorax.search.GroundCriteriaBlock(programs=["themis-asi"])]
    space = [aurorax.search.SpaceCriteriaBlock(programs=["swarm"])]

    # perform search
    s = aurorax.search.conjunctions.search(start, end, distance, ground=ground, space=space)

    # check results
    assert len(s.data) == 0

    # check __str__ and __repr__ for ConjunctionSearch type
    print_str = str(s)
    assert print_str != ""
    assert isinstance(str(s), str) is True
    assert isinstance(repr(s), str) is True
    s.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.search_ro
def test_simple_exactly_one_result(aurorax, capsys):
    # set timeframe and distance
    start = datetime.datetime(2020, 1, 1, 0, 7, 0)
    end = datetime.datetime(2020, 1, 1, 0, 9, 0)
    distance = 200

    # set criteria blocks
    ground = [aurorax.search.GroundCriteriaBlock(programs=["themis-asi"])]
    space = [aurorax.search.SpaceCriteriaBlock(programs=["swarm"])]

    # perform search
    s = aurorax.search.conjunctions.search(start, end, distance, ground=ground, space=space)

    # check results
    assert len(s.data) == 1

    # check __str__ and __repr__ for ConjunctionSearch type
    print_str = str(s)
    assert print_str != ""
    assert isinstance(str(s), str) is True
    assert isinstance(repr(s), str) is True
    s.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.search_ro
def test_triple_search(aurorax, capsys):
    # set timeframe and distance
    start = datetime.datetime(2022, 1, 1, 0, 0, 0)
    end = datetime.datetime(2022, 1, 1, 6, 59, 59)
    distance = 500

    # set criteria blocks
    ground = [
        aurorax.search.GroundCriteriaBlock(programs=["themis-asi"]),
        aurorax.search.GroundCriteriaBlock(programs=["trex"]),
    ]
    space = [aurorax.search.SpaceCriteriaBlock(programs=["swarm"])]

    # perform search
    s = aurorax.search.conjunctions.search(start, end, distance, ground=ground, space=space)

    # check results
    assert len(s.data) > 0
    assert isinstance(s.data[0], Conjunction) is True

    # check __str__ and __repr__ for Conjunction type
    print_str = str(s.data[0])
    assert print_str != ""
    assert isinstance(str(s.data[0]), str) is True
    assert isinstance(repr(s.data[0]), str) is True
    s.data[0].pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.search_ro
def test_with_hemispheres(aurorax):
    # set up params
    start = datetime.datetime(2019, 2, 1, 0, 0, 0)
    end = datetime.datetime(2019, 2, 1, 23, 59, 59)
    space = [
        aurorax.search.SpaceCriteriaBlock(programs=["swarm"], hemisphere=["southern"]),
        aurorax.search.SpaceCriteriaBlock(programs=["themis"], hemisphere=["northern"])
    ]
    distance = 300

    # perform search
    s = aurorax.search.conjunctions.search(start, end, distance, space=space)

    # check results
    assert len(s.data) > 0
    assert isinstance(s.data[0], Conjunction) is True


@pytest.mark.search_ro
def test_conjunction_types(aurorax):
    # set up params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 23, 59, 59)
    ground = [aurorax.search.GroundCriteriaBlock(programs=["themis-asi"])]
    space = [aurorax.search.SpaceCriteriaBlock(programs=["swarm"])]
    conjunction_types = [CONJUNCTION_TYPE_SBTRACE]
    distance = 100

    # perform search
    s = aurorax.search.conjunctions.search(start, end, distance, ground=ground, space=space, conjunction_types=conjunction_types)

    # check results
    assert len(s.data) > 0
    assert isinstance(s.data[0], Conjunction) is True
    for c in s.data:
        assert c.conjunction_type == CONJUNCTION_TYPE_SBTRACE


@pytest.mark.search_ro
def test_with_ground_metadata_filters(aurorax):
    # set timeframe, distance, and conjunction type
    start = datetime.datetime(2008, 1, 11, 0, 0, 0)
    end = datetime.datetime(2008, 1, 15, 23, 59, 59)
    conjunction_types = [aurorax.search.CONJUNCTION_TYPE_NBTRACE]
    distance = 500

    # set ground criteria block
    ground = [
        aurorax.search.GroundCriteriaBlock(
            programs=["themis-asi"],
            metadata_filters=aurorax.search.MetadataFilter(expressions=[
                # only find records that were classified as APA
                aurorax.search.MetadataFilterExpression("calgary_apa_ml_v1", "classified as APA", operator="="),

                # with a confidence of at least 95%
                aurorax.search.MetadataFilterExpression("calgary_apa_ml_v1_confidence", 95, operator=">="),
            ]))
    ]

    # set space criteria block
    space = [aurorax.search.SpaceCriteriaBlock(programs=["themis"], hemisphere=["northern"])]

    # perform the search
    s = aurorax.search.conjunctions.search(
        start=start,
        end=end,
        distance=distance,
        ground=ground,
        space=space,
        conjunction_types=conjunction_types,
    )

    # check results
    assert len(s.data) > 0
    assert isinstance(s.data[0], Conjunction) is True


@pytest.mark.search_ro
def test_with_space_metadata_filters(aurorax):
    # set timeframe and distance
    start = datetime.datetime(2019, 2, 1, 0, 0, 0)
    end = datetime.datetime(2019, 2, 3, 23, 59, 59)
    distance = 500

    # set ground criteria block
    ground = [aurorax.search.GroundCriteriaBlock(programs=["themis-asi", "rego"])]

    # set space criteria block, with a metadata filter
    expression1 = aurorax.search.MetadataFilterExpression(key="nbtrace_region", values="north polar cap", operator="=")
    metadata_filter = aurorax.search.MetadataFilter(expressions=[expression1])
    space = [aurorax.search.SpaceCriteriaBlock(programs=["swarm"], metadata_filters=metadata_filter)]

    # perform search
    s = aurorax.search.conjunctions.search(start, end, distance, ground=ground, space=space)

    # check results
    assert len(s.data) > 0
    assert isinstance(s.data[0], Conjunction) is True


@pytest.mark.search_ro
def test_with_advanced_distances(aurorax):
    # set timeframe
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 4, 23, 59, 59)

    # set criteria blocks
    ground = [
        aurorax.search.GroundCriteriaBlock(programs=["rego"]),
        aurorax.search.GroundCriteriaBlock(programs=["trex"]),
    ]
    space = [
        aurorax.search.SpaceCriteriaBlock(programs=["swarm"]),
        aurorax.search.SpaceCriteriaBlock(programs=["themis"]),
    ]

    # set advanced distances
    advanced_distances = {
        "ground1-ground2": None,
        "ground1-space1": 500,
        "ground1-space2": 500,
        "ground2-space1": 500,
        "ground2-space2": 500,
        "space1-space2": None
    }

    # perform search
    s = aurorax.search.conjunctions.search(start, end, advanced_distances, ground=ground, space=space)

    # check results
    assert len(s.data) > 0
    assert isinstance(s.data[0], Conjunction) is True


@pytest.mark.search_ro
def test_events(aurorax):
    # set timeframe and distance
    start = datetime.datetime(2008, 1, 1, 0, 0, 0)
    end = datetime.datetime(2008, 12, 31, 23, 59, 59)
    distance = 500

    # set criteria blocks
    space = [aurorax.search.SpaceCriteriaBlock(programs=["themis"])]
    events = [aurorax.search.EventsCriteriaBlock(instrument_types=["substorm onset"])]

    # do search
    s = aurorax.search.conjunctions.search(
        start=start,
        end=end,
        distance=distance,
        space=space,
        events=events,
    )

    # check results
    assert len(s.data) > 0
    assert isinstance(s.data[0], Conjunction) is True


@pytest.mark.search_ro
def test_custom(aurorax):
    # set timeframe and distance
    start = datetime.datetime(2018, 1, 1, 0, 0, 0)
    end = datetime.datetime(2018, 1, 1, 23, 59, 59)
    distance = 500

    # set criteria blocks
    space = [aurorax.search.SpaceCriteriaBlock(programs=["swarm"])]
    custom = [aurorax.search.CustomLocationsCriteriaBlock(locations=[(51.05, -114.07)])]

    # do search
    s = aurorax.search.conjunctions.search(
        start=start,
        end=end,
        distance=distance,
        space=space,
        custom_locations=custom,
    )

    # check results
    assert len(s.data) > 0
    assert isinstance(s.data[0], Conjunction) is True


@pytest.mark.search_ro
def test_response_format(aurorax):
    # set up params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 23, 59, 59)
    ground = [aurorax.search.GroundCriteriaBlock(programs=["themis-asi"], platforms=["gillam"])]
    space = [aurorax.search.SpaceCriteriaBlock(programs=["swarm", "themis"])]
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
    s = aurorax.search.conjunctions.search(
        start,
        end,
        distance,
        ground=ground,
        space=space,
        verbose=False,
        response_format=response_format,
    )

    # do checks on response data
    assert len(s.data) > 0
    assert isinstance(s.data[0], dict) is True
    for key in s.data[0].keys():
        assert key in response_format.keys()


@pytest.mark.search_ro
def test_async(aurorax):
    # set up params
    # set timeframe and distance
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 6, 59, 59)
    distance = 200

    # set criteria blocks
    ground = [aurorax.search.GroundCriteriaBlock(programs=["themis-asi"])]
    space = [aurorax.search.SpaceCriteriaBlock(programs=["swarm"])]

    # so asynchronous search
    s = aurorax.search.conjunctions.search(
        start,
        end,
        distance,
        ground=ground,
        space=space,
        return_immediately=True,
    )

    # update the status
    #
    # NOTE: this is not needed, but for coverage we include it
    s.update_status()

    # wait for the request to finish
    s.wait()

    # check for data
    #
    # NOTE: again, this is not needed, but for coverage we include it
    s.check_for_data()

    # get data
    s.get_data()

    # check results
    assert len(s.data) > 0
    assert isinstance(s.data[0], Conjunction) is True


@pytest.mark.search_ro
def test_cancel(aurorax):
    # set up params
    start = datetime.datetime(2019, 1, 1, 0, 0, 0)
    end = datetime.datetime(2019, 12, 31, 23, 59, 59)
    ground = [aurorax.search.GroundCriteriaBlock(programs=["themis-asi"])]
    space = [aurorax.search.SpaceCriteriaBlock(programs=["swarm"])]
    conjunction_types = [aurorax.search.CONJUNCTION_TYPE_SBTRACE]
    distance = 100

    # do asynchronous search
    s = aurorax.search.conjunctions.search(start,
                                           end,
                                           distance,
                                           ground=ground,
                                           space=space,
                                           conjunction_types=conjunction_types,
                                           return_immediately=True)

    # cancel request
    result = s.cancel(wait=True)

    # check to make sure it has been cancelled
    assert result == 0
