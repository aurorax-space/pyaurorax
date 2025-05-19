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
from pyaurorax.tools import MosaicSkymap


@pytest.mark.tools
def test_simple(at, themis_mosaic_data, capsys):

    # init
    skymaps = themis_mosaic_data["skymaps"]

    prepped_skymaps = at.mosaic.prep_skymaps(skymaps, height_km=110)

    assert isinstance(prepped_skymaps, MosaicSkymap)

    # check __str__ and __repr__ for Mosaic type
    print_str = str(prepped_skymaps)
    assert print_str != ""
    assert isinstance(str(prepped_skymaps), str) is True
    assert isinstance(repr(prepped_skymaps), str) is True
    prepped_skymaps.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.tools
def test_other_args(at, themis_mosaic_data, capsys):

    # init
    skymaps = themis_mosaic_data["skymaps"]

    prepped_skymaps = at.mosaic.prep_skymaps(skymaps, height_km=117.3, n_parallel=2, site_uid_order=["fsmi", "atha"])

    assert isinstance(prepped_skymaps, MosaicSkymap)

    # check __str__ and __repr__ for Mosaic type
    print_str = str(prepped_skymaps)
    assert print_str != ""
    assert isinstance(str(prepped_skymaps), str) is True
    assert isinstance(repr(prepped_skymaps), str) is True
    prepped_skymaps.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.tools
def test_errors(at, themis_mosaic_data, capsys):

    # init
    skymaps = themis_mosaic_data["skymaps"]

    # wrong number of sites in site_uid_order list
    with pytest.raises(ValueError) as e_info:
        _ = at.mosaic.prep_skymaps(skymaps, height_km=110, site_uid_order=["fsmi"])

    assert ("Number of items in supplied skymaps and site_uid_order lists do not match, or " +
            "some site_uids specified in the order were not found. Unable to flatten skymaps due to this mismatch.") in str(e_info)
