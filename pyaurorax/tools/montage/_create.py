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
Routines for creating and manipulating montages
"""

import datetime
import numpy as np
from typing import List
from ..classes.montage import Montage


def create(images: np.ndarray, timestamp: List[datetime.datetime]) -> Montage:
    """
    Create a montage from a set of images.

    Args:
        images (numpy.ndarray): 
            A set of images. Normally this would come directly from a data `read` call, but can also 
            be any arbitrary set of images. It is anticipated that the order of axes is [rows, cols, num_images]
            or [row, cols, channels, num_images]. If it is not, then be sure to specify the `axis` parameter
            accordingly.

        timestamp (List[datetime.datetime]): 
            A list of timestamps corresponding to each image.

    Returns:
        A `pyaurorax.tools.Montage` object.
    """
    # determine if we are single or 3 channel
    n_channels = 1
    if (len(images.shape) == 3):
        # single channel
        n_channels = 1
    elif (len(images.shape) == 4):
        # three channel
        n_channels = 3
    else:
        ValueError("Unable to determine number of channels based on the supplied images. Make sure you are supplying a " +
                   "[rows,cols,images] or [rows,cols,channels,images] sized array.")

    # create the montage object
    #
    # NOTE: we presently do nothing more than repackage the data. This logic for create()
    # is here in case we need to further expand functionality and need it. It's also good
    # for consistency.
    montage_obj = Montage(data=images, timestamp=timestamp, n_channels=n_channels)

    # return
    return montage_obj
