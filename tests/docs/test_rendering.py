# Copyright 2026 University of Calgary
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

"""Check pdoc's rendered sections without API credentials or scientific test data."""

import ast
from pathlib import Path
from xml.etree import ElementTree

import pytest
from pdoc.html_helpers import to_html


@pytest.mark.parametrize("section", ["Args", "Attributes", "Returns", "Yields", "Raises", "Warns"])
def test_google_sections(section):
    entry = "value (int)" if section in ("Args", "Attributes") else "int"
    html = to_html(f"Summary.\n\n{section}:\n    {entry}: A documented value.\n")
    assert "-----=" not in html
    root = ElementTree.fromstring(f"<div>{html.replace('&ensp;', '&#8194;')}</div>")
    assert root.findtext("h2") == section
    assert root.findtext("dl/dd") == "A documented value."
    assert root.find("dl/dt/code") is not None or root.find("dl/dt/strong/code") is not None


def test_location_docstring():
    # Read the actual source without importing the package's scientific dependencies.
    source = Path(__file__).resolve().parents[2] / "pyaurorax/search/location.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))
    location = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "Location")
    docstring = ast.get_docstring(location)
    assert docstring is not None
    html = to_html(docstring)
    assert "-----=" not in html
    root = ElementTree.fromstring(f"<div>{html.replace('&ensp;', '&#8194;')}</div>")
    assert [heading.text for heading in root.findall("h2")] == ["Attributes", "Raises"]
    assert [name.text for name in root.findall("dl/dt/strong/code")] == ["lat", "lon"]
    assert [code.text for code in root.findall("dl/dt/code")] == ["float", "float", "ValueError"]
    assert [description.text for description in root.findall("dl/dd")][:2] == ["latitude value", "longitude value"]
