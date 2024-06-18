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

import datetime
import numpy as np
from typing import List
from ..classes.keogram import Keogram


def create(images: np.ndarray, timestamp: List[datetime.datetime], axis: int = 0) -> Keogram:
    """
    Create a keogram from a set of images.

    Args:
        images (numpy.ndarray): 
            A set of images. Normally this would come directly from a data `read` call, but can also 
            be any arbitrary set of images. It is anticipated that the order of axes is [rows, cols, num_images]
            or [row, cols, channels, num_images]. If it is not, then be sure to specify the `axis` parameter
            accordingly.

        timestamp (List[datetime.datetime]): 
            A list of timestamps corresponding to each image.

        axis (int): 
            The axis to extract the keogram slice from. Default is `0`, meaning the rows (or Y) axis.

    Returns:
        A `pyaurorax.tools.Keogram` object.

    Raises:
        ValueError: issue with supplied parameters.
    """
    # set y axis
    ccd_y = np.arange(0, images.shape[axis])

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

    # initialize keogram data
    n_rows = images.shape[0]
    n_imgs = images.shape[-1]
    if (n_channels == 1):
        keo_arr = np.full([n_rows, n_imgs], 0, dtype=images.dtype)
    else:
        keo_arr = np.full([n_rows, n_imgs, n_channels], 0, dtype=images.dtype)

    # extract the keogram slices
    middle_column_idx = int(np.floor((images.shape[1]) / 2 - 1))
    for img_idx in range(0, n_imgs):
        if (n_channels == 1):
            # single channel
            frame = images[:, :, img_idx]
            frame_middle_slice = frame[:, middle_column_idx]
            keo_arr[:, img_idx] = frame_middle_slice
        else:
            # 3-channel
            frame = images[:, :, :, img_idx]
            frame_middle_slice = frame[:, middle_column_idx, :]
            keo_arr[:, img_idx, :] = frame_middle_slice

    # create the keogram object
    keo_obj = Keogram(data=keo_arr, slice_idx=middle_column_idx, timestamp=timestamp, ccd_y=ccd_y)

    # return
    return keo_obj
