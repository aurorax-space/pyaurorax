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
import datetime


@pytest.mark.data
def test_download(aurorax):
    # download
    dataset_name = "THEMIS_ASI_RAW"
    site_uid = "atha"
    start_dt = datetime.datetime(2020, 1, 1, 6, 0)
    end_dt = datetime.datetime(2020, 1, 1, 6, 9)
    r = aurorax.data.ucalgary.download(dataset_name, start_dt, end_dt, site_uid=site_uid, progress_bar_disable=True)
    assert isinstance(r, pyaurorax.data.ucalgary.FileDownloadResult)
    assert r.count > 0


@pytest.mark.data
def test_download_using_urls(aurorax):
    # get urls
    dataset_name = "THEMIS_ASI_RAW"
    start_dt = datetime.datetime(2020, 1, 1, 6, 0)
    end_dt = datetime.datetime(2020, 1, 1, 6, 9)
    site_uid = "atha"
    r = aurorax.data.ucalgary.get_urls(dataset_name, start_dt, end_dt, site_uid=site_uid)
    assert isinstance(r, pyaurorax.data.ucalgary.FileListingResponse)
    assert r.count > 0

    # download
    r = aurorax.data.ucalgary.download_using_urls(r, progress_bar_disable=True)
    assert isinstance(r, pyaurorax.data.ucalgary.FileDownloadResult)
    assert r.count > 0


@pytest.mark.data
def test_download_best_skymap(aurorax):
    # download
    dataset_name = "THEMIS_ASI_SKYMAP_IDLSAV"
    site_uid = "atha"
    timestamp = datetime.datetime(2020, 1, 1, 0, 0)
    r = aurorax.data.ucalgary.download_best_skymap(dataset_name, site_uid, timestamp)
    assert isinstance(r, pyaurorax.data.ucalgary.FileDownloadResult)
    assert r.count > 0


@pytest.mark.data
def test_download_best_skymap_bad(aurorax):
    # download
    dataset_name = "THEMIS_ASI_SKYMAP_IDLSAV"
    site_uid = "asdf"
    timestamp = datetime.datetime(2020, 1, 1, 0, 0)
    with pytest.raises(ValueError) as e_info:
        _ = aurorax.data.ucalgary.download_best_skymap(dataset_name, site_uid, timestamp)
    assert "Unable to determine a skymap recommendation" in str(e_info)


@pytest.mark.data
def test_download_best_calibration_rayleighs(aurorax):
    # download
    dataset_name = "REGO_CALIBRATION_RAYLEIGHS_IDLSAV"
    device_uid = "654"
    timestamp = datetime.datetime(2020, 1, 1, 0, 0)
    r = aurorax.data.ucalgary.download_best_rayleighs_calibration(dataset_name, device_uid, timestamp)
    assert isinstance(r, pyaurorax.data.ucalgary.FileDownloadResult)
    assert r.count > 0


@pytest.mark.data
def test_download_best_calibration_rayleighs_bad(aurorax):
    # download
    dataset_name = "REGO_CALIBRATION_RAYLEIGHS_IDLSAV"
    device_uid = "something-bad"
    timestamp = datetime.datetime(2020, 1, 1, 0, 0)
    with pytest.raises(ValueError) as e_info:
        _ = aurorax.data.ucalgary.download_best_rayleighs_calibration(dataset_name, device_uid, timestamp)
    assert "Unable to determine a Rayleighs calibration recommendation" in str(e_info)


@pytest.mark.data
def test_download_best_calibration_flatfield(aurorax):
    # download
    dataset_name = "REGO_CALIBRATION_FLATFIELD_IDLSAV"
    device_uid = "654"
    timestamp = datetime.datetime(2020, 1, 1, 0, 0)
    r = aurorax.data.ucalgary.download_best_flatfield_calibration(dataset_name, device_uid, timestamp)
    assert isinstance(r, pyaurorax.data.ucalgary.FileDownloadResult)
    assert r.count > 0


@pytest.mark.data
def test_download_best_calibration_flatfield_bad(aurorax):
    # download
    dataset_name = "REGO_CALIBRATION_FLATFIELD_IDLSAV"
    device_uid = "something-bad"
    timestamp = datetime.datetime(2020, 1, 1, 0, 0)
    with pytest.raises(ValueError) as e_info:
        _ = aurorax.data.ucalgary.download_best_flatfield_calibration(dataset_name, device_uid, timestamp)
    assert "Unable to determine a flatfield calibration recommendation" in str(e_info)
