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
import numpy as np
from pyaurorax.tools import Mosaic
from matplotlib import pyplot as plt
from unittest.mock import patch


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_simple(mock_show, plot_cleanup, at, themis_mosaic_data, capsys):
    # init
    mosaic_dt = themis_mosaic_data["dt"]
    prepped_images = themis_mosaic_data["prepped_images"]
    prepped_skymaps = themis_mosaic_data["prepped_skymaps"]

    # create projection
    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # create mosaic
    mosaic = at.mosaic.create(prepped_images, prepped_skymaps, mosaic_dt, projection_obj, spect_cmap="greens_r")
    assert isinstance(mosaic, Mosaic)

    # check __str__ and __repr__ for Mosaic type
    print_str = str(Mosaic)
    assert print_str != ""
    assert isinstance(str(Mosaic), str) is True
    assert isinstance(repr(Mosaic), str) is True
    mosaic.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    map_extent = [-145, -65, 35, 80]
    mosaic.plot(map_extent, title="THEMIS ASI")
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_simple_spect(mock_show, plot_cleanup, at, trex_spect_mosaic_data, capsys):
    # init
    mosaic_dt = trex_spect_mosaic_data["dt"]
    prepped_images = trex_spect_mosaic_data["prepped_images"]
    prepped_skymaps = trex_spect_mosaic_data["prepped_skymaps"]

    # create projection
    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # create mosaic
    mosaic = at.mosaic.create(prepped_images, prepped_skymaps, mosaic_dt, projection_obj, spect_intensity_scales=None, spect_cmap="Greens_r")
    assert isinstance(mosaic, Mosaic)

    # check __str__ and __repr__ for Mosaic type
    print_str = str(Mosaic)
    assert print_str != ""
    assert isinstance(str(Mosaic), str) is True
    assert isinstance(repr(Mosaic), str) is True
    mosaic.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    map_extent = [-145, -65, 35, 80]
    mosaic.plot(
        map_extent,
        rayleighs=True,
        title="TREx Spect",
        ocean_color="blue",
        land_color="red",
        land_edgecolor="gray",
        borders_color="brown",
        cbar_title="some_title",
        cbar_colormap="Greens_r",
    )
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_add_contours(mock_show, plot_cleanup, at, themis_mosaic_data):
    # init
    mosaic_dt = themis_mosaic_data["dt"]
    prepped_images = themis_mosaic_data["prepped_images"]
    prepped_skymaps = themis_mosaic_data["prepped_skymaps"]

    # create projection
    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # create mosaic
    mosaic = at.mosaic.create(prepped_images, prepped_skymaps, mosaic_dt, projection_obj, spect_cmap="greens_r")

    # add a bunch of contours
    mosaic.add_mag_contours(mosaic_dt, constant_lats=[62, 72], color="red", linewidth=3, bring_to_front=True)
    mosaic.add_geo_contours(constant_lats=[62, 72], color="red", linewidth=3, bring_to_front=True)
    lat_locs = np.arange(0, 90, 10)
    lon_locs = np.arange(-180, 0, 20)
    mosaic.add_geo_contours(constant_lats=lat_locs, constant_lons=lon_locs, linestyle="--", color="black")
    mosaic.add_mag_contours(mosaic_dt, constant_lats=lat_locs, constant_lons=lon_locs, linestyle="--", color="black")
    mosaic.add_geo_contours(constant_lats=80, constant_lons=-130.3, linestyle="--", color="black")
    mosaic.add_mag_contours(mosaic_dt, constant_lats=80, constant_lons=-130.3, linestyle="--", color="black")
    custom_lats = [40, 43, 47, 47, 45, 40]
    custom_lons = [-145, -125, -125, -135, -140, -145]
    mosaic.add_geo_contours(lats=custom_lats, lons=custom_lons, linestyle="dashdot", linewidth=3, color="blue", bring_to_front=True)
    mosaic.add_mag_contours(mosaic_dt, lats=custom_lats, lons=custom_lons, linestyle="dashdot", linewidth=3, color="blue", bring_to_front=True)

    map_extent = [-145, -65, 35, 80]
    with warnings.catch_warnings(record=True) as w:
        mosaic.plot(map_extent, title="THEMIS ASI", colorbar_title="some_string", borders_disable=True)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "The parameter 'colorbar_title' was deprecated in v1.11.0. Please use 'cbar_title' instead (usage is identical)." in str(w[-1].message)

    assert mock_show.call_count == 1


