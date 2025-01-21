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
Calibration procedures for TREx NIR data.
"""

from ._common import (
    perform_dark_frame_correction,
    perform_flatfield_calibration,
    perform_rayleighs_correction,
)


def apply_calibration(
    images,
    cal_flatfield,
    cal_rayleighs,
    step_dark_frame_correction,
    step_flatfield_calibration,
    step_rayleighs_calibration,
    exposure_length_sec,
):
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
