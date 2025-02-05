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
from pyaurorax.search import DataSource, DataProductData, DATA_PRODUCT_TYPE_KEOGRAM


@pytest.mark.search_ro
def test_create_data_product_object(aurorax):
    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    start_dt = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end_dt = start_dt.replace(hour=23, minute=59, second=59)
    data_product_type = DATA_PRODUCT_TYPE_KEOGRAM
    url = "testing_url.jpg"
    metadata = {}

    # get identifier
    data_source = aurorax.search.sources.get(program, platform, instrument_type)

    # create DataProduct object
    d = DataProductData(
        data_source=data_source,
        data_product_type=data_product_type,
        url=url,
        start=start_dt,
        end=end_dt,
        metadata=metadata,
    )

    assert isinstance(d, DataProductData) is True
    assert isinstance(d.data_source, DataSource) is True
    assert d.data_source.program == program
    assert d.data_source.platform == platform
    assert d.data_source.instrument_type == instrument_type
