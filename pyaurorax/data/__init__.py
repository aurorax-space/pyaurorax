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
Instrument data downloading and reading module. This module presently has support 
for data provided by the University of Calgary, such as THEMIS ASI, REGO, and the 
Transition Region Explorer (TREx) instruments.
"""

from typing import List, Literal, Optional
from pyucalgarysrs.data import Dataset, Observatory
from texttable import Texttable
from .ucalgary import UCalgaryManager
from ..exceptions import AuroraXAPIError

__all__ = ["DataManager"]


class DataManager:
    """
    The DataManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    def __init__(self, aurorax_obj):
        self.__aurorax_obj = aurorax_obj

        # initialize sub-modules
        self.__ucalgary = UCalgaryManager(self.__aurorax_obj)

    # ------------------------------------------
    # properties for submodule managers
    # ------------------------------------------
    @property
    def ucalgary(self):
        """
        Access to the `ucalgary` submodule from within a PyAuroraX object.
        """
        return self.__ucalgary

    def list_datasets(self, name: Optional[str] = None, timeout: Optional[int] = None) -> List[Dataset]:
        """
        List available datasets from all providers

        Args:
            name (str): 
                Supply a name used for filtering. If that name is found in the available dataset 
                names received from the API, it will be included in the results. This parameter is
                optional.
            
            timeout (int): 
                Represents how many seconds to wait for the API to send data before giving up. The 
                default is 10 seconds, or the `api_timeout` value in the super class' `pyaurorax.PyAuroraX`
                object. This parameter is optional.
            
        Returns:
            A list of [`Dataset`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.Dataset)
            objects.
        
        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered.
        """
        # init
        datasets = []

        # get ucalgary datasets
        ucalgary_datasets = self.__ucalgary.list_datasets(name=name, timeout=timeout)

        # merge
        datasets = datasets + ucalgary_datasets

        # sort by name
        datasets = sorted(datasets, key=lambda x: x.name)

        # return
        return datasets

    def list_datasets_in_table(self, name: Optional[str] = None, max_width: int = 200, timeout: Optional[int] = None) -> None:
        """
        Print available datasets from all providers in a table

        Args:
            name (str): 
                Supply a name used for filtering. If that name is found in the available dataset 
                names received from the API, it will be included in the results. This parameter is
                optional.
            
            max_width (int): 
                Maximum width of the table. Default is `200`. This parameter is optional.

            timeout (int): 
                Represents how many seconds to wait for the API to send data before giving up. The 
                default is 10 seconds, or the `api_timeout` value in the super class' `pyaurorax.PyAuroraX`
                object. This parameter is optional.
            
        Returns:
            Printed table.

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered.
        """
        # get datasets
        datasets = self.list_datasets(name=name, timeout=timeout)

        # set table lists
        table_names = []
        table_providers = []
        table_levels = []
        table_doi_details = []
        table_short_descriptions = []
        for d in datasets:
            table_names.append(d.name)
            table_providers.append(d.provider)
            table_levels.append(d.level)
            table_doi_details.append(d.doi_details)
            table_short_descriptions.append(d.short_description)

        # set header values
        table_headers = [
            "Name",
            "Provider",
            "Level",
            "DOI Details",
            "Short Description",
        ]

        # print as table
        table = Texttable(max_width=max_width)
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(["t"] * len(table_headers))
        table.set_header_align(["l"] * len(table_headers))
        table.set_cols_align(["l"] * len(table_headers))
        table.header(table_headers)
        for i in range(0, len(table_names)):
            table.add_row([
                table_names[i],
                table_providers[i],
                table_levels[i],
                table_doi_details[i],
                table_short_descriptions[i],
            ])
        print(table.draw())

    def get_dataset(self, name: str, timeout: Optional[int] = None) -> Dataset:
        """
        Get a specific dataset

        Args:
            name (str): 
                The dataset name to get. Case is insensitive.

            timeout (int): 
                Represents how many seconds to wait for the API to send data before giving up. The 
                default is 10 seconds, or the `api_timeout` value in the super class' `pyaurorax.PyAuroraX`
                object. This parameter is optional.
            
        Returns:
            The found [`Dataset`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.Dataset)
            object. Raises an exception if not found.
        
        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered.
        """
        # init
        dataset = None

        # search ucalgary datasets
        try:
            ucalgary_dataset = self.__ucalgary.get_dataset(name, timeout=timeout)
            dataset = ucalgary_dataset
        except Exception:  # nosec
            pass

        # return
        if (dataset is None):
            # never could find it
            raise AuroraXAPIError("Dataset not found")
        else:
            return dataset

    def list_observatories(self,
                           instrument_array: Literal["themis_asi", "rego", "trex_rgb", "trex_nir", "trex_blue", "trex_spectrograph"],
                           uid: Optional[str] = None,
                           timeout: Optional[int] = None) -> List[Observatory]:
        """
        List information about observatories utilized by all providers.

        Args:
            instrument_array (str): 
                The instrument array to list observatories for. Valid values are: themis_asi, rego, 
                trex_rgb, trex_nir, trex_blue, and trex_spectrograph.

            uid (str): 
                Supply a observatory unique identifier used for filtering (usually 4-letter site code). If that UID 
                is found in the available observatories received from the API, it will be included in the results. This 
                parameter is optional.
            
            timeout (int): 
                Represents how many seconds to wait for the API to send data before giving up. The 
                default is 10 seconds, or the `api_timeout` value in the super class' `pyaurorax.PyAuroraX`
                object. This parameter is optional.
            
        Returns:
            A list of [`Observatory`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.Observatory)
            objects.
        
        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered.
        """
        # init
        observatories = []

        # get ucalgary datasets
        ucalgary_observatories = self.__ucalgary.list_observatories(instrument_array, uid=uid, timeout=timeout)

        # merge
        observatories = observatories + ucalgary_observatories

        # sort by name
        observatories = sorted(observatories, key=lambda x: x.uid)

        # return
        return observatories

    def list_observatories_in_table(self,
                                    instrument_array: Literal["themis_asi", "rego", "trex_rgb", "trex_nir", "trex_blue", "trex_spectrograph"],
                                    uid: Optional[str] = None,
                                    max_width: int = 200,
                                    timeout: Optional[int] = None) -> None:
        """
        Print available observatories for a given instrument array in a table

        Args:
            instrument_array (str): 
                The instrument array to list observatories for. Valid values are: themis_asi, rego, 
                trex_rgb, trex_nir, trex_blue, and trex_spectrograph.

            uid (str): 
                Supply a observatory unique identifier used for filtering (usually 4-letter site code). If that UID 
                is found in the available observatories received from the API, it will be included in the results. This 
                parameter is optional.
            
            max_width (int): 
                Maximum width of the table. Default is `200`. This parameter is optional.

            timeout (int): 
                Represents how many seconds to wait for the API to send data before giving up. The 
                default is 10 seconds, or the `api_timeout` value in the super class' `pyaurorax.PyAuroraX`
                object. This parameter is optional.
            
        Returns:
            Printed table.
        
        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered.
        """
        # get observatories
        observatories = self.list_observatories(instrument_array, uid=uid, timeout=timeout)

        # set table lists
        table_uids = []
        table_full_names = []
        table_geo_lats = []
        table_geo_lons = []
        table_providers = []
        for o in observatories:
            table_uids.append(o.uid)
            table_full_names.append(o.full_name)
            table_geo_lats.append(o.geodetic_latitude)
            table_geo_lons.append(o.geodetic_longitude)
            table_providers.append(o.provider)

        # set header values
        table_headers = [
            "UID",
            "Full Name",
            "Geodetic Latitude",
            "Geodetic Longitude",
            "Provider",
        ]

        # print as table
        table = Texttable(max_width=max_width)
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(["t"] * len(table_headers))
        table.set_header_align(["l"] * len(table_headers))
        table.set_cols_align(["l"] * len(table_headers))
        table.header(table_headers)
        for i in range(0, len(table_uids)):
            table.add_row([
                table_uids[i],
                table_full_names[i],
                table_geo_lats[i],
                table_geo_lons[i],
                table_providers[i],
            ])
        print(table.draw())
