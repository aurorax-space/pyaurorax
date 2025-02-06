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
from pyaurorax.search.sources import DataSource, FORMAT_FULL_RECORD


@pytest.mark.search_ro
def test_simple(aurorax):
    # get sources
    sources = aurorax.search.sources.search(programs=["swarm"], format=FORMAT_FULL_RECORD, include_stats=True)

    # check count and type
    assert len(sources) == 3
    for s in sources:
        assert isinstance(s, DataSource) is True


@pytest.mark.search_ro
def test_no_results(aurorax):
    # get sources
    sources = aurorax.search.sources.search(programs=["something-not-existing"], format=FORMAT_FULL_RECORD, include_stats=True)

    # check count and type
    assert len(sources) == 0
    for s in sources:
        assert isinstance(s, DataSource) is True