@pytest.mark.tools
def test_returnfig_savefig(at, themis_mosaic_data):
    # init
    mosaic_dt = themis_mosaic_data["dt"]
    prepped_images = themis_mosaic_data["prepped_images"]
    prepped_skymaps = themis_mosaic_data["prepped_skymaps"]

    # create projection
    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # create mosaic
    mosaic = at.mosaic.create(prepped_images, prepped_skymaps, mosaic_dt, projection_obj)
    map_extent = [-145, -65, 35, 80]

    with pytest.raises(ValueError) as e_info:
        mosaic.plot(map_extent, returnfig=True, savefig=True)
    assert "Only one of returnfig or savefig can be set to True" in str(e_info)


@pytest.mark.tools
def test_returnfig_warnings(at, themis_mosaic_data):
    # init
    mosaic_dt = themis_mosaic_data["dt"]
    prepped_images = themis_mosaic_data["prepped_images"]
    prepped_skymaps = themis_mosaic_data["prepped_skymaps"]

    # create projection
    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # create mosaic
    mosaic = at.mosaic.create(prepped_images, prepped_skymaps, mosaic_dt, projection_obj)
    map_extent = [-145, -65, 35, 80]

    # check savefig_filename
    with warnings.catch_warnings(record=True) as w:
        fig, _ = mosaic.plot(map_extent, returnfig=True, savefig_filename="some_filename")
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "The figure will be returned, but a savefig option parameter was supplied" in str(w[-1].message)
    plt.close(fig)

    # check savefig_quality
    with warnings.catch_warnings(record=True) as w:
        fig, _ = mosaic.plot(map_extent, returnfig=True, savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "The figure will be returned, but a savefig option parameter was supplied" in str(w[-1].message)
    plt.close(fig)

    # check both
    with warnings.catch_warnings(record=True) as w:
        fig, _ = mosaic.plot(map_extent, returnfig=True, savefig_filename="some_filename", savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "The figure will be returned, but a savefig option parameter was supplied" in str(w[-1].message)
    plt.close(fig)


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_savefig_warnings(mock_show, at, plot_cleanup, themis_mosaic_data):
    # init
    mosaic_dt = themis_mosaic_data["dt"]
    prepped_images = themis_mosaic_data["prepped_images"]
    prepped_skymaps = themis_mosaic_data["prepped_skymaps"]

    # create projection
    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # create mosaic
    mosaic = at.mosaic.create(prepped_images, prepped_skymaps, mosaic_dt, projection_obj)
    map_extent = [-145, -65, 35, 80]

    # check savefig_filename
    with warnings.catch_warnings(record=True) as w:
        mosaic.plot(map_extent, savefig_filename="some_filename")
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "A savefig option parameter was supplied, but the savefig parameter is False" in str(w[-1].message)

    # check savefig_quality
    with warnings.catch_warnings(record=True) as w:
        mosaic.plot(map_extent, savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "A savefig option parameter was supplied, but the savefig parameter is False" in str(w[-1].message)

    # check both
    with warnings.catch_warnings(record=True) as w:
        mosaic.plot(map_extent, savefig_filename="some_filename", savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "A savefig option parameter was supplied, but the savefig parameter is False" in str(w[-1].message)

    # check plots
    assert mock_show.call_count == 3


@pytest.mark.tools
def test_savefig(at, themis_mosaic_data):
    # init
    mosaic_dt = themis_mosaic_data["dt"]
    prepped_images = themis_mosaic_data["prepped_images"]
    prepped_skymaps = themis_mosaic_data["prepped_skymaps"]

    # create projection
    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # create mosaic
    mosaic = at.mosaic.create(prepped_images, prepped_skymaps, mosaic_dt, projection_obj)
    map_extent = [-145, -65, 35, 80]

    # check filename missing
    with pytest.raises(ValueError) as e_info:
        mosaic.plot(map_extent, savefig=True)
    assert "The savefig_filename parameter is missing, but required since savefig was set to True" in str(e_info)

    # regular savefig
    output_filename = "/tmp/pyaurorax_testing_%s.png" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    mosaic.plot(map_extent, savefig=True, savefig_filename=output_filename)
    assert os.path.exists(output_filename)
    os.remove(output_filename)

    # regular savefig
    output_filename = "/tmp/pyaurorax_testing_%s.jpg" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    mosaic.plot(map_extent, savefig=True, savefig_filename=output_filename)
    assert os.path.exists(output_filename)
    os.remove(output_filename)

    # savefig with quality
    output_filename = "/tmp/pyaurorax_testing_%s.jpg" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    mosaic.plot(map_extent, savefig=True, savefig_filename=output_filename, savefig_quality=90)
    assert os.path.exists(output_filename)
    os.remove(output_filename)

    # savefig with quality and not a jpg (will show warning)
    output_filename = "/tmp/pyaurorax_testing_%s.png" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    with warnings.catch_warnings(record=True) as w:
        mosaic.plot(map_extent, savefig=True, savefig_filename=output_filename, savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "The savefig_quality parameter was specified, but is only used for saving JPG files" in str(w[-1].message)
    assert os.path.exists(output_filename)
    os.remove(output_filename)


@pytest.mark.tools
def test_input_errors(at, themis_mosaic_data):
    # init
    mosaic_dt = themis_mosaic_data["dt"]
    prepped_images = themis_mosaic_data["prepped_images"]
    prepped_skymaps = themis_mosaic_data["prepped_skymaps"]

    # create projection
    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # create mosaic
    mosaic = at.mosaic.create(prepped_images, prepped_skymaps, mosaic_dt, projection_obj)

    # missing all geo contours
    with pytest.raises(ValueError) as e_info:
        mosaic.add_geo_contours()
    assert "No latitudes or longitudes provided." in str(e_info)

    # missing all mag contours
    with pytest.raises(ValueError) as e_info:
        mosaic.add_mag_contours(mosaic_dt)
    assert "No latitudes or longitudes provided." in str(e_info)

    # missing lats or lons on geo contour
    with pytest.raises(ValueError) as e_info:
        mosaic.add_geo_contours(lats=[54.0, 55.0])
    assert "Manually supplying contour requires both lats and lons." in str(e_info)

    # missing lats or lons on mag contour
    with pytest.raises(ValueError) as e_info:
        mosaic.add_mag_contours(mosaic_dt, lats=[54.0, 55.0])
    assert "Manually supplying contour requires both lats and lons." in str(e_info)

    # non-existent color
    with pytest.raises(ValueError) as e_info:
        mosaic.add_geo_contours(lats=[54.0, 55.0], lons=[-130.0, -140.0], color="some_color")
    assert "not recognized by matplotlib." in str(e_info)

    # non-existent color
    with pytest.raises(ValueError) as e_info:
        mosaic.add_mag_contours(mosaic_dt, lats=[54.0, 55.0], lons=[-130.0, -140.0], color="some_color")
    assert "not recognized by matplotlib." in str(e_info)

    # non-existent color
    with pytest.raises(ValueError) as e_info:
        mosaic.add_geo_contours(lats=[54.0, 55.0], lons=[-130.0, -140.0], linestyle="some_linestyle")
    assert "not recognized by matplotlib." in str(e_info)

    # non-existent color
    with pytest.raises(ValueError) as e_info:
        mosaic.add_mag_contours(mosaic_dt, lats=[54.0, 55.0], lons=[-130.0, -140.0], linestyle="some_linestyle")
    assert "not recognized by matplotlib." in str(e_info)

    # bad linewidth
    with pytest.raises(ValueError) as e_info:
        mosaic.add_geo_contours(lats=[54.0, 55.0], lons=[-130.0, -140.0], linewidth=-1)
    assert "Linewidth must be greater than zero." in str(e_info)

    # bad linewidth
    with pytest.raises(ValueError) as e_info:
        mosaic.add_mag_contours(mosaic_dt, lats=[54.0, 55.0], lons=[-130.0, -140.0], linewidth=-1)
    assert "Linewidth must be greater than zero." in str(e_info)

    # non-supported marker
    with pytest.raises(ValueError) as e_info:
        mosaic.add_geo_contours(lats=[54.0, 55.0], lons=[-130.0, -140.0], marker="some_marker")
    assert "not currently supported." in str(e_info)

    # non-supported marker
    with pytest.raises(ValueError) as e_info:
        mosaic.add_mag_contours(mosaic_dt, lats=[54.0, 55.0], lons=[-130.0, -140.0], marker="some_marker")
    assert "not currently supported." in str(e_info)

    # non-supported marker
    with pytest.raises(ValueError) as e_info:
        mosaic.add_geo_contours(lats=[54.0, 55.0, 69.0], lons=[-130.0, -140.0])
    assert "Lat/Lon data must be of the same size." in str(e_info)
