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
Perform various calibration procedures on image data. 
"""

import numpy as np
from typing import Optional
from ...data.ucalgary import Calibration
from ._rego import apply_calibration as func_rego
from ._trex_nir import apply_calibration as func_trex_nir

__all__ = ["CalibrationManager"]


class CalibrationManager:
    """
    The CalibrationManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    def __init__(self):
        pass

    def rego(
        self,
        images: np.ndarray,
        cal_flatfield: Optional[Calibration] = None,
        cal_rayleighs: Optional[Calibration] = None,
        step_dark_frame_correction: bool = True,
        step_flatfield_calibration: bool = True,
        step_rayleighs_calibration: bool = True,
        exposure_length_sec: float = 2.0,
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
                Perform the dark frame correction step by subtracting an average of a bottom corner grid from 
                the image (ie. 4x4.). Defaults to `True`.
            step_flatfield_calibration (bool): 
                Perform the flatfield correction step. Defaults to `True`. Note that the `cal_flatfield` parameter
                must be supplied if this is True.
            step_rayleighs_calibration (bool): 
                Perform the Rayleighs conversion step. Defaults to `True.` Note that the `cal_rayleighs` parameter
                must be supplied if this is True.
            exposure_length_sec (float): 
                Force the exposure length to be a certain value. Default is TREx NIR's nominal operating mode 
                exposure length of `2.0 seconds`. Adjusting this field should be done with caution.

        Returns:
            The calibrated images. 
            
            The shape of the calibrated data will be same as the input images. The dtype of the calibrated data 
            will depend on if the Rayleighs conversion was performed. If it was, a float32 array will be returned. 
            If it wasn't, the dtype will be the same as input images' dtype.

        Raises:
            ValueError: issues encountered with supplied parameters.
        """
        return func_rego(
            images,
            cal_flatfield,
            cal_rayleighs,
            step_dark_frame_correction,
            step_flatfield_calibration,
            step_rayleighs_calibration,
            exposure_length_sec,
        )

    def trex_nir(
        self,
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
        return func_trex_nir(
            images,
            cal_flatfield,
            cal_rayleighs,
            step_dark_frame_correction,
            step_flatfield_calibration,
            step_rayleighs_calibration,
            exposure_length_sec,
        )
