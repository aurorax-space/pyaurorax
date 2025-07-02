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
import cartopy.crs
from matplotlib import pyplot as plt
from unittest.mock import patch


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_simple(mock_show, plot_cleanup, at):

    # Create FOVData
    fov_data = at.fov.create_data(
        ['atha', 'fsmi'],
        instrument_array='themis_asi',
    )

    # Create FOV
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=-100.0, central_latitude=55.0)
    fov_map = at.fov.create_map(projection_obj, fov_data)

    fov_map.plot([-145, -65, 35, 80])
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_args(mock_show, plot_cleanup, at):

    # Create FOVData
    fov_data = at.fov.create_data(
        ['atha', 'fsmi'],
        instrument_array='themis_asi',
    )

    # Create FOV
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=-100.0, central_latitude=55.0)
    fov_map = at.fov.create_map(projection_obj, fov_data)

    fov_map.plot([-145, -65, 35, 80],
                 label=False,
                 figsize=(10, 7),
                 land_color="red",
                 land_edgecolor="green",
                 borders_color="orange",
                 borders_disable=True,
                 title="some title",
                 ocean_color="white")

    assert mock_show.call_count == 1


@pytest.mark.tools
def test_returnfig_savefig(at):

    # Create FOVData
    fov_data = at.fov.create_data(
        ['atha', 'fsmi'],
        instrument_array='themis_asi',
    )

    # Create FOV
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=-100.0, central_latitude=55.0)
    fov_map = at.fov.create_map(projection_obj, fov_data)

    with pytest.raises(ValueError) as e_info:
        fov_map.plot([-145, -65, 35, 80], returnfig=True, savefig=True)
    assert "Only one of returnfig or savefig can be set to True" in str(e_info)


@pytest.mark.tools
def test_returnfig_warnings(at):

    # Create FOVData
    fov_data = at.fov.create_data(
        ['atha', 'fsmi'],
        instrument_array='themis_asi',
    )

    # Create FOV
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=-100.0, central_latitude=55.0)
    fov_map = at.fov.create_map(projection_obj, fov_data)

    # check savefig_filename
    with warnings.catch_warnings(record=True) as w:
        fig, _ = fov_map.plot([-145, -65, 35, 80], returnfig=True, savefig_filename="some_filename")

    assert len(w) >= 1
    assert issubclass(w[0].category, UserWarning)
    assert "The figure will be returned, but a savefig option parameter was supplied" in str(w[0].message)
    plt.close(fig)

    # check savefig_quality
    with warnings.catch_warnings(record=True) as w:
        fig, _ = fov_map.plot([-145, -65, 35, 80], returnfig=True, savefig_quality=90)
    assert len(w) >= 1
    assert issubclass(w[0].category, UserWarning)
    assert "The figure will be returned, but a savefig option parameter was supplied" in str(w[0].message)
    plt.close(fig)

    # check both
    with warnings.catch_warnings(record=True) as w:
        fig, _ = fov_map.plot([-145, -65, 35, 80], returnfig=True, savefig_filename="some_filename", savefig_quality=90)
    assert len(w) >= 1
    assert issubclass(w[0].category, UserWarning)
    assert "The figure will be returned, but a savefig option parameter was supplied" in str(w[0].message)
    plt.close(fig)


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_savefig_warnings(mock_show, at, plot_cleanup):

    # Create FOVData
    fov_data = at.fov.create_data(
        ['atha', 'fsmi'],
        instrument_array='themis_asi',
    )

    # Create FOV
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=-100.0, central_latitude=55.0)
    fov_map = at.fov.create_map(projection_obj, fov_data)

    # check savefig_filename
    with warnings.catch_warnings(record=True) as w:
        fov_map.plot([-145, -65, 35, 80], savefig_filename="some_filename")
    assert len(w) >= 1
    assert issubclass(w[0].category, UserWarning)
    assert "A savefig option parameter was supplied, but the savefig parameter is False" in str(w[0].message)

    # check savefig_quality
    with warnings.catch_warnings(record=True) as w:
        fov_map.plot([-145, -65, 35, 80], savefig_quality=90)
    assert len(w) >= 1
    assert issubclass(w[0].category, UserWarning)
    assert "A savefig option parameter was supplied, but the savefig parameter is False" in str(w[0].message)

    # check both
    with warnings.catch_warnings(record=True) as w:
        fov_map.plot([-145, -65, 35, 80], savefig_filename="some_filename", savefig_quality=90)
    assert len(w) >= 1
    assert issubclass(w[0].category, UserWarning)
    assert "A savefig option parameter was supplied, but the savefig parameter is False" in str(w[0].message)

    # check plots
    assert mock_show.call_count == 3


