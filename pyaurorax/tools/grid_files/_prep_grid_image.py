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


def prep_grid_image(aurorax_obj, grid, fill_val, scale, cmap):
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
        if (isinstance(scale, tuple) or isinstance(scale, list)):
            scale = np.asarray(scale)
        elif (isinstance(scale, int) or isinstance(scale, float)):
            raise ValueError("Scale must be provided as a two-element vector, i.e. [scale_min, scale_max].")
        if len(scale) != 2:
            raise ValueError("Scale must be provided as a two-element vector, i.e. [scale_min, scale_max].")

    # Handle RGB data first as it is straightforward
    if n_channels == 3:
        # Replace fill values with nans
        grid = np.where(grid == fill_val, np.nan, grid)

        # Scale the image data
        if scale is None:
            scaled_grid = aurorax_obj.tools.scale_intensity(np.where(np.isnan(grid), 0, grid), top=255, memory_saver=False)
        else:
            scaled_grid = aurorax_obj.tools.scale_intensity(np.where(np.isnan(grid), 0, grid),
                                                            min=scale[0],
                                                            max=scale[1],
                                                            top=255,
                                                            memory_saver=False)

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
            scaled_grid = aurorax_obj.tools.scale_intensity(np.where(np.isnan(grid), 0, grid), top=255, memory_saver=False)
        else:
            scaled_grid = aurorax_obj.tools.scale_intensity(np.where(np.isnan(grid), 0, grid),
                                                            min=scale[0],
                                                            max=scale[1],
                                                            top=255,
                                                            memory_saver=False)

        # Normalize array and apply colormap to obtain RGBA Array
        norm_scaled_grid = scaled_grid / 255.0
        colormap = plt.get_cmap(cmap)
        norm_scaled_grid = colormap(norm_scaled_grid)

        # 'De-normalize' array back to 8-bit range
        rgba_grid = (norm_scaled_grid * 255).astype(int)

        # Add alpha channel with max transparency for cells with no data
        alpha_channel = np.where(np.isnan(grid), 0, 255)
        rgba_grid[..., -1] = alpha_channel

        # return
        return rgba_grid
