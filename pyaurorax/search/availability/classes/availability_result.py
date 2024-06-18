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
Class definition for data availability information
"""

from dataclasses import dataclass
from typing import Dict, Optional
from ...sources.classes.data_source import DataSource


@dataclass
class AvailabilityResult:
    """
    Class definition for data availability information

    Attributes:
        data_source (pyaurorax.search.DataSource): 
            the data source that the records are associated with
        available_ephemeris (Dict): 
            the ephemeris availability information
        available_data_products (Dict): 
            the data product availability information
    """
    data_source: DataSource
    available_data_products: Optional[Dict] = None
    available_ephemeris: Optional[Dict] = None
