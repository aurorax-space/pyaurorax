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
from pyaurorax.search import DataProductSearch, DataProductData


@pytest.mark.search_ro
def test_simple(aurorax, capsys):
    # do search
    s = aurorax.search.data_products.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                            datetime.datetime(2020, 1, 2, 23, 59, 59),
                                            programs=["auroramax"],
                                            data_product_types=["keogram"],
                                            verbose=True)
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # check
    assert isinstance(s.data, list) is True
    assert len(s.data) > 0
    for dp in s.data:
        assert isinstance(dp, DataProductData) is True

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
def test_single_result(aurorax, capsys):
    # set metadata filters
    metadata_filters = aurorax.search.MetadataFilter(
        expressions=[aurorax.search.MetadataFilterExpression("keogram_type", "daily_hires", operator="=")])

    # perform search
    s = aurorax.search.data_products.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                            datetime.datetime(2020, 1, 1, 23, 59, 59),
                                            programs=["auroramax"],
                                            data_product_types=["keogram"],
                                            metadata_filters=metadata_filters,
                                            verbose=False)

    # check
    assert isinstance(s.data, list) is True
    assert len(s.data) == 1
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


@pytest.mark.search_ro
def test_metadata_filters(aurorax):
    # set metadata filters
    metadata_filters = aurorax.search.MetadataFilter(
        expressions=[
            aurorax.search.MetadataFilterExpression("keogram_type", "daily_hires", operator="="),
            aurorax.search.MetadataFilterExpression("movie_type", "real-time daily", operator="="),
        ],
        operator="OR",
    )

    # perform search
    s = aurorax.search.data_products.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                            datetime.datetime(2020, 1, 2, 23, 59, 59),
                                            programs=["auroramax"],
                                            data_product_types=["keogram", "movie"],
                                            metadata_filters=metadata_filters)

    # check
    assert isinstance(s.data, list) is True
    assert len(s.data) > 0
    for dp in s.data:
        assert isinstance(dp, DataProductData) is True

    # check describe function
    description = s.describe()
    assert description != ""


@pytest.mark.search_ro
def test_async(aurorax):
    s = aurorax.search.data_products.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                            datetime.datetime(2020, 1, 2, 23, 59, 59),
                                            programs=["auroramax"],
                                            return_immediately=True)

    # get data
    #
    # NOTE: this is not supposed to be done at this point, but for coverage we
    # include it
    s.get_data()

    # update the status
    #
    # NOTE: this is not needed, but for coverage we include it
    s.update_status()

    # wait for the request to finish
    s.wait()

    # check for data
    #
    # NOTE: again, this is not needed, but for coverage we include it
    s.check_for_data()

    # get data
    s.get_data()

    # check
    assert isinstance(s.data, list) is True
    assert len(s.data) > 0
    for e in s.data:
        assert isinstance(e, DataProductData) is True


@pytest.mark.search_ro
def test_response_format(aurorax):
    # do search
    s = aurorax.search.data_products.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                            datetime.datetime(2020, 1, 2, 23, 59, 59),
                                            programs=["auroramax"],
                                            response_format={
                                                "start": True,
                                                "end": True,
                                                "data_source": {
                                                    "identifier": True,
                                                    "program": True,
                                                    "platform": True,
                                                    "instrument_type": True,
                                                },
                                                "url": True,
                                                "data_product_type": True,
                                            })

    # wait for data
    s.wait()
    s.get_data()

    # check
    assert isinstance(s.data, list) is True
    assert len(s.data) > 0
    for e in s.data:
        assert isinstance(e, dict) is True
        assert "metadata" not in e.keys()

    # check describe function
    description = s.describe()
    assert description != ""


@pytest.mark.search_ro
def test_no_data(aurorax, capsys):
    s = aurorax.search.data_products.search(
        datetime.datetime(1990, 1, 1, 0, 0, 0),
        datetime.datetime(1990, 1, 2, 23, 59, 59),
        programs=["auroramax"],
    )

    # check
    assert isinstance(s.data, list) is True
    assert len(s.data) == 0

    # check __str__ and __repr__ for DataProductSearch type
    print_str = str(s)
    assert print_str != ""
    assert isinstance(str(s), str) is True
    assert isinstance(repr(s), str) is True
    s.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.search_ro
def test_metadata_filter_warning(aurorax):
    # set metadata filters
    metadata_filters = aurorax.search.MetadataFilter(
        expressions=[
            aurorax.search.MetadataFilterExpression("keogram_type", "daily_hires", operator="="),
            aurorax.search.MetadataFilterExpression("movie_type", "real-time daily", operator="="),
        ],
        operator="OR",
    )

    # create object
    with warnings.catch_warnings(record=True) as w:
        _ = aurorax.search.data_products.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                                datetime.datetime(2020, 1, 2, 23, 59, 59),
                                                programs=["auroramax"],
                                                data_product_types=["keogram", "movie"],
                                                metadata_filters=metadata_filters,
                                                metadata_filters_logical_operator="OR")
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "Supplying a MetadataFilter object in addition to the metadata_filters_logical_operator parameter is redundant." in str(w[-1].message)


@pytest.mark.search_ro
def test_cancel(aurorax):
    start_dt = datetime.datetime(2018, 1, 1, 0, 0, 0)
    end_dt = datetime.datetime(2021, 12, 31, 23, 59, 59)
    programs = ["themis"]

    # do search
    s = DataProductSearch(aurorax, start=start_dt, end=end_dt, programs=programs)
    s.execute()

    # cancel it
    result = s.cancel(wait=True)

    # check it was cancelled
    assert result == 0
