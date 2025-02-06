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
from pyaurorax.search import EphemerisSearch, EphemerisData


@pytest.mark.search_ro
def test_simple(aurorax, capsys):
    s = aurorax.search.ephemeris.search(datetime.datetime(2019, 1, 1, 0, 0, 0),
                                        datetime.datetime(2019, 1, 1, 0, 9, 59),
                                        programs=["swarm"],
                                        platforms=["swarma"],
                                        instrument_types=["footprint"],
                                        verbose=True)

    # check
    assert isinstance(s.data, list) is True
    assert len(s.data) > 0
    for e in s.data:
        assert isinstance(e, EphemerisData) is True

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
def test_single_result(aurorax, capsys):
    s = aurorax.search.ephemeris.search(datetime.datetime(2019, 1, 1, 0, 0, 0),
                                        datetime.datetime(2019, 1, 1, 0, 0, 59),
                                        programs=["swarm"],
                                        platforms=["swarma"],
                                        instrument_types=["footprint"])

    # check
    assert isinstance(s.data, list) is True
    assert len(s.data) == 1
    for e in s.data:
        assert isinstance(e, EphemerisData) is True

    # check __str__ and __repr__ for EphemerisSearch type
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
    metadata_filter = aurorax.search.MetadataFilter(
        expressions=[aurorax.search.MetadataFilterExpression("nbtrace_region", "north polar cap", operator="=")])

    # perform search
    s = aurorax.search.ephemeris.search(datetime.datetime(2019, 1, 1, 0, 0, 0),
                                        datetime.datetime(2019, 1, 1, 11, 59, 59),
                                        programs=["swarm"],
                                        platforms=["swarma"],
                                        instrument_types=["footprint"],
                                        metadata_filters=metadata_filter)

    # check
    assert isinstance(s.data, list) is True
    assert len(s.data) > 0
    for e in s.data:
        assert isinstance(e, EphemerisData) is True

    # check describe function
    description = s.describe()
    assert description != ""


@pytest.mark.search_ro
def test_async(aurorax):
    s = aurorax.search.ephemeris.search(datetime.datetime(2019, 1, 1, 0, 0, 0),
                                        datetime.datetime(2019, 1, 1, 0, 9, 59),
                                        programs=["swarm"],
                                        platforms=["swarma"],
                                        instrument_types=["footprint"],
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
        assert isinstance(e, EphemerisData) is True


@pytest.mark.search_ro
def test_response_format(aurorax):
    s = aurorax.search.ephemeris.search(datetime.datetime(2019, 1, 1, 0, 0, 0),
                                        datetime.datetime(2019, 1, 1, 0, 59, 59),
                                        programs=["swarm"],
                                        platforms=["swarma"],
                                        instrument_types=["footprint"],
                                        response_format={
                                            "data_source": {
                                                "identifier": True,
                                                "program": True,
                                            },
                                            "epoch": True,
                                            "location_geo": {
                                                "lat": True,
                                                "lon": True
                                            },
                                            "metadata": True
                                        })

    # wait for data
    s.wait()
    s.get_data()

    # check
    assert isinstance(s.data, list) is True
    assert len(s.data) > 0
    for e in s.data:
        assert isinstance(e, dict) is True
        assert "nbtrace" not in e.keys()

    # check describe function
    description = s.describe()
    assert description != ""


@pytest.mark.search_ro
def test_no_data(aurorax, capsys):
    s = aurorax.search.ephemeris.search(datetime.datetime(2019, 1, 1, 16, 0, 0),
                                        datetime.datetime(2019, 1, 1, 16, 9, 59),
                                        programs=["themis-asi"],
                                        platforms=["gillam"])

    # check
    assert isinstance(s.data, list) is True
    assert len(s.data) == 0

    # check __str__ and __repr__ for EphemerisSearch type
    print_str = str(s)
    assert print_str != ""
    assert isinstance(str(s), str) is True
    assert isinstance(repr(s), str) is True
    s.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.search_ro
def test_metadata_filter_warning(aurorax):
    # set search parameters
    start = datetime.datetime(2019, 1, 1, 6, 0, 0)
    end = datetime.datetime(2019, 1, 1, 6, 11, 59)
    programs = ["swarm"]
    platforms = ["swarma"]
    instrument_types = ["footprint"]

    # set metadata filters
    metadata_filter = aurorax.search.MetadataFilter(
        expressions=[aurorax.search.MetadataFilterExpression("nbtrace_region", "north polar cap", operator="=")])

    # create object
    with warnings.catch_warnings(record=True) as w:
        _ = aurorax.search.ephemeris.search(
            start,
            end,
            programs=programs,
            platforms=platforms,
            instrument_types=instrument_types,
            metadata_filters=metadata_filter,
            metadata_filters_logical_operator="AND",
        )
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "Supplying a MetadataFilter object in addition to the metadata_filters_logical_operator parameter is redundant." in str(w[-1].message)


@pytest.mark.search_ro
def test_cancel(aurorax):
    start_dt = datetime.datetime(2018, 1, 1, 0, 0, 0)
    end_dt = datetime.datetime(2018, 1, 31, 23, 59, 59)
    programs = ["themis"]

    # do search
    s = EphemerisSearch(aurorax, start=start_dt, end=end_dt, programs=programs)
    s.execute()

    # cancel it
    result = s.cancel(wait=True)

    # check it was cancelled
    assert result == 0


@pytest.mark.search_ro
def test_cancel_no_wait(aurorax):
    start_dt = datetime.datetime(2018, 1, 1, 0, 0, 0)
    end_dt = datetime.datetime(2018, 1, 31, 23, 59, 59)
    programs = ["themis"]

    # do search
    s = EphemerisSearch(aurorax, start=start_dt, end=end_dt, programs=programs)
    s.execute()

    # cancel it
    s.cancel(wait=False)
