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
Create montages.
"""

import datetime
import numpy as np
from typing import List
from ..classes.montage import Montage
from ._create import create as func_create

__all__ = ["MontageManager"]


class MontageManager:
    """
    The MontageManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    def __init__(self):
        pass

    def create(self, images: np.ndarray, timestamp: List[datetime.datetime]) -> Montage:
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
        return func_create(images, timestamp)
