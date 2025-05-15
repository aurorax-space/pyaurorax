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
import warnings
import os
import string
import random
import datetime
import cartopy.crs
from matplotlib import pyplot as plt
from unittest.mock import patch


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_data_availability(mock_show, plot_cleanup, at):

    # Data for data availability
    start = datetime.datetime(2024, 1, 1, 0, 0)
    end = datetime.datetime(2024, 1, 1, 23, 59)

    # Attempt to add availability to FOVData defined without instrument specified
    fov_data = at.fov.create_data(sites=[("custom1", 60.0, -120.0), ("custom2", 65.0, -130.0)], height_km=110.0)
    with pytest.raises(ValueError) as e_info:
        fov_data.add_availability(dataset_name="REGO_RAW", start=start, end=end)
    assert ("Cannot add data availability to an FOVData object with no associated instrument_array. Please specify " +
            "instrument_array upon creation of FOVData object to enforce data availability.") in str(e_info)

    # Create FOVData for spectrographs and enforce data availability
    fov_data = at.fov.create_data(sites=["rabb", "luck"], instrument_array="trex_spectrograph")
    fov_data.add_availability(dataset_name="TREX_SPECT_PROCESSED_V1", start=start, end=end)

    # check __str__ and __repr__ for fov_map type
    print_str = str(fov_data)
    assert print_str != ""
    assert isinstance(str(fov_data), str) is True
    assert isinstance(repr(fov_data), str) is True
