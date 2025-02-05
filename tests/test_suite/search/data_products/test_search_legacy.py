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
from pyaurorax.search import DataProductData, DATA_PRODUCT_TYPE_MOVIE, DATA_PRODUCT_TYPE_KEOGRAM


@pytest.mark.search_ro
def test_metadata_filters(aurorax, capsys):
    metadata_filters = [{
        "key": "keogram_type",
        "operator": "=",
        "values": ["daily_hires"]
    }, {
        "key": "movie_type",
        "operator": "=",
        "values": ["real-time daily"]
    }]
    s = aurorax.search.data_products.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                            datetime.datetime(2020, 1, 2, 23, 59, 59),
                                            programs=["auroramax"],
                                            data_product_types=[DATA_PRODUCT_TYPE_KEOGRAM, DATA_PRODUCT_TYPE_MOVIE],
                                            metadata_filters=metadata_filters,
                                            verbose=False,
                                            metadata_filters_logical_operator="OR")

    # check
    assert isinstance(s.data, list) is True
    assert len(s.data) > 0
    for e in s.data:
        assert isinstance(e, DataProductData) is True

    # check __str__ and __repr__ for DataProductSearch type
    print_str = str(s)
    assert print_str != ""
    assert isinstance(str(s), str) is True
    assert isinstance(repr(s), str) is True
    s.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # check describe function
    description = s.describe()
    assert description != ""

    # deeper check on results
    result_filter = list(
        filter(
            lambda dp: (dp.data_product_type == DATA_PRODUCT_TYPE_MOVIE and dp.metadata["movie_type"] == "real-time daily") or
            (dp.data_product_type == DATA_PRODUCT_TYPE_KEOGRAM and dp.metadata["keogram_type"] == "daily_hires"), s.data))
    assert len(s.data) == len(result_filter)
