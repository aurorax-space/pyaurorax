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
from pyaurorax.search.sources import DataSource


@pytest.mark.search_ro
def test_simple(aurorax, capsys):
    # get sources
    sources = aurorax.search.sources.list()

    # check count and type
    assert len(sources) > 1
    for s in sources:
        assert isinstance(s, DataSource) is True

        # check __str__ and __repr__ for DataSource type
        print_str = str(s)
        assert print_str != ""
        assert isinstance(str(s), str) is True
        assert isinstance(repr(s), str) is True
        s.pretty_print()
        captured_stdout = capsys.readouterr().out
        assert captured_stdout != ""


@pytest.mark.search_ro
def test_with_stats(aurorax, capsys):
    # get sources
    sources = aurorax.search.sources.list(include_stats=True)

    # check count and type
    assert len(sources) > 1
    for s in sources:
        assert isinstance(s, DataSource) is True

        # check __str__ and __repr__ for DataSource type
        print_str = str(s)
        assert print_str != ""
        assert isinstance(str(s), str) is True
        assert isinstance(repr(s), str) is True
        s.pretty_print()
        captured_stdout = capsys.readouterr().out
        assert captured_stdout != ""

        # check __str__ and __repr__ for DataSourceStats type
        print_str = str(s.stats)
        assert print_str != ""
        assert isinstance(str(s.stats), str) is True
        assert isinstance(repr(s.stats), str) is True
        s.stats.pretty_print()
        captured_stdout = capsys.readouterr().out
        assert captured_stdout != ""


@pytest.mark.search_ro
def test_simple_table(aurorax, capsys):
    # get sources
    aurorax.search.sources.list_in_table()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.search_ro
def test_table_limit(aurorax, capsys):
    # get sources
    aurorax.search.sources.list_in_table(limit=10)
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""
