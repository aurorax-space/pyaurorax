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
import json
import pyaurorax
from copy import deepcopy
from pyaurorax.search import Conjunction, ConjunctionSearch


@pytest.mark.search_ro
def test_simple_dict(aurorax, conjunction_search_dict):
    # check dict format
    s = aurorax.search.conjunctions.search_from_raw_query(conjunction_search_dict)
    assert len(s.data) > 0
    assert isinstance(s.data[0], Conjunction) is True


@pytest.mark.search_ro
def test_simple_str(aurorax, conjunction_search_dict):
    # check string format
    json_str = json.dumps(conjunction_search_dict)
    s = aurorax.search.conjunctions.search_from_raw_query(json_str)
    assert len(s.data) > 0
    assert isinstance(s.data[0], Conjunction) is True


@pytest.mark.search_ro
def test_simple_verbose(aurorax, conjunction_search_dict, capsys):
    # check string format
    s = aurorax.search.conjunctions.search_from_raw_query(conjunction_search_dict, verbose=True)
    assert len(s.data) > 0
    assert isinstance(s.data[0], Conjunction) is True
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.search_ro
def test_simple_return_immediately(aurorax, conjunction_search_dict):
    # check string format
    s = aurorax.search.conjunctions.search_from_raw_query(conjunction_search_dict, return_immediately=True)
    assert isinstance(s, ConjunctionSearch) is True
    assert s.executed is True


@pytest.mark.search_ro
def test_query_parameter_errors(aurorax, conjunction_search_dict):
    # remove start time
    query = deepcopy(conjunction_search_dict)
    del query["start"]
    with pytest.raises(pyaurorax.AuroraXError) as e_info:
        aurorax.search.conjunctions.search_from_raw_query(query)
    assert "The 'start' parameter is missing from the query" in str(e_info)

    # remove end time
    query = deepcopy(conjunction_search_dict)
    del query["end"]
    with pytest.raises(pyaurorax.AuroraXError) as e_info:
        aurorax.search.conjunctions.search_from_raw_query(query)
    assert "The 'end' parameter is missing from the query" in str(e_info)

    # remove max distances
    query = deepcopy(conjunction_search_dict)
    del query["max_distances"]
    with pytest.raises(pyaurorax.AuroraXError) as e_info:
        aurorax.search.conjunctions.search_from_raw_query(query)
    assert "The 'max_distances' parameter is missing from the query" in str(e_info)


@pytest.mark.search_ro
def test_custom_locations(aurorax):
    # set query
    query = {
        "start": "2021-01-01T00:00:00.000Z",
        "end": "2021-01-03T23:59:59.000Z",
        "conjunction_types": ["nbtrace"],
        "space": [{
            "programs": ["swarm"],
            "platforms": [],
            "instrument_types": ["footprint"],
            "ephemeris_metadata_filters": {},
            "hemisphere": ["northern"]
        }],
        "adhoc": [{
            "locations": [{
                "lat": 51.05,
                "lon": -114.07
            }]
        }],
        "max_distances": {
            "space1-adhoc1": 400
        }
    }

    # do search
    s = aurorax.search.conjunctions.search_from_raw_query(query)
    assert len(s.data) > 0
    assert isinstance(s.data[0], Conjunction) is True
