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
import pyaurorax


@pytest.mark.search_ro
def test_simple(aurorax, conjunction_search_obj):
    # get describe string
    describe_str = aurorax.search.conjunctions.describe(conjunction_search_obj)

    # test response
    assert describe_str is not None and describe_str != ""


@pytest.mark.search_ro
def test_search_object(aurorax, conjunction_search_obj):
    # get describe string
    describe_str = aurorax.search.conjunctions.describe(search_obj=conjunction_search_obj)

    # test response
    assert describe_str is not None and describe_str != ""


@pytest.mark.search_ro
def test_search_dict(aurorax, conjunction_search_dict):
    # get describe string
    describe_str = aurorax.search.conjunctions.describe(query_dict=conjunction_search_dict)

    # test response
    assert describe_str is not None and describe_str != ""


@pytest.mark.search_ro
def test_bad(aurorax):
    with pytest.raises(pyaurorax.AuroraXError) as e_info:
        aurorax.search.conjunctions.describe()
    assert "One of 'search_obj' or 'query_dict' must be supplied" in str(e_info)
