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
import pyaurorax
from copy import deepcopy
from pyaurorax.search import ConjunctionSearch, GroundCriteriaBlock, SpaceCriteriaBlock


def __create_search_object(aurorax, **kwargs):
    return ConjunctionSearch(
        aurorax,
        datetime.datetime(2020, 1, 1, 0, 0, 0),
        datetime.datetime(2020, 1, 1, 6, 59, 59),
        distance=200,
        ground=[GroundCriteriaBlock(programs=["themis-asi"])],
        space=[SpaceCriteriaBlock(programs=["swarm"])],
        **kwargs,
    )


@pytest.mark.search_ro
def test_default_omitted_from_query(aurorax):
    # the field should be left out of the query entirely when it wasn't set, so that
    # the API applies its own default of one-minute precision
    s = __create_search_object(aurorax)
    assert s.subminute_precision is None
    assert "subminute_precision" not in s.query
    assert "epoch_search_precision" not in s.query


@pytest.mark.search_ro
@pytest.mark.parametrize("value", [True, False])
def test_set_in_query(aurorax, value):
    s = __create_search_object(aurorax, subminute_precision=value)
    assert s.subminute_precision is value
    assert s.query["subminute_precision"] is value


@pytest.mark.search_ro
@pytest.mark.parametrize("value", [None, True, False])
def test_describe(aurorax, value):
    s = __create_search_object(aurorax, subminute_precision=value)
    describe_str = aurorax.search.conjunctions.describe(s)
    assert describe_str is not None and describe_str != ""
    if (value is True):
        assert "sub-minute precision" in describe_str
    else:
        assert "one-minute precision" in describe_str


@pytest.mark.search_ro
def test_search(aurorax):
    s = aurorax.search.conjunctions.search(
        datetime.datetime(2019, 1, 1, 0, 0, 0),
        datetime.datetime(2019, 1, 1, 23, 59, 59),
        distance=500,
        ground=[GroundCriteriaBlock(programs=["themis-asi"])],
        space=[SpaceCriteriaBlock(programs=["swarm"])],
        subminute_precision=True,
    )
    assert s.query["subminute_precision"] is True
    assert len(s.data) > 0


@pytest.mark.search_ro
@pytest.mark.parametrize("epoch_search_precision,expected", [(60, False), (59, True), (30, True), (1, True), (None, None)])
def test_raw_query_legacy_field(aurorax, conjunction_search_dict, epoch_search_precision, expected):
    # a query containing the deprecated field should be translated instead of rejected
    query = deepcopy(conjunction_search_dict)
    query["epoch_search_precision"] = epoch_search_precision
    s = aurorax.search.conjunctions.search_from_raw_query(query, return_immediately=True)
    assert s.subminute_precision is expected
    assert "epoch_search_precision" not in s.query
    if (expected is None):
        assert "subminute_precision" not in s.query
    else:
        assert s.query["subminute_precision"] is expected


@pytest.mark.search_ro
def test_raw_query_new_field_takes_precedence(aurorax, conjunction_search_dict):
    query = deepcopy(conjunction_search_dict)
    query["epoch_search_precision"] = 60
    query["subminute_precision"] = True
    s = aurorax.search.conjunctions.search_from_raw_query(query, return_immediately=True)
    assert s.query["subminute_precision"] is True


@pytest.mark.search_ro
@pytest.mark.parametrize("value", [0, 61, 120, "30", True])
def test_raw_query_legacy_field_errors(aurorax, conjunction_search_dict, value):
    query = deepcopy(conjunction_search_dict)
    query["epoch_search_precision"] = value
    with pytest.raises(pyaurorax.AuroraXError) as e_info:
        aurorax.search.conjunctions.search_from_raw_query(query)
    assert "The 'epoch_search_precision' parameter must be an integer between 1 and 60" in str(e_info)
