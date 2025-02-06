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
Class definition for a conjunction
"""

import datetime
from typing import Dict, List
from ...sources import DataSource

# conjunction type - north b-trace
CONJUNCTION_TYPE_NBTRACE: str = "nbtrace"
"""
Conjunction search 'conjunction_type' category for finding conjunctions using the north B-trace data
"""

# conjunction type - south b-trace
CONJUNCTION_TYPE_SBTRACE: str = "sbtrace"
"""
Conjunction search 'conjunction_type' category for finding conjunctions using the south B-trace data
"""

# conjunction type - geographic
CONJUNCTION_TYPE_GEOGRAPHIC: str = "geographic"
"""
Conjunction search 'conjunction_type' category for finding conjunctions using the geographic position data
"""


class Conjunction:
    """
    Conjunction object

    Attributes:
        conjunction_type (str): 
            The type of location data used when the conjunction was found (either `nbtrace`, 
            `sbtrace`, or `geographic`)
            
        start (datetime.datetime): 
            Start timestamp of the conjunction

        end (datetime.datetime): 
            End timestamp of the conjunction

        data_sources (List[DataSource]): 
            Data sources in the conjunction

        min_distance (float): 
            Minimum kilometer distance of the conjunction

        max_distance (float): 
            Maximum kilometer distance of the conjunction

        events (List[Dict]): 
            The sub-conjunctions that make up this over-arching conjunction (the conjunctions 
            between each set of two data sources)

        closest_epoch (datetime.datetime): 
            Timestamp for when data sources were closest

        farthest_epoch (datetime.datetime): 
            Timestamp for when data sources were farthest
    """

    def __init__(
        self,
        conjunction_type: str,
        start: datetime.datetime,
        end: datetime.datetime,
        data_sources: List[DataSource],
        min_distance: float,
        max_distance: float,
        events: List[Dict],
        closest_epoch: datetime.datetime,
        farthest_epoch: datetime.datetime,
    ):
        self.conjunction_type = conjunction_type
        self.start = start
        self.end = end
        self.data_sources = data_sources
        self.min_distance = min_distance
        self.max_distance = max_distance
        self.events = events
        self.closest_epoch = closest_epoch
        self.farthest_epoch = farthest_epoch

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"Conjunction(start={repr(self.start)}, end={repr(self.end)}, min_distance={self.min_distance:.2f}, " \
            f"max_distance={self.max_distance:.2f}, data_sources=[...], events=[...])"

    def pretty_print(self):
        """
        A special print output for this class.
        """
        # set special strings
        if (len(self.data_sources) == 1):  # pragma: nocover-ok
            data_sources_str = "[%d data source]" % (len(self.data_sources))
        else:
            data_sources_str = "[%d data sources]" % (len(self.data_sources))
        if (len(self.events) == 1):
            events_str = "[%d event]" % (len(self.events))
        else:
            events_str = "[%d events]" % (len(self.events))

        # print
        print("Conjunction:")
        print("  %-18s: %s" % ("conjunction_type", self.conjunction_type))
        print("  %-18s: %s" % ("start", self.start))
        print("  %-18s: %s" % ("end", self.end))
        print("  %-18s: %s" % ("data_sources", data_sources_str))
        print("  %-18s: %s" % ("min_distance", self.min_distance))
        print("  %-18s: %s" % ("max_distance", self.max_distance))
        print("  %-18s: %s" % ("events", events_str))
        print("  %-18s: %s" % ("closest_epoch", self.closest_epoch))
        print("  %-18s: %s" % ("farthest_epoch", self.farthest_epoch))
