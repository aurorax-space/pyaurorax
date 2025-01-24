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
Class definition for a criteria block used for conjunction searches
"""

from typing import Literal, Dict, List, Optional


class GroundCriteriaBlock:
    """
    Representation of a ground criteria block used for conjunction searches. 

    Attributes:
        programs (List[str]): 
            List of program strings to use in this criteria block. Optional, default is `[]`.
        
        platforms (List[str]): 
            List of platform strings to use in this criteria block. Optional, default is `[]`.

        instrument_types (List[str]): 
            List of instrument type strings to use in this criteria block. Optional, default is `[]`.

        hemisphere (List[str]): 
            List of hemisphere strings to use in this criteria block. Valid values are 'northern' 
            or 'southern'. Optional, default is `[]`.
    """

    def __init__(
            self,
            programs: List[str] = [],
            platforms: List[str] = [],
            instrument_types: List[str] = [],
            metadata_filters: Optional[Dict] = None  # need to change to MetadataFilters object
    ):
        self.programs = programs
        self.platforms = platforms
        self.instrument_types = instrument_types
        self.metadata_filters = metadata_filters

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "GroundCriteriaBlock(programs=%s, platforms=%s, instrument_types=%s, metadata_filters=%s)" % (
            self.programs,
            self.platforms,
            self.instrument_types,
            self.metadata_filters,
        )

    def pretty_print(self):
        """
        A special print output for this class.
        """
        # set special strings
        max_len = 80
        metadata_filters_str = str(self.metadata_filters)
        if (len(metadata_filters_str) > max_len):
            metadata_filters_str = "%s...)" % (metadata_filters_str[0:max_len])

        # print
        print("GroundCriteriaBlock:")
        print("  %-18s: %s" % ("programs", self.programs))
        print("  %-18s: %s" % ("platforms", self.platforms))
        print("  %-18s: %s" % ("instrument_types", self.instrument_types))
        print("  %-18s: %s" % ("metadata_filters", metadata_filters_str))


class SpaceCriteriaBlock:
    """
    Representation of a space criteria block used for conjunction searches. 

    Attributes:
        programs (List[str]): 
            List of program strings to use in this criteria block. Optional, default is `[]`.
        
        platforms (List[str]): 
            List of platform strings to use in this criteria block. Optional, default is `[]`.

        instrument_types (List[str]): 
            List of instrument type strings to use in this criteria block. Optional, default is `[]`.

        hemisphere (List[str]): 
            List of hemisphere strings to use in this criteria block. Valid values are 'northern' 
            or 'southern'. Optional, default is `[]`.
    """

    def __init__(
            self,
            programs: List[str] = [],
            platforms: List[str] = [],
            instrument_types: List[str] = [],
            hemisphere: List[Literal["northern", "southern"]] = [],
            metadata_filters: Optional[Dict] = None  # need to change to MetadataFilters object
    ):
        self.programs = programs
        self.platforms = platforms
        self.instrument_types = instrument_types
        self.hemisphere = hemisphere
        self.metadata_filters = metadata_filters

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "SpaceCriteriaBlock(programs=%s, platforms=%s, instrument_types=%s, hemisphere=%s, metadata_filters=%s)" % (
            self.programs,
            self.platforms,
            self.instrument_types,
            self.hemisphere,
            self.metadata_filters,
        )

    def pretty_print(self):
        """
        A special print output for this class.
        """
        # set special strings
        max_len = 80
        metadata_filters_str = str(self.metadata_filters)
        if (len(metadata_filters_str) > max_len):
            metadata_filters_str = "%s...)" % (metadata_filters_str[0:max_len])

        # print
        print("SpaceCriteriaBlock:")
        print("  %-18s: %s" % ("programs", self.programs))
        print("  %-18s: %s" % ("platforms", self.platforms))
        print("  %-18s: %s" % ("instrument_types", self.instrument_types))
        print("  %-18s: %s" % ("hemisphere", self.hemisphere))
        print("  %-18s: %s" % ("metadata_filters", metadata_filters_str))

    def to_search_query_dict(self):
        query_dict = self.__dict__
        query_dict["ephemeris_metadata_filters"] = None if self.metadata_filters is None else self.metadata_filters.__dict__
        del query_dict["metadata_filters"]
        return query_dict
