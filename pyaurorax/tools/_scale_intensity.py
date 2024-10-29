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
from typing import Optional


def __scale_data(data, min, max, top):
    # init
    bottom = 0

    # set top val
    #
    # NOTE: we only care about this if it's a uint array. If it's a double array, then we
    # check to make sure that a top was specified.
    if ("float" in str(data.dtype)):
        # this is float type, check that the top was specified
        if (top is None):
            raise ValueError("The top parameter must be specified when a float array is supplied")
    else:
        dtype_maxval = np.iinfo(data.dtype).max
        if (top is None):
            # derive values using dtype of data array
            top = dtype_maxval

        # check top
        if (top > dtype_maxval):
            raise ValueError("The top value must be less than or equal to %s" % (dtype_maxval))

    # set min and max
    if (min is None):
        cmin = data.min()
    else:
        cmin = float(min)
    if (max is None):
        cmax = data.max()
    else:
        cmax = float(max)

    # set scaling factor
    cscale = cmax - cmin
    if cscale < 0:
        raise ValueError("The max value must be larger than the min value")
    elif cscale == 0:
        cscale = 1

    # do scaling
    scale = float(top - bottom) / cscale
    byte_data = (data - cmin) * scale + bottom
    scaled_data = (byte_data.clip(bottom, top) + 0.5).astype(data.dtype)

    # return
    return scaled_data


def scale_intensity(
    data: np.ndarray,
    min: Optional[float] = None,
    max: Optional[float] = None,
    top: Optional[float] = None,
    memory_saver: bool = True,
) -> np.ndarray:
    """
    Scale all values of an array that lie in the range min<=x<=max in to 
    the range 0<=x<=high.
    
    Args:
        data (numpy.ndarray): 
            Data array, can be 2, 3, or 4-dimensional. Assumed to be an image, or array of 
            images. Also assumed that the first 2 dimensions are the image's x and y 
            coordinates, and the following dimensions are some combination of the number of 
            images, and/or the colour channel.

        min (float): 
            Minimum value of array to be considered

        max (float): 
            Maximum value of array to be considered

        top (float): 
            Maximum value of the scaled result. If not supplied, the max value
            of the data array's dtype is used.

        memory_saver (bool): 
            Utilize less RAM when scaling a set of images. Defaults to `True`. If set to `False` then
            the scaling routine will be faster, but will utilize significantly more RAM.

    Returns:
        A new `numpy.ndarray` that is the same dimensions as the inputted data array, 
        with the scaling applied.

    Raises:
        ValueError: Issues with the supplied min, max, or top
    """

    if (memory_saver is True):
        # Save original data shape
        input_shape = data.shape

        # determine if we are single or 3 channel
        if (len(data.shape) == 2):
            n_channels = 1
            data = data[:, :, np.newaxis]
        elif (len(data.shape) == 3):
            # single channel
            n_channels = 1
        elif (len(data.shape) == 4):
            # three channel
            n_channels = 3
        else:
            raise ValueError(
                "Unable to determine number of channels based on the supplied images. Make sure you are supplying a "
                +
                "[rows,cols,images] or [rows,cols,channels,images] sized array."
            )

        # init destination array
        images_scaled = np.empty((data.shape), dtype=data.dtype)

        # cycle through each image
        for i in range(0, data.shape[-1]):
            if (n_channels == 1):
                images_scaled[:, :, i] = __scale_data(data[:, :, i], min, max,
                                                      top)
            else:
                images_scaled[:, :, :,
                              i] = __scale_data(data[:, :, :, i], min, max,
                                                top)

        # Reshape to confirm output is the same shape as input
        images_scaled = np.reshape(images_scaled, input_shape)

        # return
        return images_scaled
    else:
        # scale and return
        return __scale_data(data, min, max, top)
