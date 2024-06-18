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
Retrieve availability information about data in the AuroraX search engine.
"""

import datetime
from typing import Optional, List
from ._availability import ephemeris as func_ephemeris
from ._availability import data_products as func_data_products
from .classes.availability_result import AvailabilityResult
from ..sources.classes.data_source import FORMAT_DEFAULT

__all__ = ["AvailabilityManager", "AvailabilityResult"]


class AvailabilityManager:
    """
    The AvailabilityManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    def __init__(self, aurorax_obj):
        self.__aurorax_obj = aurorax_obj

    def ephemeris(self,
                  start: datetime.date,
                  end: datetime.date,
                  program: Optional[str] = None,
                  platform: Optional[str] = None,
                  instrument_type: Optional[str] = None,
                  source_type: Optional[str] = None,
                  owner: Optional[str] = None,
                  format: str = FORMAT_DEFAULT,
                  slow: bool = False) -> List[AvailabilityResult]:
        """
        Retrieve information about the number of existing ephemeris records

        Args:
            start (datetime.date): 
                Start date to retrieve availability info for (inclusive)
            end (datetime.date): 
                End date to retrieve availability info for (inclusive)
            program (str): 
                Program name to filter sources by, defaults to `None`
            platform (str): 
                Platform name to filter sources by, defaults to `None`
            instrument_type (str): 
                Instrument type to filter sources by, defaults to `None`
            source_type (str): 
                The data source type to filter for, defaults to `None`. Options are in 
                the pyaurorax.search.sources module, or at the top level using the 
                pyaurorax.search.SOURCE_TYPE_* variables.
            owner (str): 
                Owner email address to filter sources by, defaults to `None`
            format (str): 
                The format of the data sources returned, defaults to `FORMAT_FULL_RECORD`. 
                Other options are in the pyaurorax.search.sources module, or at the top level using 
                the pyaurorax.search.FORMAT_* variables.
            slow (bool): 
                Query the data using a slower, but more accurate method, defaults to `False`

        Returns:
            Ephemeris availability information matching the requested parameters
        
        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        return func_ephemeris(self.__aurorax_obj, start, end, program, platform, instrument_type, source_type, owner, format, slow)

    def data_products(self,
                      start: datetime.date,
                      end: datetime.date,
                      program: Optional[str] = None,
                      platform: Optional[str] = None,
                      instrument_type: Optional[str] = None,
                      source_type: Optional[str] = None,
                      owner: Optional[str] = None,
                      format: Optional[str] = FORMAT_DEFAULT,
                      slow: Optional[bool] = False) -> List[AvailabilityResult]:
        """
        Retrieve information about the number of existing data product records

        Args:
            start (datetime.date): 
                Start date to retrieve availability info for (inclusive)
            end (datetime.date): 
                End date to retrieve availability info for (inclusive)
            program (str): 
                Program name to filter sources by, defaults to `None`
            platform (str): 
                Platform name to filter sources by, defaults to `None`
            instrument_type (str): 
                Instrument type to filter sources by, defaults to `None`
            source_type (str): 
                The data source type to filter for, defaults to `None`. Options are in 
                the pyaurorax.search.sources module, or at the top level using the 
                pyaurorax.search.SOURCE_TYPE_* variables.
            owner (str): 
                Owner email address to filter sources by, defaults to `None`
            format (str): 
                The format of the data sources returned, defaults to `FORMAT_FULL_RECORD`. 
                Other options are in the pyaurorax.search.sources module, or at the top level using 
                the pyaurorax.search.FORMAT_* variables.
            slow (bool): 
                Query the data using a slower, but more accurate method, defaults to `False`

        Returns:
            Data product availability information matching the requested parameters

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        return func_data_products(self.__aurorax_obj, start, end, program, platform, instrument_type, source_type, owner, format, slow)
