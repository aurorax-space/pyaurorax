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
from ...data.ucalgary import Calibration


def perform_dark_frame_correction(images: np.ndarray, size: int) -> np.ndarray:
    """
    This method will perform a dark frame correction by subtracting an average
    of a bottom corner grid from the image (ie. 4x4.).

    NOTE: This is an internal-only used function. It is not publicly exposed.
    """
    # init
    original_dtype = images.dtype
    if (len(images.shape) == 2):
        # only a single image, add an axis
        images = images[:, :, np.newaxis]

    # extract NxN box from lower left corner, compute means
    dark_boxes = images[0:size, 0:size, :]
    dark_means = np.mean(dark_boxes, axis=(0, 1))
    dark_means = dark_means.astype(np.int32)

    # apply
    #
    # NOTE: we convert to int32 to avoid lower-bound rollover and allow
    # for negative numbers, which we then cast to 0 and convert back to
    # the native dtype.
    #
    # TODO: there's definitely some optimization possible here
    images = images.astype(np.int32)
    for i in range(0, images.shape[2]):
        images[:, :, i] = images[:, :, i] - dark_means[i]
    images[np.where(images < 0)] = 0
    images = images.astype(original_dtype)

    # remove last axis if there's only one image
    if (images.shape[2] == 1):
        images = np.squeeze(images, axis=2)

    # return
    return images


def perform_flatfield_calibration(images: np.ndarray, cal_flatfield: Calibration) -> np.ndarray:
    # add axis if it's a single image
    if (len(images.shape) == 2):
        # only a single image, add an axis
        images = images[:, :, np.newaxis]

    # for each image, apply multiplier
    for i in range(0, images.shape[-1]):
        images[:, :, i] = images[:, :, i] * cal_flatfield.flat_field_multiplier

    # remove last axis if there's only one image
    if (images.shape[2] == 1):
        images = np.squeeze(images, axis=2)

    # return
    return images


def perform_rayleighs_correction(images: np.ndarray, cal_rayleighs: Calibration, exposure_length_sec: float) -> np.ndarray:
    # add axis if it's a single image
    if (len(images.shape) == 2):
        # only a single image, add an axis
        images = images[:, :, np.newaxis]

    # convert image array to a float array
    images = images.astype(np.float32)

    # for each images, apply rayleighs conversion
    for i in range(0, images.shape[-1]):
        images[:, :, i] = images[:, :, i] * cal_rayleighs.rayleighs_perdn_persecond / float(exposure_length_sec)

    # remove last axis if there's only one image
    if (images.shape[2] == 1):
        images = np.squeeze(images, axis=2)

    # return
    return images
