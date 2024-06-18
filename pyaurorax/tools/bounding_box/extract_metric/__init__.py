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
Extract various metrics from a given bounding box.
"""

from ._geo import geo
from ._ccd import ccd
from ._mag import mag
from ._elevation import elevation
from ._azimuth import azimuth

__all__ = [
    "geo",
    "ccd",
    "mag",
    "elevation",
    "azimuth",
]
