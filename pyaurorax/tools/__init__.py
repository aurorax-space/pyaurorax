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
Data analysis toolkit for working with all-sky imager data available within the
AuroraX platform.

This portion of the PyAuroraX library allows you to easily generate basic plots
for ASI data, and common manipulations. These include things like displaying single
images, making keograms, projecting ASI data onto maps, and extracting metrics for
a given lat/lon bounding box.

Example:
    For shorter function calls, you can initialize the tools submodule using like so:

    ```
    import pyaurorax
    aurorax = pyaurorax.PyAuroraX()
    at = aurorax.tools
    ```
"""

# pull in top-level functions
from ._display import display
from ._movie import movie
from ._scale_intensity import scale_intensity
from ._util import set_theme

# pull in classes
from .classes.keogram import Keogram
from .classes.montage import Montage
from .classes.mosaic import Mosaic, MosaicData, MosaicSkymap

# pull in submodules
from . import keogram
from . import montage
from . import calibration
from . import bounding_box
from . import mosaic
from . import ccd_contour
from . import grid_files
from . import spectra

__all__ = [
    # sub-modules
    "keogram",
    "montage",
    "calibration",
    "bounding_box",
    "mosaic",
    "ccd_contour",
    "grid_files",
    "spectra",

    # top level functions
    "display",
    "movie",
    "scale_intensity",
    "set_theme",

    # classses
    "Keogram",
    "Montage",
    "Mosaic",
    "MosaicData",
    "MosaicSkymap",
]