@pytest.mark.tools
def test_savefig(at):

    # Create FOVData
    fov_data = at.fov.create_data(
        ['atha', 'fsmi'],
        instrument_array='themis_asi',
    )

    # Create FOV
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=-100.0, central_latitude=55.0)
    fov_map = at.fov.create_map(projection_obj, fov_data)

    # check filename missing
    with pytest.raises(ValueError) as e_info:
        fov_map.plot([-145, -65, 35, 80], savefig=True)
    assert "The savefig_filename parameter is missing, but required since savefig was set to True" in str(e_info)

    # regular savefig
    output_filename = "/tmp/pyaurorax_testing_%s.png" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    fov_map.plot([-145, -65, 35, 80], savefig=True, savefig_filename=output_filename)
    assert os.path.exists(output_filename)
    os.remove(output_filename)

    # regular savefig
    output_filename = "/tmp/pyaurorax_testing_%s.jpg" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    fov_map.plot([-145, -65, 35, 80], savefig=True, savefig_filename=output_filename)
    assert os.path.exists(output_filename)
    os.remove(output_filename)

    # savefig with quality and not a jpg (will show warning)
    output_filename = "/tmp/pyaurorax_testing_%s.png" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    with warnings.catch_warnings(record=True) as w:
        fov_map.plot([-145, -65, 35, 80], savefig=True, savefig_filename=output_filename, savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "The savefig_quality parameter was specified, but is only used for saving JPG files" in str(w[-1].message)
    assert os.path.exists(output_filename)
    os.remove(output_filename)

    # savefig with quality and is a jpg
    output_filename = "/tmp/pyaurorax_testing_%s.jpg" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    fov_map.plot([-145, -65, 35, 80], savefig=True, savefig_filename=output_filename, savefig_quality=90)
    assert os.path.exists(output_filename)
    os.remove(output_filename)


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_with_data_availability(mock_show, at):

    # Create FOVData
    fov_data = at.fov.create_data(
        ['atha', 'fsmi'],
        instrument_array='themis_asi',
    )

    # Create FOV
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=-100.0, central_latitude=55.0)
    fov_map = at.fov.create_map(projection_obj, fov_data)

    # Plot and enforce data availability without actually adding data availability
    with pytest.raises(ValueError) as e_info:
        fov_map.plot([-145, -65, 35, 80], enforce_data_availability=True)

    assert ("Before plotting FOV object with enforce_data_availability=True, " +
            "FOVData.add_availability(...) must be called for all included FOVData objects.") in str(e_info)


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_with_contours(mock_show, at):

    # Create FOVData
    fov_data = at.fov.create_data(
        ['atha', 'fsmi'],
        instrument_array='themis_asi',
    )

    # Create FOV with no data
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=-100.0, central_latitude=55.0)
    fov_map = at.fov.create_map(projection_obj, fov_data)

    # Add some magnetic and geomagnetic contours
    fov_map.add_geo_contours(lats=[60.0, 60.0, 60.0],
                             lons=[-130.0, -125.0, -120.0],
                             constant_lats=[55.0],
                             constant_lons=[-150.0],
                             color="red",
                             linewidth=2,
                             linestyle="--",
                             marker="o",
                             bring_to_front=True)

    fov_map.plot([-145, -65, 35, 80])

    assert mock_show.call_count == 1
