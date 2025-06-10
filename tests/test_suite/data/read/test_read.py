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
import pytest
import pyaurorax
from ...conftest import find_dataset

# globals
DATA_DIR = "%s/../../../test_data/data/ucalgary/read" % (os.path.dirname(os.path.realpath(__file__)))


@pytest.mark.data
def test_list_supported_datasets(aurorax):
    # list supported datasets
    supported_datasets = aurorax.data.ucalgary.readers.list_supported_datasets()
    assert len(supported_datasets) > 0


@pytest.mark.data
def test_is_supported(aurorax):
    # check if supported
    is_supported = aurorax.data.ucalgary.readers.is_supported("TREX_RGB_RAW_NOMINAL")
    assert is_supported is True


@pytest.mark.data
def test_read(aurorax, all_datasets):
    # get dataset
    dataset = find_dataset(all_datasets, "THEMIS_ASI_RAW")

    # read a file using the general reader
    filename = "%s/read_themis/20140310_0600_gill_themis19_full.pgm.gz" % (DATA_DIR)
    data = aurorax.data.ucalgary.read(dataset, filename)
    assert isinstance(data, pyaurorax.data.ucalgary.Data)


@pytest.mark.data
def test_read_themis_reader(aurorax):
    # read a file using the specific reader
    filename = "%s/read_themis/20140310_0600_gill_themis19_full.pgm.gz" % (DATA_DIR)
    data = aurorax.data.ucalgary.readers.read_themis(filename)
    assert isinstance(data, pyaurorax.data.ucalgary.Data)


@pytest.mark.data
def test_read_rego_reader(aurorax):
    # read a file using the specific reader
    filename = "%s/read_rego/20180403_0600_gill_rego-652_6300.pgm.gz" % (DATA_DIR)
    data = aurorax.data.ucalgary.readers.read_rego(filename)
    assert isinstance(data, pyaurorax.data.ucalgary.Data)


@pytest.mark.data
def test_read_trex_nir_reader(aurorax):
    # read a file using the specific reader
    filename = "%s/read_trex_nir/20220307_0600_gill_nir-216_8446.pgm.gz" % (DATA_DIR)
    data = aurorax.data.ucalgary.readers.read_trex_nir(filename)
    assert isinstance(data, pyaurorax.data.ucalgary.Data)


@pytest.mark.data
def test_read_trex_rgb_reader(aurorax):
    # read a file using the specific reader
    filename = "%s/read_trex_rgb/20210205_0600_gill_rgb-04_full.h5" % (DATA_DIR)
    data = aurorax.data.ucalgary.readers.read_trex_rgb(filename)
    assert isinstance(data, pyaurorax.data.ucalgary.Data)


@pytest.mark.data
def test_read_trex_blue_reader(aurorax):
    # read a file using the specific reader
    filename = "%s/read_trex_blue/20220308_0600_gill_blue-814_full.pgm.gz" % (DATA_DIR)
    data = aurorax.data.ucalgary.readers.read_trex_blue(filename)
    assert isinstance(data, pyaurorax.data.ucalgary.Data)


@pytest.mark.data
def test_read_trex_spect_reader(aurorax):
    # read a file using the specific reader
    filename = "%s/read_trex_spectrograph/20230503_0600_luck_spect-02_spectra.pgm.gz" % (DATA_DIR)
    data = aurorax.data.ucalgary.readers.read_trex_spectrograph(filename)
    assert isinstance(data, pyaurorax.data.ucalgary.Data)


@pytest.mark.data
def test_read_smile_reader(aurorax):
    # read a file using the specific reader
    filename = "%s/read_smile/20250315_0600_atha_smile-31_rgb-full.h5" % (DATA_DIR)
    data = aurorax.data.ucalgary.readers.read_smile(filename)
    assert isinstance(data, pyaurorax.data.ucalgary.Data)


@pytest.mark.data
def test_read_skymap_reader(aurorax):
    # read a file using the specific reader
    filename = "%s/read_skymap/themis_skymap_atha_20230115-+_v02.sav" % (DATA_DIR)
    data = aurorax.data.ucalgary.readers.read_skymap(filename)
    assert isinstance(data, pyaurorax.data.ucalgary.Data)


@pytest.mark.data
def test_read_calibration_reader(aurorax):
    # read a file using the specific reader
    filename = "%s/read_calibration/REGO_Rayleighs_15651_20210908-+_v02.sav" % (DATA_DIR)
    data = aurorax.data.ucalgary.readers.read_calibration(filename)
    assert isinstance(data, pyaurorax.data.ucalgary.Data)


@pytest.mark.data
def test_read_grid_reader(aurorax):
    # read a file using the specific reader
    filename = "%s/read_grid/20230324_0600_110km_MOSv001_grid_themis-asi.h5" % (DATA_DIR)
    data = aurorax.data.ucalgary.readers.read_grid(filename)
    assert isinstance(data, pyaurorax.data.ucalgary.Data)
