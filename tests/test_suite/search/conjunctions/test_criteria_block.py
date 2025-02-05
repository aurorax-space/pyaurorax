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
from pyaurorax.search import (
    GroundCriteriaBlock,
    SpaceCriteriaBlock,
    EventsCriteriaBlock,
    CustomLocationsCriteriaBlock,
    MetadataFilter,
    MetadataFilterExpression,
)


@pytest.mark.search_ro
def test_ground(capsys):
    # create criteria block
    cb = GroundCriteriaBlock(programs=["themis-asi"])

    # check __str__ and __repr__ for criteria block type
    print_str = str(cb)
    assert print_str != ""
    assert isinstance(str(cb), str) is True
    assert isinstance(repr(cb), str) is True
    cb.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.search_ro
def test_ground_metadata_filters(capsys):
    # create criteria block
    expr1 = MetadataFilterExpression(key="nbtrace_region", values="north polar cap", operator="=")
    expr2 = MetadataFilterExpression(key="nbtrace_region", values="north polar cap", operator="=")
    expr3 = MetadataFilterExpression(key="nbtrace_region", values="north polar cap", operator="=")
    expr4 = MetadataFilterExpression(key="nbtrace_region", values="north polar cap", operator="=")
    metadata_filter = MetadataFilter(expressions=[expr1, expr2, expr3, expr4])
    cb = GroundCriteriaBlock(programs=["themis-asi"], metadata_filters=metadata_filter)

    # check __str__ and __repr__ for criteria block type
    print_str = str(cb)
    assert print_str != ""
    assert isinstance(str(cb), str) is True
    assert isinstance(repr(cb), str) is True
    cb.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.search_ro
def test_space(capsys):
    # create criteria block
    cb = SpaceCriteriaBlock(programs=["themis-asi"])

    # check __str__ and __repr__ for criteria block type
    print_str = str(cb)
    assert print_str != ""
    assert isinstance(str(cb), str) is True
    assert isinstance(repr(cb), str) is True
    cb.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.search_ro
def test_events(capsys):
    # create criteria block
    cb = EventsCriteriaBlock(platforms=["something"])

    # check __str__ and __repr__ for criteria block type
    print_str = str(cb)
    assert print_str != ""
    assert isinstance(str(cb), str) is True
    assert isinstance(repr(cb), str) is True
    cb.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.search_ro
def test_custom(capsys):
    # create criteria block
    cb = CustomLocationsCriteriaBlock(locations=[(51, 51)])

    # check __str__ and __repr__ for criteria block type
    print_str = str(cb)
    assert print_str != ""
    assert isinstance(str(cb), str) is True
    assert isinstance(repr(cb), str) is True
    cb.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""
