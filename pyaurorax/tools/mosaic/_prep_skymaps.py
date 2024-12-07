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
from tqdm.auto import tqdm
from tqdm.contrib.concurrent import process_map as tqdm_process_map
from concurrent.futures import ProcessPoolExecutor
from typing import List, Optional
from ...data.ucalgary import Skymap
from ..classes.mosaic import MosaicSkymap

SPECT_WIDTH_DEG = 1.0


def __flatten_skymap(processing_dict):
    # init
    skymap = processing_dict["skymap"]
    height_km = processing_dict["height_km"]
    i = processing_dict["i"]

    # set image dimensions and number of sites
    if skymap.project_uid == 'spect':
        height = skymap.full_elevation.shape[0]

        # grab the necessary data from the skymap
        altitudes = skymap.full_map_altitude
        lats = skymap.full_map_latitude
        tmp_lons = np.array(skymap.full_map_longitude)
        tmp_lons[np.where(tmp_lons > 180)] -= 360
        lons = tmp_lons.copy()
        elev = skymap.full_elevation

        # Create this site's filling arrays
        polyfill_lon = np.zeros([5, height])
        polyfill_lat = np.zeros([5, height])

        # Convert altitudes to km for interpolation
        interpol_alts = altitudes / 1000

        for ii in range(0, height - 1):

            # Interpolate lats / lons
            lon1 = np.interp(height_km, interpol_alts, lons[:, ii])
            lon2 = np.interp(height_km, interpol_alts, lons[:, ii + 1])

            lat1 = np.interp(height_km, interpol_alts, lats[:, ii])
            lat2 = np.interp(height_km, interpol_alts, lats[:, ii + 1])

            # Get estimates of pixel corners based on spectrograph width in degrees
            pix_lons = np.array([
                lon1 - (SPECT_WIDTH_DEG / 2.0), lon2 - (SPECT_WIDTH_DEG / 2.0), lon2 + (SPECT_WIDTH_DEG / 2.0), lon1 + (SPECT_WIDTH_DEG / 2.0),
                lon1 - (SPECT_WIDTH_DEG / 2.0)
            ])
            pix_lats = np.array([lat1, lat2, lat2, lat1, lat1])

            if np.isnan(np.array(pix_lats)).any():
                # Skip any nans, as we only fill pixels with 4 finite corners
                continue

            # Insert into arrays
            polyfill_lon[:, ii] = pix_lons
            polyfill_lat[:, ii] = pix_lats

        # return
        return {
            "polyfill_lon": polyfill_lon,
            "polyfill_lat": polyfill_lat,
            "elevation": elev,
            "i": i,
        }

    else:

        height = skymap.full_elevation.shape[0]
        width = skymap.full_elevation.shape[1]

        # grab the necessary data from the skymap
        altitudes = skymap.full_map_altitude
        lats = skymap.full_map_latitude
        tmp_lons = np.array(skymap.full_map_longitude)
        tmp_lons[np.where(tmp_lons > 180)] -= 360
        lons = tmp_lons.copy()
        elev = skymap.full_elevation

        # Create this site's filling arrays
        site_polyfill_lon = np.zeros([5, height, width])
        site_polyfill_lat = np.zeros([5, height, width])

        # Convert altitudes to km for interpolation
        interpol_alts = altitudes / 1000

        # iterate through each image pixel
        for ii in range(0, height - 1):
            for jj in range(0, width - 1):

                if np.isnan(elev[ii, jj]):
                    continue

                # NOTE: Should skip interpolation if using default altitude for efficiency - for
                # now its fine grab the longitudes of the corners of this pixel, at all three
                # assumed altitudes included in the skymap, and then use interpolation to obtain
                # the pixel corner coordinates at the input height. Then add this array of
                # coordinates (polygon) to the filling array.
                lon1 = np.interp(height_km, interpol_alts, lons[:, ii, jj])
                lon2 = np.interp(height_km, interpol_alts, lons[:, ii, jj + 1])
                lon3 = np.interp(height_km, interpol_alts, lons[:, ii + 1, jj + 1])
                lon4 = np.interp(height_km, interpol_alts, lons[:, ii + 1, jj])
                pix_lons = np.array([lon1, lon2, lon3, lon4, lon1])
                if np.isnan(pix_lons).any():
                    # Skip any nans, as we only fill pixels with 4 finite corners
                    continue

                # repeat the above for latitudes.
                lat1 = np.interp(height_km, interpol_alts, lats[:, ii, jj])
                lat2 = np.interp(height_km, interpol_alts, lats[:, ii, jj + 1])
                lat3 = np.interp(height_km, interpol_alts, lats[:, ii + 1, jj + 1])
                lat4 = np.interp(height_km, interpol_alts, lats[:, ii + 1, jj])
                pix_lats = np.array([lat1, lat2, lat3, lat4, lat1])
                if np.isnan(np.array(pix_lats)).any():
                    # Skip any nans, as we only fill pixels with 4 finite corners
                    continue

                site_polyfill_lon[:, ii, jj] = pix_lons
                site_polyfill_lat[:, ii, jj] = pix_lats

        # Flatten this site's filling and elevation arrays and insert them into master arrays
        polyfill_lon = np.reshape(site_polyfill_lon, (5, width * height))
        polyfill_lat = np.reshape(site_polyfill_lat, (5, width * height))
        elevation = np.reshape(elev, (width * height))

        # return
        return {
            "polyfill_lon": polyfill_lon,
            "polyfill_lat": polyfill_lat,
            "elevation": elevation,
            "i": i,
        }


