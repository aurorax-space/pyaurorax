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
import matplotlib.pyplot as plt
from .._util import show_warning


def display(image, cmap, figsize, aspect, colorbar, title, returnfig, savefig, savefig_filename, savefig_quality):
    # check return mode
    if (returnfig is True and savefig is True):
        raise ValueError("Only one of returnfig or savefig can be set to True")
    if (returnfig is True and (savefig_filename is not None or savefig_quality is not None)):
        show_warning("The figure will be returned, but a savefig option parameter was supplied. Consider " +
                     "removing the savefig option parameter(s) as they will be ignored.",
                     stacklevel=1)
    elif (savefig is False and (savefig_filename is not None or savefig_quality is not None)):
        show_warning("A savefig option parameter was supplied, but the savefig parameter is False. The " +
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
            if (savefig_quality is not None):  # pragma: nocover-ok
                plt.savefig(savefig_filename, quality=savefig_quality, bbox_inches="tight")
            else:
                plt.savefig(savefig_filename, bbox_inches="tight")
        else:
            if (savefig_quality is not None):
                # quality specified, but output filename is not a JPG, so show a warning
                show_warning("The savefig_quality parameter was specified, but is only used for saving JPG files. The " +
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
