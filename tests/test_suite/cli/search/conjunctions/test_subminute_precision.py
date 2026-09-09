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

import os
import json
import pytest
import pyaurorax
from copy import deepcopy
from pyaurorax.cli.cli import cli
from pyaurorax.cli.templates import CONJUNCTION_SEARCH_TEMPLATE
from pyaurorax.cli.search.conjunctions.commands import __create_search_object_from_query as create_search_object_from_query


@pytest.mark.cli
def test_template_contains_field():
    assert CONJUNCTION_SEARCH_TEMPLATE["subminute_precision"] is False


@pytest.mark.cli
@pytest.mark.parametrize("query_extras,expected", [
    ({}, None),
    ({"subminute_precision": True}, True),
    ({"subminute_precision": False}, False),
    ({"epoch_search_precision": 60}, False),
    ({"epoch_search_precision": 30}, True),
    ({"epoch_search_precision": None}, None),
    ({"epoch_search_precision": 60, "subminute_precision": True}, True),
])
def test_create_search_object_from_query(conjunction_search_dict, query_extras, expected):
    # this is the path used by 'search_resubmit', where the query comes back from the API
    q = deepcopy(conjunction_search_dict)
    q.update(query_extras)
    aurorax = pyaurorax.PyAuroraX()

    s = create_search_object_from_query(aurorax, q)

    assert s.subminute_precision is expected
    assert "epoch_search_precision" not in s.query
    if (expected is None):
        assert "subminute_precision" not in s.query
    else:
        assert s.query["subminute_precision"] is expected


@pytest.mark.cli
@pytest.mark.parametrize("field,value", [("subminute_precision", True), ("epoch_search_precision", 30)])
def test_search_from_query_file(cli_runner, api_url, conjunction_search_dict, tmp_path, field, value):
    # write out a query file containing the precision field, and make sure the search runs
    q = deepcopy(conjunction_search_dict)
    q[field] = value
    infile = str(tmp_path / "query.json")
    with open(infile, 'w', encoding="utf-8") as fp:
        json.dump(q, fp)

    # NOTE: an outfile is supplied so that the results don't get written into the current directory
    outfile = str(tmp_path / "data.json")
    result = cli_runner.invoke(
        cli, "--api-base-url=%s search conjunctions search %s --poll-interval=1 --quiet --outfile=%s" % (api_url, infile, outfile))
    assert result.exit_code == 0
    assert os.path.exists(outfile) is True
