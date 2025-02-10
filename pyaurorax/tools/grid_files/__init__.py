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
Prepare grid data for plotting.
"""

import numpy as np
from typing import Optional, Union
from ._prep_grid_image import prep_grid_image as func_prep_grid_image

__all__ = ["GridFilesManager"]


class GridFilesManager:
    """
    The GridFilesManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    def __init__(self, aurorax_obj):
        self.__aurorax_obj = aurorax_obj

    def prep_grid_image(
        self,
        grid: np.ndarray,
        fill_val: Union[int, float] = -999.0,
        scale: Optional[Union[list, np.ndarray]] = None,
        cmap: Optional[str] = "Greys_r",
    ) -> np.ndarray:
        """
        Takes a grid image, and converts it to RGBA format, masking all empty cells with max
        transparency, so that it can be plotted overtop of a map.

        NOTE: the grid data passed in must be for a single grid image. Multiple images in a single
        call to this function is presently not supported.

        Args:
            grid (numpy.ndarray): 
                The grid array to prepare. Usually a result of reading a grid file and obtaining grid data from 
                said file. 
                
                Please note that the data must be a single frame; multiple frames are currently not supported.

            fill_val (int or float): 
                The fill value that was used to fill grid cells containing no data. Usually obtained from the 
                grid file's metadata.

            scale (list or numpy.ndarray): 
                A two-element vector specifying the minimum and maximum values to scale data between. This parameter
                is optional. Defaults to data min/max.

            cmap (str): 
                A string giving the name of a matplotlib colormap to prep single-channel image data using. This parameter
                is optional. Defaults to "Greys_r".

        Returns:
            The prepared RGBA grid array.

        Raises:
            ValueError: issues encountered with supplied parameters
        """
        return func_prep_grid_image(self.__aurorax_obj, grid, fill_val, scale, cmap)
