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
from typing import Union, Optional, Literal, Sequence
from ....data.ucalgary import Skymap
from ....tools import scale_intensity


def azimuth(images: np.ndarray,
            skymap: Skymap,
            azimuth_bounds: Sequence[Union[int, float]],
            metric: Literal["mean", "median", "sum"] = "median",
            n_channels: Optional[int] = None,
            show_preview: bool = False) -> np.ndarray:
    """
    Compute a metric of image data within an azimuthal boundary.

    Args:
        images (numpy.ndarray): 
            A set of images. Normally this would come directly from a data `read` call, but can also
            be any arbitrary set of images. It is anticipated that the order of axes is [rows, cols, num_images]
            or [row, cols, channels, num_images].
        
        skymap (pyaurorax.data.ucalgary.Skymap): 
            The skymap corresponding to the image data.

        azimuth_bounds (Sequence[int, float]): 
            A 2-element sequence specifying the azimuthal bounds from which to extract the metric. 
            Anticipated order is [az_min, az_max].

        metric (str): 
            The name of the metric that is to be computed for the bounded area. Valid metrics are `mean`,
            `median`, `sum`. Default is `median`.

        n_channels (int): 
            By default, function will assume the type of data passed as input - this argument can be used
            to manually specify the number of channels contained in image data.

        show_preview (bool): 
            Plot a preview of the bounded area.

    Returns:
        A numpy.ndarray containing the metrics computed within azimuth range, for all image frames.

    Raises:
        ValueError: issue encountered with value supplied in parameter
    """

    # Select individual azimuths from list
    az_0 = azimuth_bounds[0]
    az_1 = azimuth_bounds[1]

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
    if az_0 > 360 or az_0 < 0:
        raise ValueError("Invalid Azimuth: " + str(az_0))
    elif az_1 > 360 or az_1 < 0:
        raise ValueError("Invalid Azimuth: " + str(az_1))

    # Ensure that azimuths are properly ordered
    if az_0 > az_1:
        az_0, az_1 = az_1, az_0

    # Ensure that this is a valid polygon
    if (az_0 == az_1):
        raise ValueError("Azimuth bounds defined with zero area.")

    # Obtain azimuth array from skymap
    if (skymap.full_azimuth is None):
        raise ValueError("Skymap 'full_azimuth' value is None. Unable to perform function")
    az = np.squeeze(skymap.full_azimuth)

    # Obtain indices into skymap within azimuth range
    bound_idx = np.where(np.logical_and(az > float(az_0), az < float(az_1)))

    # If boundaries contain no data, raise error
    if len(bound_idx[0]) == 0 or len(bound_idx[1]) == 0:
        raise ValueError("No data within desired bounds. Try a larger area.")

    # Slice out the bounded data, and plot preview if requested
    if n_channels == 1:
        bound_data = images[bound_idx[0], bound_idx[1], :]
        if show_preview:
            preview_img = scale_intensity(images[:, :, 0], top=230)
            preview_img[bound_idx[0], bound_idx[1]] = 255
            plt.figure()
            plt.imshow(preview_img, cmap="grey", origin="lower")
            plt.title("Bounded Area Preview")
            plt.axis("off")
            plt.show()
    elif n_channels == 3:
        bound_data = images[bound_idx[0], bound_idx[1], :, :]
        if show_preview:
            preview_img = scale_intensity(images[:, :, :, 0], top=230)
            preview_img[bound_idx[0], bound_idx[1], 0] = 255
            preview_img[bound_idx[0], bound_idx[1], 1:] = 0
            plt.figure()
            plt.imshow(preview_img, origin="lower")
            plt.title("Bounded Area Preview")
            plt.axis("off")
            plt.show()
    else:
        raise ValueError("Unrecognized image format with shape: " + str(images.shape))

    # Compute metric of interest
    if metric == 'median':
        result = np.median(bound_data, axis=0)
    elif metric == 'mean':
        result = np.mean(bound_data, axis=0)
    elif metric == 'sum':
        result = np.sum(bound_data, axis=0)
    else:
        raise ValueError("Metric " + str(metric) + " is not recognized.")

    return result
