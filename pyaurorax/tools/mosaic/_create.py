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

import numpy as np
import pyproj
import datetime
import cartopy.crs
import cartopy.feature
import matplotlib.pyplot as plt
import matplotlib.collections
from typing import Optional, Union, Dict, List, Tuple
from ..classes.mosaic import Mosaic, MosaicData, MosaicSkymap
from .._scale_intensity import scale_intensity

# globals
__DEFAULT_SCALE_MIN = 0
__DEFAULT_SCALE_MAX = 20000
__DEFAULT_SPECT_SCALE_MIN = 0
__DEFAULT_SPECT_SCALE_MAX = 5000


def create(prepped_data: Union[MosaicData, List[MosaicData]],
           prepped_skymap: Union[MosaicSkymap, List[MosaicSkymap]],
           timestamp: datetime.datetime,
           cartopy_projection: cartopy.crs.Projection,
           min_elevation: Union[int, List[int]] = 5,
           colormap: Optional[Union[str, List[str]]] = None,
           spect_colormap: Optional[Union[str, List[str]]] = None,
           image_intensity_scales: Optional[Union[List, Dict]] = None,
           spect_intensity_scales: Optional[Tuple[int, int]] = None) -> Mosaic:
    """
    Create a mosaic object.

    Args:
        prepped_data (pyaurorax.tools.MosaicData): 
            The prepared mosaic data. Generated from a prior `prep_images()` function call.

        prepped_skymap (pyaurorax.tools.MosaicSkymap): 
            The prepared skymap data. Generated from a prior `prep_skymaps()` function call.

        timestamp (datetime.datetime): 
            The timestamp to generate a mosaic for. Must be within the range of timestamps
            for which image data was prepped and provided.

        cartopy_projection (cartopy.crs.Projection): 
            The cartopy projection to use when creating the mosaic.

        min_elevation (int): 
            The minimum elevation cutoff when projecting images on the map, in degrees. Default is `5`.

        colormap (str): 
            The matplotlib colormap to use for the rendered image data. Default is `gray`.

            Commonly used colormaps are:

            - REGO: `gist_heat`
            - THEMIS ASI: `gray`
            - TREx Blue: `Blues_r`
            - TREx NIR: `gray`
            - TREx RGB: `None`

            A list of all available colormaps can be found on the 
            [matplotlib documentation](https://matplotlib.org/stable/gallery/color/colormap_reference.html).

        spect_cmap (str): 
            The matplotlib colormap to use for the colorbar if working with spectrograph
            data. Default is `gnuplot`.

        image_intensity_scaled (List or Dict): 
            Ranges for scaling images. Either a a list with 2 elements which will scale all sites with 
            the same range, or as a dictionary which can be used for scaling each site differently. 

            Example of uniform scaling across all sites: 
            `image_intensity_scales = [2000, 8000]`

            Example of scaling each site differently:
            `image_intensity_scales = {"fsmi": [1000, 10000], "gill": [2000, 8000]}`

        spect_intensity_scaled (Tuple[int]): 
            Min and max values, in Rayleighs, to scale ALL spectrograph data.

    Returns:
        The generated `pyaurorax.tools.Mosaic` object.

    Raises:
        ValueError: issues with supplied parameters.
    """
    # init coordinates transformer
    #
    # To convert from geodetic coordinates onto the map projection, we use pyproj instead
    # of cartopy's native transformations. This is an optimization.
    pyproj_src_proj = pyproj.CRS.from_user_input(cartopy.crs.Geodetic())
    pyproj_des_proj = pyproj.CRS.from_user_input(cartopy_projection)
    transformer = pyproj.Transformer.from_crs(pyproj_src_proj, pyproj_des_proj, always_xy=True)

    # Convert data, skymaps, colormap indicators to lists for iteration purposed
    if not isinstance(prepped_data, list):
        prepped_data = [prepped_data]
    if not isinstance(prepped_skymap, list):
        prepped_skymap = [prepped_skymap]
    if not isinstance(colormap, list):
        if colormap is None:
            colormap = []
            for _ in range(len(prepped_data)):
                colormap.append('gray')
        else:
            colormap = [colormap]
    if not isinstance(min_elevation, list):
        tmp = []
        for _ in range(len(prepped_data)):
            tmp.append(min_elevation)
        min_elevation = tmp
    if spect_intensity_scales is None:
        spect_intensity_scales = (__DEFAULT_SPECT_SCALE_MIN, __DEFAULT_SPECT_SCALE_MAX)

    # Make sure all lists are same length
    if (len(prepped_data) != len(prepped_skymap)):
        raise ValueError("When passing lists of prepped data and prepped skymap, they must be of the same length.")
    if (len(prepped_data) != len(colormap)) or (len(prepped_skymap) != len(colormap)):
        raise ValueError("List of colormaps must have same length as lists of prepped data and prepped skymaps.")

    # Itarate through each set of prepped data, prepped skymap
    img_poly_list = []
    any_spect_data = False
    for mosaic_data_idx in range(len(prepped_data)):
        data = prepped_data[mosaic_data_idx]
        skymap = prepped_skymap[mosaic_data_idx]
        iter_cmap = colormap[mosaic_data_idx]
        min_el = min_elevation[mosaic_data_idx]

        if spect_colormap is None:
            iter_spect_cmap = 'gnuplot2'
        else:
            iter_spect_cmap = spect_colormap

        if isinstance(iter_spect_cmap, list):
            iter_spect_cmap = iter_spect_cmap[0]
        # get sites
        site_list = data.site_uid_list

        # set image intensity scales
        if (image_intensity_scales is None):
            # defaults to scaling all sites between 0-20000
            image_intensity_scales = {}
            for site_uid in skymap.site_uid_list:
                image_intensity_scales[site_uid] = [__DEFAULT_SCALE_MIN, __DEFAULT_SCALE_MAX]
        elif (isinstance(image_intensity_scales, list) is True):
            image_intensity_scales_dict = {}
            for site_uid in site_list:
                image_intensity_scales_dict[site_uid] = image_intensity_scales
            image_intensity_scales = image_intensity_scales_dict
        elif (isinstance(image_intensity_scales, dict) is True):
            # no action needed
            pass
        else:
            raise ValueError("Invalid image_intensity_scales format. Please refer to the documentation for this function.")

        # We need a numpy array of the sites requested, that will be used to make sure any sites
        # that don't have data for the requested frame are not plotted. Also empty dict for images..
        site_list_arr = np.array(site_list)
        # all_images = np.zeros([len(site_list), width * height, __N_CHANNELS], dtype=np.int32)
        all_images = {}

        # Grab the elevation, and filling lats/lons
        elev = skymap.elevation
        polyfill_lon = skymap.polyfill_lon
        polyfill_lat = skymap.polyfill_lat

        # Now we begin to fill in the above arrays, one site at a time. Before doing so
        # we need lists to keep track of which sites actually have data for this frame.
        sites_with_data = []
        sites_with_data_idx = []
        datatypes_with_data = []

        # Determine the frame index of data the corresponds to the requested timestamp
        minimum_timestamp = (np.array(data.timestamps))[np.argmin(np.array(data.timestamps))]
        maximum_timestamp = (np.array(data.timestamps))[np.argmax(np.array(data.timestamps))]
        if timestamp < minimum_timestamp or timestamp > maximum_timestamp:
            raise ValueError("Could not create mosaic for timestamp" + timestamp.strftime("%Y/%m/%d %H:%M:%S") +
                             " as image data was only supplied for the timestamp range: " + minimum_timestamp.strftime("%Y/%m/%d %H:%M:%S") + " to " +
                             maximum_timestamp.strftime("%Y/%m/%d %H:%M:%S"))

        # Get the frame index of the timestamp closest to desired mosaic frame
        frame_idx = np.argmin(np.abs(np.array(data.timestamps) - timestamp))

        # We also define a list that will hold all unique timestamps pulled from each
        # frame's metadata. This should be of length 1, and we can check that to make
        # sure all images being plotted correspond to the same time.
        unique_timestamps = []
        n_channels_dict = {}
        for idx_for_dataype, site in enumerate(site_list):

            # set image dimensions
            height = data.images_dimensions[site][0]
            width = data.images_dimensions[site][1]

            # Grab the timestamp for this frame/site
            meta_timestamp = data.timestamps[frame_idx]

            # Determine whether current image is single or multi-channel, and add to dictionary for reference
            if len(data.images[site].shape) == 4:
                n_channels = data.images[site].shape[2]
            else:
                n_channels = 1
            n_channels_dict[site] = n_channels

            # Now, obtain the frame of interest, for this site, from the image data and flatten it
            if data.data_types[idx_for_dataype] == 'spect':
                any_spect_data = True
                rayleighs = data.images[site][:, frame_idx]
                flattened_rayleighs = np.reshape(rayleighs, height)

                tmp = flattened_rayleighs

                if (np.sum(tmp) == 0.0):
                    # If it's sum is zero, we know there is no data so we can simply continue.
                    continue

                # Scale this site's data based on previously defined scaling bounds
                tmp = scale_intensity(
                    tmp,
                    min=spect_intensity_scales[0],  # type: ignore
                    max=spect_intensity_scales[1],  # type: ignore
                    top=255,
                    memory_saver=False,
                )

            else:
                if n_channels == 1:
                    img = data.images[site][:, :, frame_idx]
                    flattened_img = np.reshape(img, (width * height))
                else:
                    img = data.images[site][:, :, :, frame_idx]
                    flattened_img = np.reshape(img, (width * height, n_channels))

                tmp = flattened_img

                if (np.sum(tmp) == 0.0):
                    # If it's sum is zero, we know there is no data so we can simply continue.
                    continue

                # Scale this site's data based on previously defined scaling bounds
                tmp = scale_intensity(
                    tmp,
                    min=image_intensity_scales[site][0],  # type: ignore
                    max=image_intensity_scales[site][1],  # type: ignore
                    top=255,
                    memory_saver=False,
                )

            # Add the timestamp to tracking list if it's unique
            if meta_timestamp not in unique_timestamps:
                unique_timestamps.append(meta_timestamp)

            # Append sites to respective lists, and add image data to master list
            datatypes_with_data.append(data.data_types[idx_for_dataype])
            sites_with_data.append(site)
            sites_with_data_idx.append(np.where(site_list_arr == site)[0][0])
            all_images[site] = tmp.astype(np.int32)

        # This checks to make sure all images have the same timestamps
        if len(unique_timestamps) != 1:
            raise Exception("Error: Images have different timestamps.")

        # Create empty lists for tracking the pixel polygons and their values
        lon_list = []
        lat_list = []
        cmap_vals = []

        # Set up elevation increment for plotting. We start at the min elevation
        # and plot groups of elevations until reaching 90 deg.
        elev_delta = 0.1
        el = min_el

        # Iterate through all elevation ranges - Always do ASI data first !
        while el < 90:

            # Only iterate through the sites that actually have data
            for site_id, site_idx in zip(sites_with_data, sites_with_data_idx):

                # Skip spectrograph data for now as that should always be plotted last
                if datatypes_with_data[site_idx] == 'spect':
                    continue

                if spect_colormap is None:
                    spect_colormap = iter_spect_cmap

                # Get this sites number of channels
                n_channels = n_channels_dict[site_id]

                # Get all pixels within current elevation threshold
                el_idx = np.nonzero(np.logical_and(elev[site_idx] > el, elev[site_idx] <= el + elev_delta))[0]
                if len(el_idx) == 0:
                    continue

                # Grab this level's filling lat/lons
                el_lvl_fill_lats = polyfill_lat[site_idx][:, el_idx]
                el_lvl_fill_lons = polyfill_lon[site_idx][:, el_idx]

                # Grab this level's data values
                if n_channels == 1:
                    el_lvl_cmap_vals = all_images[site_id][el_idx]
                else:
                    el_lvl_cmap_vals = all_images[site_id][el_idx, :]

                # # Mask any nans that may have slipped through - done as a precaution
                nan_mask = ~np.isnan(el_lvl_fill_lats).any(axis=0) & ~np.isnan(el_lvl_fill_lons).any(axis=0)

                el_lvl_fill_lats = el_lvl_fill_lats[:, nan_mask]
                el_lvl_fill_lons = el_lvl_fill_lons[:, nan_mask]
                if n_channels == 1:
                    el_lvl_cmap_vals = el_lvl_cmap_vals[nan_mask]
                else:
                    el_lvl_cmap_vals = el_lvl_cmap_vals[nan_mask, :]

                # Convert pixel values to a normalized float
                el_lvl_colors = el_lvl_cmap_vals.astype(np.float32) / 255.0

                # Append polygon lat/lons and values to master lists
                if n_channels == 1:
                    cmap = plt.get_cmap(iter_cmap)
                    for k in range(len(el_lvl_fill_lats[0, :])):
                        lon_list.append(el_lvl_fill_lons[:, k])
                        lat_list.append(el_lvl_fill_lats[:, k])
                        cmap_vals.append(cmap(el_lvl_colors[k]))
                else:
                    for k in range(len(el_lvl_fill_lats[0, :])):
                        lon_list.append(el_lvl_fill_lons[:, k])
                        lat_list.append(el_lvl_fill_lats[:, k])
                        cmap_vals.append(el_lvl_colors[k, :])

            el += elev_delta

        # Repeat the above, but for spectrograph data now
        el = min_el
        while el < 90:

            # Only iterate through the sites that actually have data
            for site_id, site_idx in zip(sites_with_data, sites_with_data_idx):

                # Skip spectrograph data for now as that should always be plotted last
                if datatypes_with_data[site_idx] != 'spect':
                    continue

                # Get this sites number of channels
                n_channels = n_channels_dict[site_id]

                # Get all pixels within current elevation threshold
                el_idx = np.nonzero(np.logical_and(elev[site_idx] > el, elev[site_idx] <= el + elev_delta))[0]
                if len(el_idx) == 0:
                    continue

                # Grab this level's filling lat/lons
                el_lvl_fill_lats = polyfill_lat[site_idx][:, el_idx]
                el_lvl_fill_lons = polyfill_lon[site_idx][:, el_idx]

                # Grab this level's data values
                if n_channels == 1:
                    el_lvl_cmap_vals = all_images[site_id][el_idx]
                else:
                    el_lvl_cmap_vals = all_images[site_id][el_idx, :]

                # # Mask any nans that may have slipped through - done as a precaution
                nan_mask = ~np.isnan(el_lvl_fill_lats).any(axis=0) & ~np.isnan(el_lvl_fill_lons).any(axis=0)

                el_lvl_fill_lats = el_lvl_fill_lats[:, nan_mask]
                el_lvl_fill_lons = el_lvl_fill_lons[:, nan_mask]
                if n_channels == 1:
                    el_lvl_cmap_vals = el_lvl_cmap_vals[nan_mask]
                else:
                    el_lvl_cmap_vals = el_lvl_cmap_vals[nan_mask, :]

                # Convert pixel values to a normalized float
                el_lvl_colors = el_lvl_cmap_vals.astype(np.float32) / 255.0

                # Append polygon lat/lons and values to master lists
                if n_channels == 1:
                    cmap = plt.get_cmap(iter_spect_cmap)
                    for k in range(len(el_lvl_fill_lats[0, :])):
                        lon_list.append(el_lvl_fill_lons[:, k])
                        lat_list.append(el_lvl_fill_lats[:, k])
                        cmap_vals.append(cmap(el_lvl_colors[k]))
                else:
                    for k in range(len(el_lvl_fill_lats[0, :])):
                        lon_list.append(el_lvl_fill_lons[:, k])
                        lat_list.append(el_lvl_fill_lats[:, k])
                        cmap_vals.append(el_lvl_colors[k, :])

            el += elev_delta

        # Use our transformer object to convert the lat/lon polygons into projection coordinates.
        lons, lats = transformer.transform(np.array(lon_list), np.array(lat_list))

        # Format polygons for creation of PolyCollection object
        lonlat_polygons = np.empty((lons.shape[0], 5, 2))
        lonlat_polygons[:, :, 0] = lons
        lonlat_polygons[:, :, 1] = lats

        # generate a PolyCollection object, containing all of the Polygons shaded with
        # their corresponding RGB value

        img_data_poly = matplotlib.collections.PolyCollection(
            lonlat_polygons,  # type: ignore
            facecolors=cmap_vals,
            array=None,
            clim=[0.0, 1.0],
            edgecolors="face",
        )

        img_poly_list.append(img_data_poly)

    if isinstance(spect_colormap, list):
        spect_colormap = spect_colormap[0]

    # cast into mosaic object
    if any_spect_data:
        if len(img_poly_list) == 1:
            mosaic = Mosaic(polygon_data=img_poly_list[0],
                            cartopy_projection=cartopy_projection,
                            spect_cmap=spect_colormap,
                            spect_intensity_scale=spect_intensity_scales)
        else:
            mosaic = Mosaic(polygon_data=img_poly_list,
                            cartopy_projection=cartopy_projection,
                            spect_cmap=spect_colormap,
                            spect_intensity_scale=spect_intensity_scales)
    else:
        if len(img_poly_list) == 1:
            mosaic = Mosaic(polygon_data=img_poly_list[0], cartopy_projection=cartopy_projection)
        else:
            mosaic = Mosaic(polygon_data=img_poly_list, cartopy_projection=cartopy_projection)
    # return
    return mosaic
