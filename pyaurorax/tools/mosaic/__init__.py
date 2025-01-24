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
"""
Prepare data and create mosaics.
"""

import datetime
import cartopy.crs
from typing import Union, Optional, List, Dict, Tuple, Literal
from ..._util import show_warning
from ...data.ucalgary import Data, Skymap
from ..classes.mosaic import MosaicData, MosaicSkymap, Mosaic
from ._prep_skymaps import prep_skymaps as func_prep_skymaps
from ._prep_images import prep_images as func_prep_images
from ._create import create as func_create

__all__ = ["MosaicManager"]


class MosaicManager:
    """
    The MosaicManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    def __init__(self, aurorax_obj):
        self.__aurorax_obj = aurorax_obj

    def create(
            self,
            prepped_data: Union[MosaicData, List[MosaicData]],
            prepped_skymap: Union[MosaicSkymap, List[MosaicSkymap]],
            timestamp: datetime.datetime,
            cartopy_projection: cartopy.crs.Projection,
            min_elevation: Union[int, List[int]] = 5,
            cmap: Optional[Union[str, List[str]]] = None,
            spect_cmap: Optional[Union[str, List[str]]] = None,
            image_intensity_scales: Optional[Union[List, Dict]] = None,
            spect_intensity_scales: Optional[Tuple[int, int]] = None,
            colormap: Optional[Union[str, List[str]]] = None,  # deprecated in v1.10.0
            spect_colormap: Optional[Union[str, List[str]]] = None,  # deprecated in v1.10.0
    ) -> Mosaic:
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

            cmap (str): 
                The matplotlib colormap to use for the rendered image data. Default is `gray`.

                Commonly used colormaps are:

                - REGO: `gist_heat`
                - THEMIS ASI: `gray`
                - TREx Blue: `Blues_r`
                - TREx NIR: `gray`
                - TREx RGB: `None`

                A list of all available colormaps can be found on the 
                [matplotlib documentation](https://matplotlib.org/stable/gallery/color/colormap_reference.html).

            colormap (str): 
                Deprecated as of v1.10.0. Use 'cmap' instead in the exact same way.

            spect_cmap (str): 
                The matplotlib colormap to use for the colorbar if working with spectrograph
                data. Default is `gnuplot`.

            image_intensity_scales (List or Dict): 
                Ranges for scaling images. Either a a list with 2 elements which will scale all sites with 
                the same range, or as a dictionary which can be used for scaling each site differently. 

                Example of uniform scaling across all sites: 
                `image_intensity_scales = [2000, 8000]`

                Example of scaling each site differently:
                `image_intensity_scales = {"fsmi": [1000, 10000], "gill": [2000, 8000]}`

            spect_intensity_scales (Tuple[int]): 
                Min and max values, in Rayleighs, to scale ALL spectrograph data.

            spect_colormap (str): 
                The name of a matplotlib colormap to use for plotting spectrograph data.

        Returns:
            The generated `pyaurorax.tools.Mosaic` object.

        Raises:
            ValueError: issues encountered with supplied parameters
            pyaurorax.exceptions.AuroraXError: general issue encountered
        """
        # handle deprecation warnings
        use_colormap = False
        use_spect_colormap = False
        if (colormap is not None):
            show_warning("The parameter 'colormap' was deprecated in v1.10.0. Please use 'cmap' instead (usage is identical).", stacklevel=1)
            use_colormap = True
        if (spect_colormap is not None):
            show_warning("The parameter 'spect_colormap' was deprecated in v1.10.0. Please use 'spect_cmap' instead (usage is identical).",
                         stacklevel=1)
            use_spect_colormap = True

        # run function
        if (use_colormap is False and use_spect_colormap is False):
            # normal
            return func_create(prepped_data, prepped_skymap, timestamp, cartopy_projection, min_elevation, cmap, spect_cmap, image_intensity_scales,
                               spect_intensity_scales)
        elif (use_colormap is True and use_spect_colormap is True):
            # both deprecated parameters were supplied
            return func_create(prepped_data, prepped_skymap, timestamp, cartopy_projection, min_elevation, colormap, spect_colormap,
                               image_intensity_scales, spect_intensity_scales)
        elif (use_colormap is True and use_spect_colormap is False):
            # one deprecated parameter was supplied (colormap)
            return func_create(prepped_data, prepped_skymap, timestamp, cartopy_projection, min_elevation, colormap, spect_cmap,
                               image_intensity_scales, spect_intensity_scales)
        else:
            # one deprecated parameter was supplied (spect_colormap)
            return func_create(prepped_data, prepped_skymap, timestamp, cartopy_projection, min_elevation, cmap, spect_colormap,
                               image_intensity_scales, spect_intensity_scales)

    def prep_images(self,
                    image_list: List[Data],
                    data_attribute: Literal["data", "calibrated_data"] = "data",
                    spect_emission: Literal["green", "red", "blue", "hbeta"] = "green",
                    spect_band: Optional[Tuple[float, float]] = None,
                    spect_band_bg: Optional[Tuple[float, float]] = None) -> MosaicData:
        """
        Prepare the image data for use in a mosaic.

        Args:
            image_list (List[pyaurorax.data.ucalgary.Data]): 
                List of image data. Each element of the list is the data for each site.
            
            data_attribute (str): 
                The data attribute to use when prepping the images. Either `data` or `calibrated_data`. 
                Default is `data`.

            spect_emission (str): 
                The emission (green, red, blue, hbeta) to prepare from spectrograph data. Default is 
                'green' (557.7 nm emission).

            spect_band (Tuple[float]): 
                Manual selection of the wavelength region to integrate for obtaining emissions. Use this
                to prepare emissions that are not available in spect_emission.

            spect_band_bg (Tuple[float]): 
                Manual selection of the wavelength region to subtract from integration for manually
                chosen emissions, via the spect_band argument.

        Returns:
            The prepared data, as a `pyaurorax.tools.MosaicData` object.

        Raises:
            ValueError: issues encountered with supplied parameters
        """
        return func_prep_images(image_list, data_attribute, spect_emission, spect_band, spect_band_bg)

    def prep_skymaps(self,
                     skymaps: List[Skymap],
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
            ValueError: issues encountered with supplied parameters
        """
        return func_prep_skymaps(self.__aurorax_obj, skymaps, height_km, site_uid_order, progress_bar_disable, n_parallel)
