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
Calibration procedures for REGO data.
"""

import numpy as np
from typing import Optional
from ...data.ucalgary import Calibration
from ._common import (
    perform_dark_frame_correction,
    perform_flatfield_calibration,
    perform_rayleighs_correction,
)


def apply_calibration(
    images: np.ndarray,
    cal_flatfield: Optional[Calibration] = None,
    cal_rayleighs: Optional[Calibration] = None,
    step_dark_frame_correction: bool = True,
    step_flatfield_calibration: bool = True,
    step_rayleighs_calibration: bool = True,
    exposure_length_sec: float = 5.0,
) -> np.ndarray:
    """
    Apply various calibration adjustments to a single or set of images raw images.

    Args:
        images (numpy.ndarray): 
            Raw images to perform calibration procedures on.
        cal_flatfield (pyaurorax.data.ucalgary.Calibration): 
            Calibration object containing the flatfield data to utilize. This field is required if
            the `step_flatfield_corection` is set to True.
        cal_rayleighs (pyaurorax.data.ucalgary.Calibration): 
            Calibration object containing the Rayleighs data to utilize. This field is required if 
            the `step_rayleighs_calibration` is set to True.
        step_dark_frame_correction (bool): 
            Perform the dark frame correction step. Defaults to `True`.
        step_flatfield_calibration (bool): 
            Perform the flatfield correction step. Defaults to `True`. Note that the `cal_flatfield` parameter
            must be supplied if this is True.
        step_rayleighs_calibration (bool): 
            Perform the Rayleighs conversion step. Defaults to `True.` Note that the `cal_rayleighs` parameter
            must be supplied if this is True.
        exposure_length_sec (float): 
            Force the exposure length to be a certain value. Default is TREx NIR's nominal operating mode 
            exposure length of `5.0 seconds`. Adjusting this field should be done with caution.

    Returns:
        The calibrated images. 
        
        The shape of the calibrated data will be same as the input images. The dtype of the calibrated data 
        will depend on if the Rayleighs conversion was performed. If it was, a float32 array will be returned. 
        If it wasn't, the dtype will be the same as input images' dtype.

    Raises:
        ValueError: issues encountered with supplied parameters.
    """
    # verify that we have everything we need for each requested step
    if (step_flatfield_calibration is True and cal_flatfield is None):
        raise ValueError("The cal_flatfield parameter must be supplied to perform the flatfield correction step")
    if (step_rayleighs_calibration is True and cal_rayleighs is None):
        raise ValueError("The cal_rayleighs parameter must be supplied to perform the rayleighs conversion step")

    # init
    calibrated_images = images

    # perform the dark frame correction
    #
    # NOTE: we do a 4x4 bottom corner mean
    if (step_dark_frame_correction is True):
        calibrated_images = perform_dark_frame_correction(images, 5)

    # apply the flatfield correction
    if (step_flatfield_calibration is True and cal_flatfield is not None):
        calibrated_images = perform_flatfield_calibration(calibrated_images, cal_flatfield)

    # apply the rayleighs conversion
    if (step_rayleighs_calibration is True and cal_rayleighs is not None):
        calibrated_images = perform_rayleighs_correction(calibrated_images, cal_rayleighs, exposure_length_sec)

    # return
    return calibrated_images
