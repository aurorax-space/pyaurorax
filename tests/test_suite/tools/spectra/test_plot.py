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
import datetime
import warnings
import random
import string
import os
import matplotlib.pyplot as plt
from unittest.mock import patch


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
@pytest.mark.parametrize("spect_loc", [140, 145])
@pytest.mark.parametrize("minute", [9, 32])
def test_simple(mock_show, plot_cleanup, at, trex_spect_keogram_data, spect_loc, minute):

    # get spect data
    data = trex_spect_keogram_data["raw_data"]

    t_0 = datetime.datetime(2021, 2, 16, 9, minute, 0)

    # call the plotting function
    at.spectra.plot(data, t_0, spect_loc, figsize=(10, 4))
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_multi_spectra(mock_show, plot_cleanup, at, trex_spect_keogram_data):

    # get spect data
    data = trex_spect_keogram_data["raw_data"]

    t_0 = datetime.datetime(2021, 2, 16, 9, 30, 0)
    spect_loc = [28, 70, 123]

    # call the plotting function
    at.spectra.plot(data, t_0, spect_loc, figsize=(10, 4))
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_multi_time(mock_show, plot_cleanup, at, trex_spect_keogram_data):

    # get spect data
    data = trex_spect_keogram_data["raw_data"]

    t_0 = datetime.datetime(2021, 2, 16, 9, 20, 0)
    t_1 = datetime.datetime(2021, 2, 16, 9, 30, 0)
    t_2 = datetime.datetime(2021, 2, 16, 9, 40, 0)
    times = [t_0, t_1, t_2]
    spect_loc = 140

    # call the plotting function
    at.spectra.plot(data, times, spect_loc, figsize=(10, 4))
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_multi_time_and_spectra(mock_show, plot_cleanup, at, trex_spect_keogram_data):

    # get spect data
    data = trex_spect_keogram_data["raw_data"]

    t_0 = datetime.datetime(2021, 2, 16, 9, 20, 0)
    t_1 = datetime.datetime(2021, 2, 16, 9, 30, 0)
    t_2 = datetime.datetime(2021, 2, 16, 9, 40, 0)
    times = [t_0, t_1, t_2]
    spect_loc = [70, 90, 115]

    # call the plotting function
    at.spectra.plot(data, times, spect_loc, figsize=(10, 4))
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_different_args(mock_show, plot_cleanup, at, trex_spect_keogram_data):

    # get spect data
    data = trex_spect_keogram_data["raw_data"]

    # overplot the redline and greenline
    lines = [557.7, 630.0]
    line_colors = ["green", "red"]

    # different location, at two new times
    t_0 = datetime.datetime(2021, 2, 16, 9, 2, 15)
    t_1 = datetime.datetime(2021, 2, 16, 9, 10, 0)
    spect_loc = 41

    # plotting function, use a log scale for the y_axis
    at.spectra.plot(data, [t_0, t_1],
                    spect_loc,
                    figsize=(10, 4),
                    plot_line=lines,
                    ylog=True,
                    plot_line_color=line_colors,
                    xlim=(520, 660),
                    color=["dodgerblue", "purple"])
    assert mock_show.call_count == 1


@pytest.mark.tools
def test_mismatched_input_lengths(at, trex_spect_keogram_data):
    # get spect data
    data = trex_spect_keogram_data["raw_data"]
    t_0 = datetime.datetime(2021, 2, 16, 9, 30, 0)
    t_1 = datetime.datetime(2021, 2, 16, 9, 35, 0)
    spect_loc = [28, 70, 120]
    times = [t_0, t_1]

    # try to use returnfig and savefig in the same call
    with pytest.raises(ValueError) as e_info:
        at.spectra.plot(data, times, spect_loc, figsize=(10, 4))
    assert "Inputs 'timestamp' and 'spect_loc' must have the same number of elements (or one must be of length 1)." in str(e_info)


@pytest.mark.tools
def test_returnfig_savefig(at, trex_spect_keogram_data):
    # get spect data
    data = trex_spect_keogram_data["raw_data"]
    t_0 = datetime.datetime(2021, 2, 16, 9, 30, 0)
    spect_loc = [28, 70, 123]

    # try to use returnfig and savefig in the same call
    with pytest.raises(ValueError) as e_info:
        at.spectra.plot(data, t_0, spect_loc, figsize=(10, 4), returnfig=True, savefig=True)
    assert "Only one of returnfig or savefig can be set to True" in str(e_info)


