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
from pyaurorax.search import EphemerisSearch


@pytest.mark.search_ro
def test_simple(aurorax, capsys):
    # set vars
    start_dt = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end_dt = datetime.datetime(2020, 1, 10, 0, 0, 0)
    programs = ["swarm"]
    platforms = ["swarma"]
    instrument_types = ["footprint"]

    # create object
    s = EphemerisSearch(
        aurorax,
        start_dt,
        end_dt,
        programs=programs,
        platforms=platforms,
        instrument_types=instrument_types,
    )

    # check
    assert isinstance(s, EphemerisSearch) is True
    assert s.start == start_dt
    assert s.end == end_dt
    assert s.programs == programs
    assert s.platforms == platforms
    assert s.instrument_types == instrument_types
    assert s.query != ""

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
    print(description)
    assert description != ""


@pytest.mark.search_ro
def test_with_metadata_filters(aurorax, capsys):
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
    s = EphemerisSearch(
        aurorax,
        start,
        end,
        programs=programs,
        platforms=platforms,
        instrument_types=instrument_types,
        metadata_filters=metadata_filter,
    )

    # check
    assert isinstance(s, EphemerisSearch) is True
    assert s.start == start
    assert s.end == end
    assert s.programs == programs
    assert s.platforms == platforms
    assert s.instrument_types == instrument_types

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
    print(description)
    assert description != ""


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
        _ = EphemerisSearch(
            aurorax,
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
