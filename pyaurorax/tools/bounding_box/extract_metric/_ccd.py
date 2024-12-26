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
from typing import Optional, Literal, Sequence
from ....tools import scale_intensity


def ccd(images: np.ndarray,
        ccd_bounds: Sequence[int],
        metric: Literal["mean", "median", "sum"] = "median",
        n_channels: Optional[int] = None,
        show_preview: bool = False) -> np.ndarray:
    """
    Compute a metric of image data within a CCD boundary.

    Args:
        images (numpy.ndarray): 
            A set of images. Normally this would come directly from a data `read` call, but can also
            be any arbitrary set of images. It is anticipated that the order of axes is [rows, cols, num_images]
            or [row, cols, channels, num_images].
        
        ccd_bounds (List[int]): 
            A 4-element sequence specifying the (inclusive) CCD bounds from which to extract the metric. 
            Anticipated order is [x_0, x_1, y_0, y_1].

        metric (str): 
            The name of the metric that is to be computed for the bounded area. Valid metrics are `mean`,
            `median`, `sum`. Defaults to `median`.

        n_channels (int): 
            By default, function will assume the type of data passed as input - this argument can be used
            to manually specify the number of channels contained in image data.
        
        show_preview (bool): 
            Plot a preview of the bounded area.

    Returns:
        A numpy.ndarray containing the metrics computed within CCD bounds, for all image frames.

    Raises:
        ValueError: issue encountered with value supplied in parameter
    """

    # Select individual ccd x/y from list
    x_0 = ccd_bounds[0]
    x_1 = ccd_bounds[1]
    y_0 = ccd_bounds[2]
    y_1 = ccd_bounds[3]

    # Determine if we are using single or 3 channel
    images = np.squeeze(images)
    if n_channels is not None:
        n_channels = n_channels
    else:
        n_channels = 1
        if (len(images.shape) == 3):
            # single channel
            n_channels = 1
        elif (len(images.shape) == 4):
            # three channel
            n_channels = 3

    # Ensure that coordinates are valid
    max_x = images.shape[0]
    max_y = images.shape[1]

    if y_0 > max_y or y_0 < 0:
        raise ValueError("CCD Y Coordinate " + str(y_0) + " out of range for image of shape " + str((max_y, max_x)) + ".")
    elif y_1 > max_y or y_1 < 0:
        raise ValueError("CCD Y Coordinate " + str(y_1) + " out of range for image of shape " + str((max_y, max_x)) + ".")
    elif x_0 > max_x or x_0 < 0:
        raise ValueError("CCD Y Coordinate " + str(x_0) + " out of range for image of shape " + str((max_y, max_x)) + ".")
    elif x_1 > max_x or x_1 < 0:
        raise ValueError("CCD Y Coordinate " + str(x_1) + " out of range for image of shape " + str((max_y, max_x)) + ".")

    # Ensure that coordinates are properly ordered
    if y_0 > y_1:
        y_0, y_1 = y_1, y_0
    if x_0 > x_1:
        x_0, x_1 = x_1, x_0

    # Ensure that this is a valid polygon
    if (y_0 == y_1) or (x_0 == x_1):
        raise ValueError("Polygon defined with zero area.")

    # Slice out the bounded data
    if n_channels == 1:
        bound_data = images[y_0:y_1, x_0:x_1, :]
        if show_preview:
            preview_img = scale_intensity(images[:, :, 0], top=230)
            preview_img[y_0:y_1, x_0:x_1] = 255
            plt.figure()
            plt.imshow(preview_img, cmap="grey", origin="lower")
            plt.title("Bounded Area Preview")
            plt.axis("off")
            plt.show()
    elif n_channels == 3:
        bound_data = images[y_0:y_1, x_0:x_1, :, :]
        if show_preview:
            preview_img = scale_intensity(images[:, :, :, 0], top=230)
            preview_img[y_0:y_1, x_0:x_1, 0] = 255
            preview_img[y_0:y_1, x_0:x_1, 1:] = 0
            plt.figure()
            plt.imshow(preview_img, origin="lower")
            plt.title("Bounded Area Preview")
            plt.axis("off")
            plt.show()
    else:
        raise ValueError("Unrecognized image format with shape: " + str(images.shape))

    # Compute metric of interest
    if metric == 'median':
        result = np.median(bound_data, axis=(0, 1))
    elif metric == 'mean':
        result = np.mean(bound_data, axis=(0, 1))
    elif metric == 'sum':
        result = np.sum(bound_data, axis=(0, 1))
    else:
        raise ValueError("Metric " + str(metric) + " is not recognized.")

    return result
