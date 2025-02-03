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
from pyaurorax.search import FORMAT_IDENTIFIER_ONLY


@pytest.mark.search_ro
def test_validate_schema(aurorax):
    source = aurorax.search.sources.get_using_filters(program="swarm", platform="swarma", instrument_type="footprint")
    schema = aurorax.search.metadata.get_ephemeris_schema(source[0].identifier)

    # create an example metadata dictionary
    metadata = {
        "nbtrace_region": "north cleft",
        "sbtrace_region": "south auroral oval",
        "radial_distance": 150.25,
        "radial_trace_region": "low latitude",
        "spacecraft_region": "nightside magnetosheath",
        "state": "definitive",
        "tii_on": True,
        "tii_quality_vixh": 0,
        "tii_quality_vixv": 1,
        "tii_quality_viy": 2,
        "tii_quality_viz": 3
    }

    # validate
    assert aurorax.search.metadata.validate(schema, metadata)


@pytest.mark.search_ro
def test_get_ephemeris_metadata_schema(aurorax):
    # set parameters
    program = "swarm"
    platform = "swarma"
    instrument_type = "footprint"

    # get identifier
    data_source = aurorax.search.sources.get(program, platform, instrument_type, "identifier_only")

    # get schema
    schema = aurorax.search.metadata.get_ephemeris_schema(data_source.identifier)

    # check
    assert isinstance(schema, list) is True


@pytest.mark.search_ro
def test_get_data_product_metadata_schema(aurorax):
    # set parameters
    program = "themis-asi"
    platform = "gillam"
    instrument_type = "panchromatic ASI"

    # get identifier
    data_source = aurorax.search.sources.get(program, platform, instrument_type, format=FORMAT_IDENTIFIER_ONLY)

    # get schema
    schema = aurorax.search.metadata.get_data_products_schema(data_source.identifier)

    # check
    assert isinstance(schema, list) is True
