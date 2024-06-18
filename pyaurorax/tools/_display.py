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

import os
import numpy as np
import matplotlib.pyplot as plt
import warnings
from typing import Optional, Tuple, Union, Literal, Any


def display(image: np.ndarray,
            cmap: Optional[str] = None,
            figsize: Optional[Tuple[int, int]] = None,
            aspect: Optional[Union[Literal["equal", "auto"], float]] = None,
            colorbar: bool = False,
            title: Optional[str] = None,
            returnfig: bool = False,
            savefig: bool = False,
            savefig_filename: Optional[str] = None,
            savefig_quality: Optional[int] = None) -> Any:
    """
    Render a visualization of a single image.

    Either display it (default behaviour), save it to disk (using the `savefig` parameter), or 
    return the matplotlib plot object for further usage (using the `returnfig` parameter).

    Args:
        image (numpy.ndarray): 
            The image to display, represented as a numpy array.

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

        figsize (tuple): 
            The matplotlib figure size to use when displaying, tuple of two integers (ie. `figsize=(14, 4)`)
    
        aspect (str or float): 
            The matplotlib imshow aspect ration to use. A common value for this is `auto`. All valid values 
            can be found on the [matplotlib documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html).

        colorbar (bool): 
            Display a colorbar. Default is `False`.

        title (str): 
            A title to display above the rendered image. Defaults to no title.

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
        The displayed image, by default. If `savefig` is set to True, nothing will be returned. If `returnfig` is 
        set to True, the plotting variables `(fig, ax)` will be returned.

    Raises:
        ValueError: issues with supplied parameters.
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
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_axis_off()

    # plot data
    im = ax.imshow(image, cmap=cmap, origin="lower", aspect=aspect)

    # show colour bar
    if (colorbar is True):
        fig.colorbar(im, ax=ax)

    # show title
    if (title is not None):
        ax.set_title(title)

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
        return (fig, ax)
    else:
        # show the figure
        plt.show(fig)

        # cleanup by closing the figure
        plt.close(fig)

    # return
    return None
