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
import cartopy.crs
import datetime
from pyaurorax.tools import Mosaic
from pyaurorax.exceptions import AuroraXError


@pytest.mark.tools
def test_simple(at, themis_mosaic_data, capsys):
    # init
    mosaic_dt = themis_mosaic_data["dt"]
    prepped_images = themis_mosaic_data["prepped_images"]
    prepped_skymaps = themis_mosaic_data["prepped_skymaps"]

    # create projection
    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # create mosaic
    mosaic = at.mosaic.create(prepped_images, prepped_skymaps, mosaic_dt, projection_obj, spect_cmap=["greens_r", "greens_r"])
    assert isinstance(mosaic, Mosaic) is True

    # check __str__ and __repr__ for Mosaic type
    print_str = str(mosaic)
    assert print_str != ""
    assert isinstance(str(mosaic), str) is True
    assert isinstance(repr(mosaic), str) is True
    mosaic.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.tools
def test_simple_rgb(at, trex_rgb_mosaic_data, capsys):
    # init
    mosaic_dt = trex_rgb_mosaic_data["dt"]
    prepped_images = trex_rgb_mosaic_data["prepped_images"]
    prepped_skymaps = trex_rgb_mosaic_data["prepped_skymaps"]

    # create projection
    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # create mosaic
    mosaic = at.mosaic.create(prepped_images, prepped_skymaps, mosaic_dt, projection_obj, spect_cmap=["greens_r", "greens_r"])
    assert isinstance(mosaic, Mosaic) is True

    # check __str__ and __repr__ for Mosaic type
    print_str = str(mosaic)
    assert print_str != ""
    assert isinstance(str(mosaic), str) is True
    assert isinstance(repr(mosaic), str) is True
    mosaic.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.tools
def test_cmap(at, themis_mosaic_data, capsys):
    # init
    mosaic_dt = themis_mosaic_data["dt"]
    prepped_images = themis_mosaic_data["prepped_images"]
    prepped_skymaps = themis_mosaic_data["prepped_skymaps"]

    # create projection
    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # create mosaic
    mosaic = at.mosaic.create(prepped_images,
                              prepped_skymaps,
                              mosaic_dt,
                              projection_obj,
                              cmap="gray",
                              spect_cmap="greens_r",
                              image_intensity_scales=[500, 1000])
    assert isinstance(mosaic, Mosaic) is True

    # check __str__ and __repr__ for Mosaic type
    print_str = str(mosaic)
    assert print_str != ""
    assert isinstance(str(mosaic), str) is True
    assert isinstance(repr(mosaic), str) is True
    mosaic.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.tools
def test_input_errors(at, themis_mosaic_data, capsys):
    # init
    mosaic_dt = themis_mosaic_data["dt"]
    prepped_images = themis_mosaic_data["prepped_images"]
    prepped_skymaps = themis_mosaic_data["prepped_skymaps"]

    # create projection
    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # mismatched data / skymap list lengths
    with pytest.raises(ValueError) as e_info:
        _ = at.mosaic.create([prepped_images, prepped_images], prepped_skymaps, mosaic_dt, projection_obj)
    assert "When passing lists of prepped data and prepped skymap, they must be of the same length." in str(e_info)

    # mismatched data / colormap list lengths
    with pytest.raises(ValueError) as e_info:
        _ = at.mosaic.create([prepped_images, prepped_images], [prepped_skymaps, prepped_skymaps], mosaic_dt, projection_obj, cmap="gray")
    assert "List of colormaps must have same length as lists of prepped data and prepped skymaps." in str(e_info)

    # incorrect format for scaling
    with pytest.raises(ValueError) as e_info:
        _ = at.mosaic.create(prepped_images, prepped_skymaps, mosaic_dt, projection_obj, image_intensity_scales="wrong_format")
    assert "Invalid image_intensity_scales format. Please refer to the documentation for this function." in str(e_info)

    # requested timestamp not in data
    bad_dt = datetime.datetime(2025, 1, 1, 0, 0, 0)
    with pytest.raises(ValueError) as e_info:
        _ = at.mosaic.create(prepped_images, prepped_skymaps, bad_dt, projection_obj)
    assert "Could not create mosaic for timestamp" in str(e_info) and " as image data was only supplied for the timestamp range: " in str(e_info)


@pytest.mark.tools
def test_spect_and_rgb_mosaic(at, trex_spect_mosaic_data, capsys):
    # init
    mosaic_dt = trex_spect_mosaic_data["dt"]
    prepped_images = trex_spect_mosaic_data["prepped_images"]
    prepped_skymaps = trex_spect_mosaic_data["prepped_skymaps"]

    # create projection
    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # create mosaic
    mosaic = at.mosaic.create(prepped_images, prepped_skymaps, mosaic_dt, projection_obj, spect_cmap="Greens_r")
    assert isinstance(mosaic, Mosaic) is True


@pytest.mark.tools
def test_spect_mosaic(at, trex_spect_mosaic_data, capsys):
    # init
    mosaic_dt = trex_spect_mosaic_data["dt"]
    prepped_images = trex_spect_mosaic_data["prepped_spect_images"]
    prepped_skymaps = trex_spect_mosaic_data["prepped_spect_skymaps"]

    # create projection
    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # create mosaic
    mosaic = at.mosaic.create(prepped_images, prepped_skymaps, mosaic_dt, projection_obj, spect_cmap="Greens_r")
    assert isinstance(mosaic, Mosaic) is True


@pytest.mark.tools
def test_spect_mosaic_zero_frame(at, trex_spect_mosaic_data, capsys):
    # init
    mosaic_dt = trex_spect_mosaic_data["dt"]
    prepped_images = trex_spect_mosaic_data["prepped_spect_images"]
    prepped_skymaps = trex_spect_mosaic_data["prepped_spect_skymaps"]

    # Make one of the frames full of zeros
    prepped_images.images['luck'][:, 1] *= 0.0

    # create projection
    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # create mosaic
    # incorrect format for scaling
    with pytest.raises(AuroraXError) as e_info:
        _ = at.mosaic.create(prepped_images, prepped_skymaps, mosaic_dt, projection_obj)

    assert "Images have different timestamps" in str(e_info)


@pytest.mark.tools
def test_themis_mosaic_zero_frame(at, themis_mosaic_data, capsys):
    # init
    mosaic_dt = themis_mosaic_data["dt"]
    prepped_images = themis_mosaic_data["prepped_images"]
    prepped_skymaps = themis_mosaic_data["prepped_skymaps"]

    # Make one of the frames full of zeros
    prepped_images.images["atha"][:, :, 1] *= 0.0

    # create projection
    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # create mosaic
    mosaic = at.mosaic.create(prepped_images, prepped_skymaps, mosaic_dt, projection_obj)
    assert isinstance(mosaic, Mosaic) is True
