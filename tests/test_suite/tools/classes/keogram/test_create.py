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
from pyaurorax.tools import Keogram


@pytest.mark.tools
def test_simple(at, themis_keogram_data, capsys):
    # create the keogram object
    data = themis_keogram_data["raw_data"].data
    timestamp = themis_keogram_data["raw_data"].timestamp
    keogram = at.keogram.create(data, timestamp)
    assert isinstance(keogram, Keogram) is True
    assert keogram.data.shape[-1] == data.shape[-1]

    # check __str__ and __repr__ for Keogram type
    print_str = str(keogram)
    assert print_str != ""
    assert isinstance(str(keogram), str) is True
    assert isinstance(repr(keogram), str) is True
    keogram.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""
