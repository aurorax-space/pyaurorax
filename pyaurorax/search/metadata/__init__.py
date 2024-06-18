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
Interacting with the data source metadata schemas.

Note that all functions and classes from submodules are all imported
at this level of the metadata module. They can be referenced from
here instead of digging in deeper to the submodules.
"""

from typing import Dict, List, Optional
from ._metadata import get_ephemeris_schema as func_get_ephemeris_schema
from ._metadata import get_data_products_schema as func_get_data_products_schema
from ._metadata import validate as func_validate

__all__ = ["MetadataManager"]


class MetadataManager:
    """
    The MetadataManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    def __init__(self, aurorax_obj):
        self.__aurorax_obj = aurorax_obj

    def validate(self, schema: List[Dict], record: Dict, quiet: Optional[bool] = False) -> bool:
        """
        Validate a metadata record against a schema. This checks that the
        key names match and there aren't fewer or more keys than expected.

        Args:
            schema: the metadata schema to validate against
            record: metadata record to validate

        Returns:
            True if the metadata record is valid, False if it is not
        """
        return func_validate(schema, record, quiet)

    def get_ephemeris_schema(self, identifier: int) -> List[Dict]:
        """
        Retrieve the ephemeris metadata schema for a data source

        Args:
            identifier: the AuroraX data source ID

        Returns:
            the ephemeris metadata schema for the data source
        """
        return func_get_ephemeris_schema(self.__aurorax_obj, identifier)

    def get_data_products_schema(self, identifier: int) -> List[Dict]:
        """
        Retrieve the data products metadata schema for a data source

        Args:
            identifier: the AuroraX data source ID

        Returns:
            the data products metadata schema for the data source
        """
        return func_get_data_products_schema(self.__aurorax_obj, identifier)
