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
import warnings
import random
import string
from matplotlib import pyplot as plt
from unittest.mock import patch


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_simple(mock_show, plot_cleanup, at, themis_single_file):
    at.display(themis_single_file.data[:, :, 0])
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_args(mock_show, plot_cleanup, at, themis_single_file):
    at.display(themis_single_file.data[:, :, 0], colorbar=True, title="some title")
    assert mock_show.call_count == 1


@pytest.mark.tools
def test_returnfig_savefig(at, themis_single_file):
    with pytest.raises(ValueError) as e_info:
        at.display(themis_single_file.data[:, :, 0], returnfig=True, savefig=True)
    assert "Only one of returnfig or savefig can be set to True" in str(e_info)


@pytest.mark.tools
def test_returnfig_warnings(at, themis_single_file):
    # check savefig_filename
    with warnings.catch_warnings(record=True) as w:
        fig, _ = at.display(themis_single_file.data[:, :, 0], returnfig=True, savefig_filename="some_filename")
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "The figure will be returned, but a savefig option parameter was supplied" in str(w[-1].message)
    plt.close(fig)

    # check savefig_quality
    with warnings.catch_warnings(record=True) as w:
        fig, _ = at.display(themis_single_file.data[:, :, 0], returnfig=True, savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "The figure will be returned, but a savefig option parameter was supplied" in str(w[-1].message)
    plt.close(fig)

    # check both
    with warnings.catch_warnings(record=True) as w:
        fig, _ = at.display(themis_single_file.data[:, :, 0], returnfig=True, savefig_filename="some_filename", savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "The figure will be returned, but a savefig option parameter was supplied" in str(w[-1].message)
    plt.close(fig)


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_savefig_warnins(mock_show, at, plot_cleanup, themis_single_file):
    # check savefig_filename
    with warnings.catch_warnings(record=True) as w:
        at.display(themis_single_file.data[:, :, 0], savefig_filename="some_filename")
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "A savefig option parameter was supplied, but the savefig parameter is False" in str(w[-1].message)

    # check savefig_quality
    with warnings.catch_warnings(record=True) as w:
        at.display(themis_single_file.data[:, :, 0], savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "A savefig option parameter was supplied, but the savefig parameter is False" in str(w[-1].message)

    # check both
    with warnings.catch_warnings(record=True) as w:
        at.display(themis_single_file.data[:, :, 0], savefig_filename="some_filename", savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "A savefig option parameter was supplied, but the savefig parameter is False" in str(w[-1].message)

    # check plots
    assert mock_show.call_count == 3


@pytest.mark.tools
def test_savefig(at, themis_single_file):
    # check filename missing
    with pytest.raises(ValueError) as e_info:
        at.display(themis_single_file.data[:, :, 0], savefig=True)
    assert "The savefig_filename parameter is missing, but required since savefig was set to True" in str(e_info)

    # regular savefig
    output_filename = "/tmp/pyaurorax_testing_%s.png" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    at.display(themis_single_file.data[:, :, 0], savefig=True, savefig_filename=output_filename)
    assert os.path.exists(output_filename)
    os.remove(output_filename)

    # regular savefig
    output_filename = "/tmp/pyaurorax_testing_%s.jpg" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    at.display(themis_single_file.data[:, :, 0], savefig=True, savefig_filename=output_filename)
    assert os.path.exists(output_filename)
    os.remove(output_filename)

    # savefig with quality and not a jpg (will show warning)
    output_filename = "/tmp/pyaurorax_testing_%s.png" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    with warnings.catch_warnings(record=True) as w:
        at.display(themis_single_file.data[:, :, 0], savefig=True, savefig_filename=output_filename, savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "The savefig_quality parameter was specified, but is only used for saving JPG files" in str(w[-1].message)
    assert os.path.exists(output_filename)
    os.remove(output_filename)
