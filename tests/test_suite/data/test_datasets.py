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
import pyaurorax


@pytest.mark.data
def test_list_datasets(aurorax):
    # list datasets
    datasets = aurorax.data.list_datasets()
    assert len(datasets) > 0

    # check type
    for d in datasets:
        assert isinstance(d, pyaurorax.data.Dataset) is True

    # list datasets, but changing the API url to something bad first
    aurorax.srs_obj.api_base_url = "https://aurora.phys.ucalgary.ca/api_testing_url"
    with pytest.raises(pyaurorax.exceptions.AuroraXAPIError) as e_info:
        aurorax.data.list_datasets()
    assert str(e_info) != ""


@pytest.mark.data
def test_get_dataset(aurorax):
    # get dataset
    dataset = aurorax.data.get_dataset("TREX_RGB_RAW_NOMINAL")
    assert isinstance(dataset, pyaurorax.data.Dataset)
    assert dataset.name == "TREX_RGB_RAW_NOMINAL"

    # get dataset that doesn't exist
    with pytest.raises(pyaurorax.exceptions.AuroraXAPIError) as e_info:
        dataset = aurorax.data.get_dataset("SOME_BAD_DATASET")
    assert "Dataset not found" in str(e_info)


@pytest.mark.data
def test_list_datasets_in_table(aurorax, capsys):
    # list datasets in table
    aurorax.data.list_datasets_in_table()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.data
def test_is_read_supported(aurorax):
    # check if read supported
    is_read_supported = aurorax.data.ucalgary.is_read_supported("TREX_RGB_RAW_NOMINAL")
    assert is_read_supported is True


@pytest.mark.data
def test_list_supported_datasets(aurorax):
    # list supported datasets
    supported_datasets = aurorax.data.ucalgary.list_supported_read_datasets()
    assert len(supported_datasets) > 0
