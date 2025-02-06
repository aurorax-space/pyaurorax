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


@pytest.mark.search_ro
def test_create(aurorax, capsys):
    # create expression
    expression1 = aurorax.search.MetadataFilterExpression(key="some_key", values="some value", operator="=")
    expression2 = aurorax.search.MetadataFilterExpression(key="some_key", values=["some value", "another value"], operator="in")

    # create filter
    metadata_filter1 = aurorax.search.MetadataFilter(expressions=[expression1])
    metadata_filter2 = aurorax.search.MetadataFilter(expressions=[expression1, expression2])

    # check __str__ and __repr__ for MetadataFilterExpression type
    print_str = str(expression1)
    assert print_str != ""
    assert isinstance(str(expression1), str) is True
    assert isinstance(repr(expression1), str) is True
    expression1.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # check __str__ and __repr__ for MetadataFilterExpression type
    print_str = str(expression2)
    assert print_str != ""
    assert isinstance(str(expression2), str) is True
    assert isinstance(repr(expression2), str) is True
    expression2.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # check __str__ and __repr__ for MetadataFilter type
    print_str = str(metadata_filter1)
    assert print_str != ""
    assert isinstance(str(metadata_filter1), str) is True
    assert isinstance(repr(metadata_filter1), str) is True
    metadata_filter1.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # check __str__ and __repr__ for MetadataFilter type
    print_str = str(metadata_filter2)
    assert print_str != ""
    assert isinstance(str(metadata_filter2), str) is True
    assert isinstance(repr(metadata_filter2), str) is True
    metadata_filter2.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.search_ro
def test_update(aurorax):
    # create expression
    expression1 = aurorax.search.MetadataFilterExpression(key="some_key", values="some value", operator="=")
    expression1.operator = "in"

    # create filter
    metadata_filter = aurorax.search.MetadataFilter(expressions=[expression1])
    metadata_filter.operator = "OR"

    # made it here, great!
    assert True


@pytest.mark.search_ro
def test_expression_bad_operator1(aurorax):
    # create expression
    expression = aurorax.search.MetadataFilterExpression(key="some_key", values="some value")
    with pytest.raises(ValueError) as e_info:
        expression.operator = "something-bad"
    assert "not allowed. You must use one of the following" in str(e_info)

    # create filter
    metadata_filter = aurorax.search.MetadataFilter(expressions=[aurorax.search.MetadataFilterExpression(key="some_key", values="some value")])
    with pytest.raises(ValueError) as e_info:
        metadata_filter.operator = "something-bad"
    assert "not allowed. You must use one of the following" in str(e_info)


@pytest.mark.search_ro
def test_expression_bad_operator2(aurorax):
    # create expression
    with pytest.raises(ValueError) as e_info:
        aurorax.search.MetadataFilterExpression(key="some_key", values="some value", operator="something-bad")
    assert "not allowed. You must use one of the following" in str(e_info)

    # create filter
    with pytest.raises(ValueError) as e_info:
        aurorax.search.MetadataFilter(expressions=[aurorax.search.MetadataFilterExpression(key="some_key", values="some value")],
                                      operator="something-bad")
    assert "not allowed. You must use one of the following" in str(e_info)
