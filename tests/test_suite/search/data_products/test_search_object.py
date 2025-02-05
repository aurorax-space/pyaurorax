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
import warnings
from pyaurorax.search import DataProductSearch, DATA_PRODUCT_TYPE_KEOGRAM, DATA_PRODUCT_TYPE_MOVIE


@pytest.mark.search_ro
def test_simple(aurorax, capsys):
    # set vars
    start_dt = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end_dt = datetime.datetime(2020, 1, 1, 23, 59, 59)
    programs = ["auroramax"]

    # create search object
    s = DataProductSearch(aurorax, start_dt, end_dt, programs=programs)

    # check
    assert isinstance(s, DataProductSearch) is True
    assert s.start == start_dt
    assert s.end == end_dt
    assert s.programs == programs
    assert s.query != ""

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


@pytest.mark.search_ro
def test_with_metadata_filters(aurorax, capsys):
    # set search parameters
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 2, 23, 59, 59)
    programs = ["auroramax"]

    # set metadata filters
    metadata_filter = aurorax.search.MetadataFilter(
        expressions=[
            aurorax.search.MetadataFilterExpression("keogram_type", "daily_hires", operator="="),
            aurorax.search.MetadataFilterExpression("movie_type", "real-time daily", operator="=")
        ],
        operator="OR",
    )

    # create object
    s = DataProductSearch(
        aurorax,
        start,
        end,
        programs=programs,
        data_product_types=["keogram", "movie"],
        metadata_filters=metadata_filter,
    )

    # check
    assert isinstance(s, DataProductSearch) is True

    # deeper check on data
    for dp in s.data:
        if (dp.data_product_type == DATA_PRODUCT_TYPE_MOVIE):
            assert dp.metadata["movie_type"] == "real-time daily"  # type: ignore
        elif (dp.data_product_type == DATA_PRODUCT_TYPE_KEOGRAM):
            assert dp.metadata["keogram_type"] == "daily_hires"  # type: ignore
        else:
            raise AssertionError("Unexpected data product record included in search results")

    # check __str__ and __repr__ for EphemerisSearch type
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


@pytest.mark.search_ro
def test_create_response_format_template(aurorax):
    response_format = aurorax.search.data_products.create_response_format_template()
    assert isinstance(response_format, dict) is True


@pytest.mark.search_ro
def test_metadata_filter_warning(aurorax):
    # set search parameters
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 2, 23, 59, 59)
    programs = ["auroramax"]

    # set metadata filters
    metadata_filter = aurorax.search.MetadataFilter(
        expressions=[
            aurorax.search.MetadataFilterExpression("keogram_type", "daily_hires", operator="="),
            aurorax.search.MetadataFilterExpression("movie_type", "real-time daily", operator="=")
        ],
        operator="OR",
    )

    # create object
    with warnings.catch_warnings(record=True) as w:
        _ = DataProductSearch(
            aurorax,
            start,
            end,
            programs=programs,
            metadata_filters=metadata_filter,
            metadata_filters_logical_operator="OR",
        )
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "Supplying a MetadataFilter object in addition to the metadata_filters_logical_operator parameter is redundant." in str(w[-1].message)
