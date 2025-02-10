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

import os
import random
import string
import warnings
import pytest


@pytest.mark.search_ro
def test_get_url(aurorax, conjunction_search_obj):
    url = aurorax.search.conjunctions.swarmaurora.get_url(conjunction_search_obj)
    assert url != ""


@pytest.mark.search_ro
def test_open_in_browser(aurorax, conjunction_search_obj):
    with warnings.catch_warnings(record=True):
        aurorax.search.conjunctions.swarmaurora.open_in_browser(conjunction_search_obj)
    assert True


@pytest.mark.search_ro
def test_open_in_browser_bad_choice(aurorax, conjunction_search_obj):
    with pytest.raises(ValueError) as e_info:
        aurorax.search.conjunctions.swarmaurora.open_in_browser(conjunction_search_obj, browser="some-bad-choice")
    assert "Error: selected browser" in str(e_info) and "not found, please try another" in str(e_info)


@pytest.mark.search_ro
def test_create_custom_import_file_simple(aurorax, conjunction_search_obj):
    output_filename = aurorax.search.conjunctions.swarmaurora.create_custom_import_file(conjunction_search_obj)
    assert isinstance(output_filename, str) is True
    assert os.path.exists(output_filename) is True
    os.remove(output_filename)


@pytest.mark.search_ro
def test_create_custom_import_file_with_filename(aurorax, conjunction_search_obj):
    output_filename = "/tmp/pyaurorax_testing_%s_swarmaurora_custom.json" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    aurorax.search.conjunctions.swarmaurora.create_custom_import_file(conjunction_search_obj, filename=output_filename)
    assert os.path.exists(output_filename) is True
    os.remove(output_filename)


@pytest.mark.search_ro
def test_create_custom_import_file_as_dict(aurorax, conjunction_search_obj):
    custom_import_dict = aurorax.search.conjunctions.swarmaurora.create_custom_import_file(conjunction_search_obj, return_dict=True)
    assert isinstance(custom_import_dict, list) is True
    for item in custom_import_dict:
        assert isinstance(item, dict) is True
