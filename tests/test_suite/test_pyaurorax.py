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
import pyucalgarysrs
import datetime
from pathlib import Path


@pytest.mark.top_level
def test_top_level_class_instantiation_noparams(capsys):
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

    # change API key
    testing_api_key = "some-api-key"
    aurorax.api_key = testing_api_key
    assert aurorax.api_key == testing_api_key

    # check __str__ and __repr__ for PyAuroraX type
    print_str = str(aurorax)
    assert print_str != ""
    assert isinstance(str(aurorax), str) is True
    assert isinstance(repr(aurorax), str) is True
    aurorax.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # check SRS object
    assert isinstance(aurorax.srs_obj, pyucalgarysrs.PyUCalgarySRS) is True


@pytest.mark.top_level
def test_top_level_class_instantiation_usingparams():
    # instantiate object
    testing_url = "https://testing-url.com"
    testing_api_key = "some-api-key"
    testing_download_path = str("%s/pyaurorax_data_download_testing_%s" %
                                (Path.home(), ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))))
    testing_tar_path = str("%s/pyaurorax_tar_read_testing_%s" % (Path.home(), ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))))
    testing_api_timeout = 5
    aurorax = pyaurorax.PyAuroraX(
        api_base_url=testing_url,
        download_output_root_path=testing_download_path,
        read_tar_temp_path=testing_tar_path,
        api_timeout=testing_api_timeout,
        api_key=testing_api_key,
    )
    assert aurorax.download_output_root_path == testing_download_path
    assert aurorax.read_tar_temp_path == testing_tar_path
    assert aurorax.api_base_url == testing_url
    assert aurorax.api_key == testing_api_key
    assert aurorax.api_headers != {} and "user-agent" in aurorax.api_headers and "python-pyaurorax" in aurorax.api_headers["user-agent"]
    assert aurorax.api_timeout == testing_api_timeout
    assert os.path.exists(testing_download_path)
    assert os.path.exists(testing_tar_path)

    # cleanup
    shutil.rmtree(testing_download_path, ignore_errors=True)
    shutil.rmtree(testing_tar_path, ignore_errors=True)


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

    # check that trailing slash is removed
    aurorax.api_base_url = "https://something/"
    assert aurorax.api_base_url == "https://something"

    # check invalid URL
    with pytest.raises(pyaurorax.AuroraXInitializationError) as e_info:
        aurorax.api_base_url = "something invalid"
    assert "API base URL is an invalid URL" in str(e_info)


@pytest.mark.top_level
def test_api_timeout(aurorax):
    # set flag
    default_timeout = aurorax.api_timeout
    aurorax.api_timeout = 5
    assert aurorax.api_timeout == 5
    aurorax.api_timeout = None
    assert aurorax.api_timeout == default_timeout


@pytest.mark.top_level
def test_progress_bar_backend(aurorax):
    # save default for later
    progress_bar_backend = aurorax.progress_bar_backend

    # set flag (standard)
    aurorax.progress_bar_backend = "standard"
    assert aurorax.progress_bar_backend == "standard"

    # set flag (notebook)
    aurorax.progress_bar_backend = "notebook"
    assert aurorax.progress_bar_backend == "notebook"

    # set flag (auto)
    aurorax.progress_bar_backend = "auto"
    assert aurorax.progress_bar_backend == "auto"

    # set flag (back to default)
    aurorax.progress_bar_backend = None
    assert aurorax.progress_bar_backend == progress_bar_backend

    # check invalid value
    with pytest.raises(pyaurorax.AuroraXInitializationError) as e_info:
        aurorax.progress_bar_backend = "something invalid"
    assert "Invalid progress bar backend" in str(e_info)


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


@pytest.mark.top_level
def test_show_data_usage(aurorax, capsys):
    # download a bit of data for several datasets
    for dataset_name in ["THEMIS_ASI_RAW", "TREX_RGB_RAW_NOMINAL"]:
        start_dt = datetime.datetime(2023, 1, 1, 6, 0)
        end_dt = datetime.datetime(2023, 1, 1, 6, 0)
        site_uid = "gill"
        aurorax.data.ucalgary.download(dataset_name, start_dt, end_dt, site_uid=site_uid, progress_bar_disable=True)

    # check default params
    print(aurorax.show_data_usage())
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # check return_dict=True
    print(aurorax.show_data_usage(return_dict=True))
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # check order being name
    print(aurorax.show_data_usage(order="name"))
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""
