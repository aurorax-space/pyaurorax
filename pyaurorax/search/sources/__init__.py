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
Manage AuroraX data sources utilized by the search engine.
"""

from typing import Optional, List, Dict
from texttable import Texttable
from ._sources import list as func_list
from ._sources import search as func_search
from ._sources import get as func_get
from ._sources import get_using_filters as func_get_using_filters
from ._sources import get_using_identifier as func_get_using_identifier
from ._sources import add as func_add
from ._sources import delete as func_delete
from ._sources import update as func_update
from .classes.data_source import DataSource, DataSourceStatistics
from .classes.data_source import (
    FORMAT_BASIC_INFO,
    FORMAT_BASIC_INFO_WITH_METADATA,
    FORMAT_DEFAULT,
    FORMAT_FULL_RECORD,
    FORMAT_IDENTIFIER_ONLY,
    SOURCE_TYPE_EVENT_LIST,
    SOURCE_TYPE_GROUND,
    SOURCE_TYPE_HEO,
    SOURCE_TYPE_LEO,
    SOURCE_TYPE_LUNAR,
    SOURCE_TYPE_NOT_APPLICABLE,
)

__all__ = [
    "SourcesManager",
    "DataSource",
    "DataSourceStatistics",
    "FORMAT_BASIC_INFO",
    "FORMAT_BASIC_INFO_WITH_METADATA",
    "FORMAT_DEFAULT",
    "FORMAT_FULL_RECORD",
    "FORMAT_IDENTIFIER_ONLY",
    "SOURCE_TYPE_EVENT_LIST",
    "SOURCE_TYPE_GROUND",
    "SOURCE_TYPE_HEO",
    "SOURCE_TYPE_LEO",
    "SOURCE_TYPE_LUNAR",
    "SOURCE_TYPE_NOT_APPLICABLE",
]


class SourcesManager:
    """
    The SourcesManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    def __init__(self, aurorax_obj):
        self.__aurorax_obj = aurorax_obj

    def list(self,
             program: Optional[str] = None,
             platform: Optional[str] = None,
             instrument_type: Optional[str] = None,
             source_type: Optional[str] = None,
             owner: Optional[str] = None,
             format: Optional[str] = FORMAT_FULL_RECORD,
             order: Optional[str] = "identifier",
             include_stats: Optional[bool] = False) -> List[DataSource]:
        """
        Retrieve all data source records. Parameters can be used to filter as desired.

        Args:
            program (str): 
                the program to filter for, defaults to `None`
            platform (str): 
                the platform to filter for, defaults to `None`
            instrument_type (str): 
                the instrument type to filter for, defaults to `None`
            source_type (str): 
                the data source type to filter for, defaults to `None`. Options are in 
                the pyaurorax.search.sources module, or at the top level using the 
                pyaurorax.search.SOURCE_TYPE_* variables.
            owner (str): 
                the owner's email address to filter for, defaults to `None`
            format (str): 
                the format of the data sources returned, defaults to `classes.data_source.FORMAT_FULL_RECORD`. 
                Other options are in the pyaurorax.search.sources module, or at the top level using 
                the pyaurorax.search.FORMAT_* variables.
            order (str): 
                the category to order results by. Valid values are identifier, program, platform,
                instrument_type, display_name, or owner. Defaults to `identifier`
            include_stats (bool): 
                include additional stats information about the data source, defaults to `False`

        Returns:
            a list of `DataSource` records matching the requested parameters

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: error during API call
        """
        return func_list(
            self.__aurorax_obj,
            program,
            platform,
            instrument_type,
            source_type,
            owner,
            format,
            order,
            include_stats,
        )

    def list_in_table(self,
                      program: Optional[str] = None,
                      platform: Optional[str] = None,
                      instrument_type: Optional[str] = None,
                      source_type: Optional[str] = None,
                      owner: Optional[str] = None,
                      order: Optional[str] = "identifier",
                      table_max_width: int = 200) -> None:
        """
        Display all data source records in a table. Parameters can be used to filter as desired.

        Args:
            program (str): 
                the program to filter for, defaults to `None`

            platform (str): 
                the platform to filter for, defaults to `None`

            instrument_type (str): 
                the instrument type to filter for, defaults to `None`

            source_type (str): 
                the data source type to filter for, defaults to `None`. Options are in 
                the pyaurorax.search.sources module, or at the top level using the 
                pyaurorax.search.SOURCE_TYPE_* variables.

            owner (str): 
                the owner's email address to filter for, defaults to `None`

            format (str): 
                the format of the data sources returned, defaults to `classes.data_source.FORMAT_FULL_RECORD`. 
                Other options are in the pyaurorax.search.sources module, or at the top level using 
                the pyaurorax.search.FORMAT_* variables.

            order (str): 
                the category to order results by. Valid values are identifier, program, platform,
                instrument_type, display_name, or owner. Defaults to `identifier`
                
            table_max_width (int): 
                table maximum width, defaults to 200

        Returns:
            No return, only prints a table

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: error during API call
        """
        # get datasets
        datasets = func_list(
            self.__aurorax_obj,
            program,
            platform,
            instrument_type,
            source_type,
            owner,
            FORMAT_BASIC_INFO,
            order,
            False,
        )

        # set table lists
        table_identifiers = []
        table_programs = []
        table_platforms = []
        table_instrument_types = []
        table_source_types = []
        table_display_names = []
        for d in datasets:
            table_identifiers.append(d.identifier)
            table_programs.append(d.program)
            table_platforms.append(d.platform)
            table_instrument_types.append(d.instrument_type)
            table_source_types.append(d.source_type)
            table_display_names.append(d.display_name)

        # set header values
        table_headers = [
            "Identifier",
            "Program",
            "Platform",
            "Instrument Type",
            "Source Type",
            "Display Name",
        ]

        # print as table
        table = Texttable(max_width=table_max_width)
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(["t"] * len(table_headers))
        table.set_header_align(["l"] * len(table_headers))
        table.set_cols_align(["l"] * len(table_headers))
        table.header(table_headers)
        for i in range(0, len(table_identifiers)):
            table.add_row([
                table_identifiers[i],
                table_programs[i],
                table_platforms[i],
                table_instrument_types[i],
                table_source_types[i],
                table_display_names[i],
            ])
        print(table.draw())

    def search(self,
               programs: Optional[List[str]] = [],
               platforms: Optional[List[str]] = [],
               instrument_types: Optional[List[str]] = [],
               format: Optional[str] = FORMAT_FULL_RECORD,
               order: Optional[str] = "identifier",
               include_stats: Optional[bool] = False) -> List[DataSource]:
        """
        Search for data source records. Parameters can be used to filter as desired.

        This function is very similar to the `list()` function, however multiple programs,
        platforms, and/or instrument types can be supplied here. The `list()` function only 
        supports single values for the parameters.

        Args:
            programs (List[str]): 
                the programs to search for, defaults to `[]`
            platforms (List[str]): 
                the platforms to search for, defaults to `[]`
            instrument_type (List[str]): 
                the instrument types to search for, defaults to `[]`
            format (str): 
                the format of the data sources returned, defaults to `classes.data_source.FORMAT_FULL_RECORD`. 
                Other options are in the pyaurorax.search.sources module, or at the top level using 
                the pyaurorax.search.FORMAT_* variables.
            order (str): 
                the category to order results by. Valid values are identifier, program, platform,
                instrument_type, display_name, or owner. Defaults to `identifier`
            include_stats (bool): 
                include additional stats information about the data source, defaults to `False`

        Returns:
            a list of `DataSource` records matching the requested parameters

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: error during API call
        """
        return func_search(
            self.__aurorax_obj,
            programs,
            platforms,
            instrument_types,
            format,
            order,
            include_stats,
        )

    def get(self,
            program: str,
            platform: str,
            instrument_type: str,
            format: Optional[str] = FORMAT_FULL_RECORD,
            include_stats: Optional[bool] = False) -> DataSource:
        """
        Retrieve a specific data source record

        Args:
            program (str): 
                the program name
            platform (str): 
                the platform name
            instrument_type (str): 
                the instrument type name
            format (str): 
                the format of the data sources returned, defaults to `classes.data_source.FORMAT_FULL_RECORD`. 
                Other options are in the pyaurorax.search.sources module, or at the top level using 
                the pyaurorax.search.FORMAT_* variables.
            include_stats (bool): 
                include additional stats information about the data source, defaults to `False`

        Returns:
            the `DataSource` matching the requested parameters

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: error during API call
            pyaurorax.exceptions.AuroraXNotFoundError: source not found
        """
        return func_get(
            self.__aurorax_obj,
            program,
            platform,
            instrument_type,
            format,
            include_stats,
        )

    def get_using_filters(self,
                          program: Optional[str] = None,
                          platform: Optional[str] = None,
                          instrument_type: Optional[str] = None,
                          source_type: Optional[str] = None,
                          owner: Optional[str] = None,
                          format: Optional[str] = FORMAT_FULL_RECORD,
                          order: Optional[str] = "identifier",
                          include_stats: Optional[bool] = False) -> List[DataSource]:
        """
        Retrieve all data sources matching a filter

        Args:
            program (str): 
                the program to filter for, defaults to `None`
            platform (str): 
                the platform to filter for, defaults to `None`
            instrument_type (str): 
                the instrument type to filter for, defaults to `None`
            source_type (str): 
                the data source type to filter for, defaults to `None`. Options are in 
                the pyaurorax.search.sources module, or at the top level using the 
                pyaurorax.search.SOURCE_TYPE_* variables.
            owner (str): 
                the owner's email address to filter for, defaults to `None`
            format (str): 
                the format of the data sources returned, defaults to `classes.data_source.FORMAT_FULL_RECORD`. 
                Other options are in the pyaurorax.search.sources module, or at the top level using 
                the pyaurorax.search.FORMAT_* variables.
            order (str): 
                the category to order results by. Valid values are identifier, program, platform,
                instrument_type, display_name, or owner. Defaults to `identifier`
            include_stats (bool): 
                include additional stats information about the data source, defaults to `False`.

        Returns:
            a list of `DataSource` records matching the requested parameters

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: error during API call
        """
        return func_get_using_filters(
            self.__aurorax_obj,
            program,
            platform,
            instrument_type,
            source_type,
            owner,
            format,
            order,
            include_stats,
        )

    def get_using_identifier(self, identifier: int, format: Optional[str] = FORMAT_FULL_RECORD, include_stats: Optional[bool] = False) -> DataSource:
        """
        Retrieve data source for a specific identifier

        Args:
            identifier (int): 
                the AuroraX unique data source identifier number
            format (str): 
                the format of the data sources returned, defaults to `classes.data_source.FORMAT_FULL_RECORD`. 
                Other options are in the pyaurorax.search.sources module, or at the top level using 
                the pyaurorax.search.FORMAT_* variables.
            include_stats (bool): 
                include additional stats information about the data source, defaults to `False`

        Returns:
            the `DataSource` for the specified identifier

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: error during API call
        """
        return func_get_using_identifier(self.__aurorax_obj, identifier, format, include_stats)

    def add(self, data_source: DataSource) -> DataSource:
        """
        Add a new data source to the AuroraX search engine

        Args:
            data_source (DataSource): 
                the data source to add (note: it must be a fully-defined DataSource object)

        Returns:
            the newly created `DataSource`.

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: error during API call
            pyaurorax.exceptions.AuroraXUnauthorizedError: not allowed to perform task, or API key / user permissions are invalid
            pyaurorax.exceptions.AuroraXDuplicateError: duplicate data source, already exists
        """
        return func_add(self.__aurorax_obj, data_source)

    def delete(self, identifier: int) -> int:
        """
        Delete a data source from the AuroraX search engine

        Args:
            identifier (int): the data source unique identifier to delete

        Returns:
            0 on success, raises error if an issue was encountered

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: error during API call
            pyaurorax.exceptions.AuroraXUnauthorizedError: not allowed to perform task, or API key / user permissions are invalid
            pyaurorax.exceptions.AuroraXNotFoundError: data source not found
            pyaurorax.exceptions.AuroraXConflictError: a conflict occurred
        """
        return func_delete(self.__aurorax_obj, identifier)

    def update(self,
               identifier: int,
               program: Optional[str] = None,
               platform: Optional[str] = None,
               instrument_type: Optional[str] = None,
               source_type: Optional[str] = None,
               display_name: Optional[str] = None,
               metadata: Optional[Dict] = None,
               owner: Optional[str] = None,
               maintainers: Optional[List[str]] = None,
               ephemeris_metadata_schema: Optional[List[Dict]] = None,
               data_product_metadata_schema: Optional[List[Dict]] = None) -> DataSource:
        """
        Update a data source in the AuroraX search engine. Omitted fields are ignored during the 
        update. 
        
        Note that the identifier cannot be updated. If you need to update the data source's identifier,
        we recommend deletion of the original data source and recreation using the desired identifier.

        Args:
            identifier (int): 
                the AuroraX unique identifier for the data source, required and cannot be updated
            program (str): 
                the new program for the data source, defaults to `None`
            platform (str): 
                the new platform for the data source, defaults to `None`
            instrument_type (str): 
                the new instrument type for the data source, defaults to `None`
            source_type (str): 
                the new source type for the data source, defaults to `None`. Options
                are in the pyaurorax.search.sources module, or at the top level using the
                pyaurorax.search.SOURCE_TYPE_* variables.
            display_name (str): 
                the new display name for the data source, defaults to `None`
            metadata (Dict): 
                the new metadata for the data source, defaults to `None`
            maintainers (str): 
                the new maintainer AuroraX account email addresses, defaults to `None`
            ephemeris_metadata_schema (List[Dict]): 
                a list of dictionaries capturing the metadata keys and values that can 
                appear in ephemeris records associated with the data source, defaults to `None`
            data_product_metadata_schema (List[Dict]): 
                a list of dictionaries capturing the metadata keys and values that can appear 
                in data product records associated with the data source, defaults to `None`

        Returns:
            the updated `DataSource` record

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: error during API call
            pyaurorax.exceptions.AuroraXUnauthorizedError: not allowed to perform task, or API key / user permissions are invalid
            pyaurorax.exceptions.AuroraXNotFoundError: data source not found
        """
        return func_update(
            self.__aurorax_obj,
            identifier,
            program,
            platform,
            instrument_type,
            source_type,
            display_name,
            metadata,
            owner,
            maintainers,
            ephemeris_metadata_schema,
            data_product_metadata_schema,
        )
