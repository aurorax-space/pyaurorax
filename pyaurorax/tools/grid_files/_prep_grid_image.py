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
import matplotlib.pyplot as plt
from typing import Union, Optional
from .. import scale_intensity

def prep_grid_image(
    grid: np.ndarray,
    fill_val: Union[int, float] = -999.0,
    scale: Optional[Union[list, np.ndarray]] = None,
    cmap: Optional[str] = "Greys_r",
) -> np.ndarray:
    """
    Takes a grid array, and converts it to RGBA format, masking all empty cells with max
    transparency, so that it can be plotted overtop of a map.

    Args:
        grid (numpy.ndarray): 
             The grid array to prepare. Usually a result of reading a grid file and obtaining grid data from said file.
        fill_val (int or float): 
            The fill value that was used to fill grid cells containing no data. Usually obtained from the grid file's metadata.
        scale (list or numpy.ndarray): 
            A two-element vector specifying the minimum and maximum values to scale data between, optional (defaults to data min/max).
        cmap (str): 
            A string giving the name of a matplotlib colormap to prep single-channel image data using, optional (defaults to "Greys_r").

    Returns:
        The prepared RGBA grid array.

    Raises:
        ValueError: issues encountered with supplied parameters.
    """
    # Determine number of channels in grid
    if len(grid.shape) == 2:
        n_channels = 1
    elif len(grid.shape) == 3:
        n_channels = 3
    else:
        raise ValueError("Routine currently only supports grid data with shape [rows, cols] or [rows, cols, channels].")
    
    # Convert grid to int type for plotting
    if np.issubdtype(grid.dtype, np.floating):
        grid = grid.astype(int)
        
    # Check that scale input is defined properly
    if scale is not None:
        # convert list to array
        if type(scale) is not np.ndarray:
            scale = np.array(scale)
        if scale.shape[0] != 2 or len(scale) != 2:
            raise ValueError("Scale must be provided as a two-element vector, i.e. [scale_min, scale_max].")
        
    # Handle RGB data first as it is straightforward
    if n_channels == 3:
        # Replace fill values with nans
        grid = np.where(grid == fill_val, np.nan, grid)

        # Scale the image data
        if scale is None:
            scaled_grid = scale_intensity(np.where(np.isnan(grid), 0, grid), top=255, memory_saver=False)
        else:
            scaled_grid = scale_intensity(np.where(np.isnan(grid), 0, grid), min=scale[0], max=scale[1], top=255, memory_saver=False)
        
        # Add alpha channel
        alpha_channel = np.where(np.isnan(grid).any(axis=-1), 0, 255)
        rgba_grid = np.dstack((scaled_grid, alpha_channel))

        return rgba_grid.astype(int)
    
    # Handle case of single-channel data, where we build an RGBA image using a matplotlib colormap
    else:
        # Replace fill values with nans
        grid = np.where(grid == fill_val, np.nan, grid)

        # Scale the image data
        if scale is None:
            scaled_grid = scale_intensity(np.where(np.isnan(grid), 0, grid), top=255, memory_saver=False)
        else:
            scaled_grid = scale_intensity(np.where(np.isnan(grid), 0, grid), min=scale[0], max=scale[1], top=255, memory_saver=False)

        # Normalize array and apply colormap to obtain RGBA Array
        norm_scaled_grid = scaled_grid / 255.0
        colormap = plt.get_cmap(cmap)
        norm_scaled_grid = colormap(norm_scaled_grid)
        
        # 'De-normalize' array back to 8-bit range
        rgba_grid = (norm_scaled_grid * 255).astype(int)

        # Add alpha channel with max transparency for cells with no data
        alpha_channel = np.where(np.isnan(grid), 0, 255)
        rgba_grid[..., -1] = alpha_channel

        return rgba_grid