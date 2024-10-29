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
Class representation for a montage.
"""

import os
import datetime
import warnings
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from typing import List, Optional, Tuple, Any


@dataclass
class Montage:
    """
    Class representation for a montage

    Attributes:
        data (numpy.ndarray): 
            The derived montage data.

        timestamp (List[datetime.datetime]): 
            Timestamps corresponding to each montage image.
    """

    def __init__(self, data: np.ndarray, timestamp: List[datetime.datetime], n_channels: int):
        # public vars
        self.data = data
        self.timestamp = timestamp

        # private vars
        self.__n_channels = n_channels

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        data_str = "array(dims=%s, dtype=%s)" % (self.data.shape, self.data.dtype)
        timestamp_str = "[%d datetime objects]" % (len(self.timestamp))

        return "Montage(data=%s, timestamp=%s)" % (data_str, timestamp_str)

    def plot(self,
             rows: int,
             cols: int,
             figsize: Optional[Tuple[int, int]] = None,
             cmap: Optional[str] = None,
             timestamps_display: bool = True,
             timestamps_format: str = "%Y-%m-%d %H:%M:%S",
             timestamps_fontsize: int = 11,
             returnfig: bool = False,
             savefig: bool = False,
             savefig_filename: Optional[str] = None,
             savefig_quality: Optional[int] = None) -> Any:
        """
        Generate a plot of the montage data. 
        
        Either display it (default behaviour), save it to disk (using the `savefig` parameter), or 
        return the matplotlib plot object for further usage (using the `returnfig` parameter).

        Args:
            figsize (tuple): 
                The matplotlib figure size to use when plotting. For example `figsize=(14,4)`.

            cmap (str): 
                The matplotlib colormap to use.

                Commonly used colormaps are:

                - REGO: `gist_heat`
                - THEMIS ASI: `gray`
                - TREx Blue: `Blues_r`
                - TREx NIR: `gray`
                - TREx RGB: `None`

                A list of all available colormaps can be found on the 
                [matplotlib documentation](https://matplotlib.org/stable/gallery/color/colormap_reference.html).
            
            returnfig (bool): 
                Instead of displaying the image, return the matplotlib figure object. This allows for further plot 
                manipulation, for example, adding labels or a title in a different location than the default. 
                
                Remember - if this parameter is supplied, be sure that you close your plot after finishing work 
                with it. This can be achieved by doing `plt.close(fig)`. 
                
                Note that this method cannot be used in combination with `savefig`.

            savefig (bool): 
                Save the displayed image to disk instead of displaying it. The parameter savefig_filename is required if 
                this parameter is set to True. Defaults to `False`.

            savefig_filename (str): 
                Filename to save the image to. Must be specified if the savefig parameter is set to True.

            savefig_quality (int): 
                Quality level of the saved image. This can be specified if the savefig_filename is a JPG image. If it
                is a PNG, quality is ignored. Default quality level for JPGs is matplotlib/Pillow's default of 75%.

        Returns:
            The displayed montage, by default. If `savefig` is set to True, nothing will be returned. If `returnfig` is 
            set to True, the plotting variables `(fig, ax)` will be returned.

        Raises:
            ValueError: Issues with the y-axis choice.
        """
        # check return mode
        if (returnfig is True and savefig is True):
            raise ValueError("Only one of returnfig or savefig can be set to True")
        if (returnfig is True and (savefig_filename is not None or savefig_quality is not None)):
            warnings.warn("The figure will be returned, but a savefig option parameter was supplied. Consider " +
                          "removing the savefig option parameter(s) as they will be ignored.",
                          stacklevel=1)
        elif (savefig is False and (savefig_filename is not None or savefig_quality is not None)):
            warnings.warn("A savefig option parameter was supplied, but the savefig parameter is False. The " +
                          "savefig option parameters will be ignored.",
                          stacklevel=1)

        # init figure
        fig, axs = plt.subplots(nrows=rows, ncols=cols, figsize=figsize)

        # for each image
        for ax, i in zip(axs.flat, range(0, len(self.timestamp))):  # type: ignore
            if (self.__n_channels == 1):
                # single channel
                ax.imshow(self.data[:, :, i], cmap=cmap, origin="lower", interpolation="nearest")
            elif (self.__n_channels == 3):
                # single channel
                ax.imshow(self.data[:, :, :, i], cmap=cmap, origin="lower", interpolation="nearest")
            else:
                raise ValueError("Can only plot 3 or 4 dimensional data (series of single-channel or RGB mages), but found data of shape %s" %
                                 (self.data.shape))

            ax.set_axis_off()

            # show timestamp
            if (timestamps_display is True):
                ax.text(
                    int(np.floor(self.data.shape[1] / 2.)),
                    5,
                    self.timestamp[i].strftime(timestamps_format),
                    ha="center",
                    fontsize=timestamps_fontsize,
                )
        plt.tight_layout(h_pad=0, w_pad=0)

        # save figure or show it
        if (savefig is True):
            # check that filename has been set
            if (savefig_filename is None):
                raise ValueError("The savefig_filename parameter is missing, but required since savefig was set to True.")

            # save the figure
            f_extension = os.path.splitext(savefig_filename)[-1].lower()
            if (".jpg" == f_extension or ".jpeg" == f_extension):
                # check quality setting
                if (savefig_quality is not None):
                    plt.savefig(savefig_filename, quality=savefig_quality, bbox_inches="tight")
                else:
                    plt.savefig(savefig_filename, bbox_inches="tight")
            else:
                if (savefig_quality is not None):
                    # quality specified, but output filename is not a JPG, so show a warning
                    warnings.warn("The savefig_quality parameter was specified, but is only used for saving JPG files. The " +
                                  "savefig_filename parameter was determined to not be a JPG file, so the quality will be ignored",
                                  stacklevel=1)
                plt.savefig(savefig_filename, bbox_inches="tight")

            # clean up by closing the figure
            plt.close(fig)
        elif (returnfig is True):
            # return the figure and axis objects
            return (fig, axs)
        else:
            # show the figure
            plt.show(fig)

            # cleanup by closing the figure
            plt.close(fig)

        # return
        return None