def prep_skymaps(skymaps: List[Skymap],
                 height_km: int,
                 site_uid_order: Optional[List[str]] = None,
                 progress_bar_disable: bool = False,
                 n_parallel: int = 1) -> MosaicSkymap:
    """
    Prepare skymap data for use by the mosaic routine. This is not time-dependent, so it 
    would only need to be done once.

    Allows for plotting multiple images on a map, masking the boundaries between 
    images by elevation angle.

    Args:
        skymaps (List[pyaurorax.data.ucalgary.Skymap]): 
            The skymaps to prep.
        
        height_km (int): 
            The altitude to utilize, in kilometers.
        
        site_uid_order (List[str]): 
            The site list order. The order of this list is not important for plotting, but must be
            consistent with the order of the `skymaps` parameter.
        
        progress_bar_disable (bool): 
            Disable the progress bar. Defaults to `False`.

        n_parallel (int): 
            Number of skymaps to prepare in parallel using multiprocessing. Default is `1`. 

    Returns:
        The prepared skymap data as a `pyaurorax.tools.MosaicSkymap` object.
        
    Raises:
        ValueError: issues encountered with supplied parameters.
    """
    # reorder the skymap list based on the site_uid_list supplied
    skymaps_sorted = []
    site_uid_list = []
    if (site_uid_order is not None):
        # need to specifically order the skymaps
        #
        # NOTE: can do an optimization here, but with only a few items
        # ever in this list, it doesn't matter. A O(N)^2 routine is
        # good enough.
        for site_uid in site_uid_order:
            for skymap in skymaps:
                if (site_uid == skymap.site_uid):
                    skymaps_sorted.append(skymap)
                    site_uid_list.append(site_uid)
        if (len(skymaps_sorted) != len(skymaps)):
            raise ValueError("Number of items in supplied skymaps and site_uid_order lists do not match, or " +
                             "some site_uids specified in the order were not found. Unable to flatten skymaps due to this mismatch.")
    else:
        site_uid_list = [x.site_uid for x in skymaps]
        skymaps_sorted = skymaps

    # define empty numpy arrays for the lats, lons, and elevation angles of all of
    # the sites. Also define numpy arrays for 'filling' the pixel coordinates, which
    # will contain polygons vertices in lat/lon.
    elevation = []
    polyfill_lat = []
    polyfill_lon = []
    for skymap in skymaps_sorted:
        if skymap.project_uid == 'spect':
            elevation.append(np.zeros((skymap.full_elevation.shape[0])))
            polyfill_lat.append(np.zeros((5, skymap.full_elevation.shape[0])))
            polyfill_lon.append(np.zeros((5, skymap.full_elevation.shape[0])))
        else:
            elevation.append(np.zeros((skymap.full_elevation.shape[0] * skymap.full_elevation.shape[1])))
            polyfill_lat.append(np.zeros((5, skymap.full_elevation.shape[0] * skymap.full_elevation.shape[1])))
            polyfill_lon.append(np.zeros((5, skymap.full_elevation.shape[0] * skymap.full_elevation.shape[1])))

    # set up processing objects
    processing_dicts = []
    for i in range(0, len(skymaps_sorted)):
        processing_dicts.append({
            "skymap": skymaps_sorted[i],
            "height_km": height_km,
            "i": i,
        })

    if (n_parallel == 1):
        # don't do anything special, just a basic loop
        if (progress_bar_disable is True):
            # no progress bar
            for processing_dict in processing_dicts:
                results_dict = __flatten_skymap(processing_dict)
                elevation[results_dict["i"]] = results_dict["elevation"]
                polyfill_lon[results_dict["i"]] = results_dict["polyfill_lon"]
                polyfill_lat[results_dict["i"]] = results_dict["polyfill_lat"]
        else:
            # with progress bar
            for processing_dict in tqdm(processing_dicts, desc="Preparing skymaps: ", unit="skymap"):
                results_dict = __flatten_skymap(processing_dict)
                elevation[results_dict["i"]] = results_dict["elevation"]
                polyfill_lon[results_dict["i"]] = results_dict["polyfill_lon"]
                polyfill_lat[results_dict["i"]] = results_dict["polyfill_lat"]
    else:
        # multiple workers, do it in a multiprocessing loop
        if (progress_bar_disable is True):
            with ProcessPoolExecutor(max_workers=n_parallel) as executor:
                for results_dict in executor.map(__flatten_skymap, processing_dicts):
                    elevation[results_dict["i"]] = results_dict["elevation"]
                    polyfill_lon[results_dict["i"]] = results_dict["polyfill_lon"]
                    polyfill_lat[results_dict["i"]] = results_dict["polyfill_lat"]
        else:
            results_dicts = tqdm_process_map(
                __flatten_skymap,
                processing_dicts,
                max_workers=n_parallel,
                chunksize=1,
                desc="Preparing skymaps: ",
                unit="skymap",
                tqdm_class=tqdm,
            )
            for results_dict in results_dicts:
                elevation[results_dict["i"]] = results_dict["elevation"]
                polyfill_lon[results_dict["i"]] = results_dict["polyfill_lon"]
                polyfill_lat[results_dict["i"]] = results_dict["polyfill_lat"]

    # cast data into object
    flattened_skymap = MosaicSkymap(
        elevation=elevation,
        polyfill_lat=polyfill_lat,
        polyfill_lon=polyfill_lon,
        site_uid_list=site_uid_list,
    )

    # return
    return flattened_skymap