@pytest.mark.tools
def test_returnfig_warnings(at, trex_spect_keogram_data):
    # get spect data
    data = trex_spect_keogram_data["raw_data"]
    t_0 = datetime.datetime(2021, 2, 16, 9, 30, 0)
    spect_loc = [28, 70, 123]

    # check savefig filename
    with warnings.catch_warnings(record=True) as w:
        fig, _ = at.spectra.plot(data, t_0, spect_loc, figsize=(10, 4), returnfig=True, savefig_filename="some_filename")
    assert len(w) >= 1
    assert issubclass(w[0].category, UserWarning)
    assert "The figure will be returned, but a savefig option parameter was supplied" in str(w[0].message)
    plt.close(fig)

    # check savefig_quality
    with warnings.catch_warnings(record=True) as w:
        fig, _ = at.spectra.plot(data, t_0, spect_loc, figsize=(10, 4), returnfig=True, savefig_quality=90)
    assert len(w) >= 1
    assert issubclass(w[0].category, UserWarning)
    assert "The figure will be returned, but a savefig option parameter was supplied" in str(w[0].message)
    plt.close(fig)

    # check both
    with warnings.catch_warnings(record=True) as w:
        fig, _ = at.spectra.plot(data, t_0, spect_loc, figsize=(10, 4), returnfig=True, savefig_filename="some_filename", savefig_quality=90)
    assert len(w) >= 1
    assert issubclass(w[0].category, UserWarning)
    assert "The figure will be returned, but a savefig option parameter was supplied" in str(w[0].message)
    plt.close(fig)


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_savefig_warnings(mock_show, at, plot_cleanup, trex_spect_keogram_data):
    # get spect data
    data = trex_spect_keogram_data["raw_data"]
    t_0 = datetime.datetime(2021, 2, 16, 9, 30, 0)
    spect_loc = [28, 70, 123]

    # check savefig_filename
    with warnings.catch_warnings(record=True) as w:
        at.spectra.plot(data, t_0, spect_loc, figsize=(10, 4), savefig_filename="some_filename")
    assert len(w) >= 1
    assert issubclass(w[0].category, UserWarning)
    assert "A savefig option parameter was supplied, but the savefig parameter is False" in str(w[0].message)

    # check savefig_quality
    with warnings.catch_warnings(record=True) as w:
        at.spectra.plot(data, t_0, spect_loc, figsize=(10, 4), savefig_quality=90)
    assert len(w) >= 1
    assert issubclass(w[0].category, UserWarning)
    assert "A savefig option parameter was supplied, but the savefig parameter is False" in str(w[0].message)

    # check both
    with warnings.catch_warnings(record=True) as w:
        at.spectra.plot(data, t_0, spect_loc, figsize=(10, 4), savefig_filename="some_filename", savefig_quality=90)
    assert len(w) >= 1
    assert issubclass(w[0].category, UserWarning)
    assert "A savefig option parameter was supplied, but the savefig parameter is False" in str(w[0].message)

    # check plots
    assert mock_show.call_count == 3


@pytest.mark.tools
def test_savefig(at, trex_spect_keogram_data):
    # get spect data
    data = trex_spect_keogram_data["raw_data"]
    t_0 = datetime.datetime(2021, 2, 16, 9, 30, 0)
    spect_loc = [28, 70, 123]

    # check filename missing
    with pytest.raises(ValueError) as e_info:
        at.spectra.plot(data, t_0, spect_loc, figsize=(10, 4), savefig=True)
    assert "The savefig_filename parameter is missing, but required since savefig was set to True" in str(e_info)

    # regular savefig
    output_filename = "/tmp/pyaurorax_testing_%s.png" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    at.spectra.plot(data, t_0, spect_loc, figsize=(10, 4), savefig=True, savefig_filename=output_filename, plot_line=557.7)
    assert os.path.exists(output_filename)
    os.remove(output_filename)

    # regular savefig
    output_filename = "/tmp/pyaurorax_testing_%s.jpg" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    at.spectra.plot(data, t_0, spect_loc, figsize=(10, 4), savefig=True, savefig_filename=output_filename, plot_line=557.7, plot_line_color='green')
    assert os.path.exists(output_filename)
    os.remove(output_filename)

    # savefig with quality and not a jpg (will show warning)
    output_filename = "/tmp/pyaurorax_testing_%s.png" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    with warnings.catch_warnings(record=True) as w:
        at.spectra.plot(data, t_0, spect_loc, figsize=(10, 4), savefig=True, savefig_filename=output_filename, savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "The savefig_quality parameter was specified, but is only used for saving JPG files" in str(w[-1].message)
    assert os.path.exists(output_filename)
    os.remove(output_filename)

    # savefig with quality and not a jpg (will show warning)
    output_filename = "/tmp/pyaurorax_testing_%s.jpg" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    at.spectra.plot(data, t_0, spect_loc, figsize=(10, 4), savefig=True, savefig_filename=output_filename, savefig_quality=90)
    assert os.path.exists(output_filename)
    os.remove(output_filename)
