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
from pyaurorax.search.sources import DataSource, SOURCE_TYPE_GROUND


@pytest.mark.search_rw
def test_simple(aurorax):
    # set values
    idenifier = 403
    program = "test-program"
    platform = "test-platform"
    instrument_type = "testing::test_delete_source"
    source_type = SOURCE_TYPE_GROUND
    display_name = instrument_type

    # create the source
    ds_to_create = DataSource(
        identifier=idenifier,
        program=program,
        platform=platform,
        instrument_type=instrument_type,
        source_type=source_type,
        display_name=display_name,
    )
    ds_created = aurorax.search.sources.add(ds_to_create)

    # delete the source
    delete_result = aurorax.search.sources.delete(ds_created.identifier)

    # check it successfully deleted
    assert delete_result == 0
