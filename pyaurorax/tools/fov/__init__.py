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
Obtain FoVs of ASIs and create plots.
"""

import cartopy.crs
from typing import Optional, List, Literal, Tuple, Union
from ..classes.fov import FOVData, FOV
from ._create_data import create_data as func_create_data
from ._create_map import create_map as func_create_map

__all__ = ["FOVManager"]


class FOVManager:
    """
    The FOVManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    def __init__(self, aurorax_obj):
        self.__aurorax_obj = aurorax_obj

    def create_map(self, cartopy_projection: cartopy.crs.Projection, fov_data: Optional[Union[FOVData, List[FOVData]]] = None) -> FOV:
        """
        Create a FOV object.

        Args:
            
            cartopy_projection (cartopy.crs.Projection): 
                The cartopy projection to use when creating the FoV map.

            fov_data (pyaurorax.tools.FOVData): 
                A single or list of FOVData objects, that will be added to the
                FOV object map upon initialization. Otherwise the object will be
                created without any associated data (an empty map).

        Returns:
            The generated `pyaurorax.tools.FOV` object.

        Raises:
            ValueError: issues encountered with supplied parameters
            pyaurorax.exceptions.AuroraXError: general issue encountered
        """
        return func_create_map(cartopy_projection, fov_data)

    def create_data(self,
                    sites: Optional[Union[Union[str, Tuple[str, float, float]], List[Union[str, Tuple[str, float, float]]]]] = None,
                    instrument_array: Optional[Literal["themis_asi", "rego", "trex_rgb", "trex_nir", "trex_blue", "trex_spectrograph",
                                                       "smile_asi"]] = None,
                    height_km: Optional[float] = None,
                    min_elevation: float = 5,
                    color: str = 'black',
                    linewidth: int = 1,
                    linestyle: str = '-') -> FOVData:
        """
        Prepare FOV data for use.

        Args:
            
            sites (list of str or tuples): 
                The sites to be included in the FOVData object. Can be passed as a list of either one of or both of site_uid strings and/or
                ('uid', lat, lon) tuples. If passing lone site_uid strings, the instrument_array argument must be provided.

            instrument_array (str): 
                The instrument array name to add FOVs for each site (e.g. 'themis_asi' or 'smile_asi')
            
            height_km (float): 
                The altitude to map the FoVs at, in kilometers. Defaults to 110, unless instrument_array='rego', in which case the
                altitude defaults to 230.

            min_elevation (float): 
                The minimum elevation for which the FoV is defined, in degrees. Default is 5.

            color (str): 
                String giving the matplotlib color to use for plotting this FOVData. Default is 'black'.

            linewidth (int): 
                Gives the linewidth used for plotting this FOVData. Default is 1.

            linestyle (str): 
                Matplotlib formatting string specifying the linestyle for plotting FOVData. Default is '-' (solid line).

        Returns:
            The 'prepared data, as a `pyaurorax.tools.FOVData` object.'

        Raises:
            ValueError: issues encountered with supplied parameters
        """
        return func_create_data(self.__aurorax_obj,
                                sites=sites,
                                instrument_array=instrument_array,
                                height_km=height_km,
                                min_elevation=min_elevation,
                                color=color,
                                linewidth=linewidth,
                                linestyle=linestyle)
