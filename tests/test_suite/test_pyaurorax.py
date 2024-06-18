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

import shutil
import os
import random
import string
import pytest
import platform
import pyaurorax
import warnings
from pathlib import Path


@pytest.mark.top_level
def test_top_level_class_instantiation_noparams():
    # instantiate
    aurorax = pyaurorax.PyAuroraX()

    # check paths
    assert os.path.exists(aurorax.download_output_root_path)
    assert os.path.exists(aurorax.read_tar_temp_path)

    # change download root path
    new_path = str("%s/pyaurorax_data_download_testing_%s" % (Path.home(), ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))))
    aurorax.download_output_root_path = new_path
    assert aurorax.download_output_root_path == new_path
    assert os.path.exists(new_path)
    shutil.rmtree(new_path, ignore_errors=True)

    # change tar temp path
    new_path = str("%s/pyaurorax_data_tar_testing%s" % (Path.home(), ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))))
    aurorax.read_tar_temp_path = new_path
    assert aurorax.read_tar_temp_path == new_path
    assert os.path.exists(new_path)
    shutil.rmtree(new_path, ignore_errors=True)

    # check str and repr methods
    assert isinstance(str(aurorax), str) is True
    assert isinstance(repr(aurorax), str) is True


@pytest.mark.top_level
def test_top_level_class_instantiation_usingparams():
    # instantiate object
    testing_url = "https://testing-url.com"
    testing_download_path = str("%s/pyaurorax_data_download_testing_%s" %
                                (Path.home(), ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))))
    testing_read_path = str("%s/pyaurorax_data_tar_testing%s" % (Path.home(), ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))))
    testing_api_key = "abcd1234"
    testing_api_timeout = 5
    testing_api_headers = {"some_key": "some value"}
    aurorax = pyaurorax.PyAuroraX(
        api_base_url=testing_url,
        download_output_root_path=testing_download_path,
        read_tar_temp_path=testing_read_path,
        api_key=testing_api_key,
        api_timeout=testing_api_timeout,
        api_headers=testing_api_headers,
    )
    assert aurorax.download_output_root_path == testing_download_path
    assert aurorax.read_tar_temp_path == testing_read_path
    assert aurorax.api_base_url == testing_url
    assert aurorax.api_timeout == testing_api_timeout
    assert aurorax.api_headers == testing_api_headers
    assert aurorax.api_key == testing_api_key
    assert os.path.exists(testing_download_path)
    assert os.path.exists(testing_read_path)

    # cleanup
    shutil.rmtree(testing_download_path, ignore_errors=True)
    shutil.rmtree(testing_read_path, ignore_errors=True)


@pytest.mark.top_level
def test_bad_paths_noparams(aurorax):
    # test bad paths
    #
    # NOTE: we only do this check on Linux since I don't know a bad
    # path to check on Mac. Good enough for now.
    if (platform.system() == "Linux"):
        new_path = "/dev/bad_path"
        with pytest.raises(pyaurorax.AuroraXInitializationError) as e_info:
            aurorax.download_output_root_path = new_path
        assert "Error during output path creation" in str(e_info)
        with pytest.raises(pyaurorax.AuroraXInitializationError) as e_info:
            aurorax.read_tar_temp_path = new_path
        assert "Error during output path creation" in str(e_info)


@pytest.mark.top_level
def test_api_base_url(aurorax):
    # set flag
    aurorax.api_base_url = "https://something"
    assert aurorax.api_base_url == "https://something"
    aurorax.api_base_url = None
    assert aurorax.api_base_url != "https://something"


@pytest.mark.top_level
def test_api_headers(aurorax):
    # set flag
    default_headers = aurorax.api_headers
    aurorax.api_headers = {"some": "thing"}
    assert "some" in aurorax.api_headers and aurorax.api_headers["some"] == "thing"
    aurorax.api_headers = None
    assert aurorax.api_headers == default_headers

    # check warning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")  # cause all warnings to always be triggered.
        aurorax.api_headers = {"user-agent": "some other value"}
        assert len(w) == 1
        assert issubclass(w[-1].category, UserWarning)
        assert "Cannot override default" in str(w[-1].message)


@pytest.mark.top_level
def test_api_timeout(aurorax):
    # set flag
    default_timeout = aurorax.api_timeout
    aurorax.api_timeout = 5
    assert aurorax.api_timeout == 5
    aurorax.api_timeout = None
    assert aurorax.api_timeout == default_timeout


@pytest.mark.top_level
def test_purge_download_path(aurorax):
    # set up object
    #
    # NOTE: we set the path to something with a random string in it
    # so that our github actions for linux/mac/windows, which fire off
    # simultaneously on the same machine, work without stepping on the
    # toes of each other.
    new_path = str("%s/pyaurorax_data_purge_download_testing_%s" %
                   (Path.home(), ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))))
    aurorax.download_output_root_path = new_path
    assert aurorax.download_output_root_path == new_path
    assert os.path.exists(aurorax.download_output_root_path)

    # create some dummy files and folders
    os.makedirs("%s/testing1" % (aurorax.download_output_root_path), exist_ok=True)
    os.makedirs("%s/testing2" % (aurorax.download_output_root_path), exist_ok=True)
    os.makedirs("%s/testing2/testing3" % (aurorax.download_output_root_path), exist_ok=True)
    Path("%s/testing.txt" % (aurorax.download_output_root_path)).touch()
    Path("%s/testing1/testing.txt" % (aurorax.download_output_root_path)).touch()

    # check purge function
    aurorax.purge_download_output_root_path()
    assert len(os.listdir(aurorax.download_output_root_path)) == 0

    # cleanup
    shutil.rmtree(aurorax.download_output_root_path, ignore_errors=True)


@pytest.mark.top_level
def test_purge_tar_temp_path(aurorax):
    # set up object
    new_path = str("%s/pyaurorax_data_purge_tartemp_testing_%s" % (
        Path.home(),
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)),
    ))
    aurorax.read_tar_temp_path = new_path
    assert aurorax.read_tar_temp_path == new_path
    assert os.path.exists(aurorax.read_tar_temp_path)

    # create some dummy files and folders
    os.makedirs("%s/testing1" % (aurorax.read_tar_temp_path), exist_ok=True)
    os.makedirs("%s/testing2" % (aurorax.read_tar_temp_path), exist_ok=True)
    os.makedirs("%s/testing2/testing3" % (aurorax.read_tar_temp_path), exist_ok=True)
    Path("%s/testing.txt" % (aurorax.read_tar_temp_path)).touch()
    Path("%s/testing1/testing.txt" % (aurorax.read_tar_temp_path)).touch()

    # check purge function
    aurorax.purge_read_tar_temp_path()
    assert len(os.listdir(aurorax.read_tar_temp_path)) == 0

    # cleanup
    shutil.rmtree(aurorax.read_tar_temp_path, ignore_errors=True)
