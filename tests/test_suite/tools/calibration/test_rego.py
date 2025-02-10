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

import pytest


@pytest.mark.tools
def test_simple(at, rego_calibration_data):
    calibrated_data = at.calibration.rego(
        rego_calibration_data["raw_data"].data,
        cal_flatfield=rego_calibration_data["flatfield_data"].data[0],
        cal_rayleighs=rego_calibration_data["rayleighs_data"].data[0],
    )
    assert calibrated_data.shape == rego_calibration_data["raw_data"].data.shape


@pytest.mark.tools
def test_single_image(at, rego_calibration_data):
    calibrated_data = at.calibration.rego(
        rego_calibration_data["raw_data"].data[:, :, 0],
        cal_flatfield=rego_calibration_data["flatfield_data"].data[0],
        cal_rayleighs=rego_calibration_data["rayleighs_data"].data[0],
    )
    assert calibrated_data.shape == rego_calibration_data["raw_data"].data[:, :, 0].shape


@pytest.mark.tools
def test_bad_flatfield_arg(at, rego_calibration_data):
    with pytest.raises(ValueError) as e_info:
        _ = at.calibration.rego(
            rego_calibration_data["raw_data"].data,
            step_dark_frame_correction=False,
            step_flatfield_calibration=True,
            step_rayleighs_calibration=False,
        )
    assert "The cal_flatfield parameter must be supplied to perform the flatfield correction step" in str(e_info)


@pytest.mark.tools
def test_bad_rayleighs_arg(at, rego_calibration_data):
    with pytest.raises(ValueError) as e_info:
        _ = at.calibration.rego(
            rego_calibration_data["raw_data"].data,
            step_dark_frame_correction=False,
            step_flatfield_calibration=False,
            step_rayleighs_calibration=True,
        )
    assert "The cal_rayleighs parameter must be supplied to perform the rayleighs conversion step" in str(e_info)
