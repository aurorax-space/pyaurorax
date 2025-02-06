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
from pyaurorax.search.sources import DataSource, DataSourceStatistics, FORMAT_FULL_RECORD, FORMAT_IDENTIFIER_ONLY


@pytest.mark.search_ro
def test_get_single_source(aurorax):
    source = aurorax.search.sources.get("swarm", "swarma", "footprint", format=FORMAT_FULL_RECORD)
    assert isinstance(source, DataSource) is True


@pytest.mark.search_ro
def test_get_source_by_filter(aurorax):
    # get sources
    sources = aurorax.search.sources.get_using_filters(program="swarm", instrument_type="footprint", format=FORMAT_FULL_RECORD)

    # check count and type
    assert len(sources) == 3
    for s in sources:
        assert isinstance(s, DataSource) is True


@pytest.mark.search_ro
def test_get_source_by_id(aurorax):
    source = aurorax.search.sources.get("swarm", "swarma", "footprint", format=FORMAT_IDENTIFIER_ONLY)
    source_using_id = aurorax.search.sources.get_using_identifier(source.identifier, format=FORMAT_FULL_RECORD)
    assert isinstance(source_using_id, DataSource) is True
    assert source.identifier == source_using_id.identifier


@pytest.mark.search_ro
def test_get_source_not_found(aurorax):
    with pytest.raises(pyaurorax.AuroraXNotFoundError):
        aurorax.search.sources.get("definitely", "doesnt", "exist")


@pytest.mark.search_ro
def test_get_source_using_filters_not_found(aurorax):
    sources = aurorax.search.sources.get_using_filters("definitely", "doesnt", "exist")
    assert len(sources) == 0


@pytest.mark.search_ro
def test_get_source_using_identifier_not_found(aurorax):
    identifier = 12345678
    with pytest.raises(pyaurorax.AuroraXAPIError) as e_info:
        aurorax.search.sources.get_using_identifier(identifier)
    assert "No Data Source record found in AuroraX for identifier %d" % (identifier) in str(e_info)


@pytest.mark.search_ro
def test_get_source_stats(aurorax):
    # get data source with stats
    program = "themis"
    platform = "themise"
    instrument_type = "footprint"
    sources = aurorax.search.sources.get_using_filters(
        program=program,
        platform=platform,
        instrument_type=instrument_type,
        include_stats=True,
    )

    # check types
    for source in sources:
        assert isinstance(source, DataSource) is True
        assert source.stats is not None
        assert isinstance(source.stats, DataSourceStatistics) is True
