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
from unittest.mock import patch


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_dark_mode(mock_show, plot_cleanup, at, themis_single_file):
    # set plot theme to dark mode
    at.set_theme("dark")
    at.display(themis_single_file.data[:, :, 0])

    # set plot theme to light mode
    at.set_theme("light")
    at.display(themis_single_file.data[:, :, 0])

    # set plot theme to default mode
    at.set_theme("default")
    at.display(themis_single_file.data[:, :, 0])

    # set plot theme to another available mode
    at.set_theme("ggplot")
    at.display(themis_single_file.data[:, :, 0])

    # check number of plots
    assert mock_show.call_count == 4
