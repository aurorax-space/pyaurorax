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
Data source statistics information
"""

import datetime
from typing import Optional


class DataSourceStatistics:
    """
    Data source statistics information

    Attributes:
        ephemeris_count (int): total number of ephemeris records for this data source
        data_product_count (int): total number of ephemeris records for this data source
        earliest_ephemeris_loaded (datetime.datetime): timestamp of the earliest ephemeris record
        latest_ephemeris_loaded (datetime.datetime): timestamp of the latest ephemeris record
        earliest_data_product_loaded (datetime.datetime): timestamp of the earliest data_product record
        latest_data_product_loaded (datetime.datetime): timestamp of the latest data product record
    """

    def __init__(self,
                 ephemeris_count: int,
                 data_product_count: int,
                 earliest_ephemeris_loaded: Optional[datetime.datetime] = None,
                 latest_ephemeris_loaded: Optional[datetime.datetime] = None,
                 earliest_data_product_loaded: Optional[datetime.datetime] = None,
                 latest_data_product_loaded: Optional[datetime.datetime] = None):
        self.ephemeris_count = ephemeris_count
        self.data_product_count = data_product_count
        self.earliest_ephemeris_loaded = earliest_ephemeris_loaded
        self.latest_ephemeris_loaded = latest_ephemeris_loaded
        self.earliest_data_product_loaded = earliest_data_product_loaded
        self.latest_data_product_loaded = latest_data_product_loaded

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "DataSourceStatistics(ephemeris_count=%d, data_product_count=%d, ...)" % (
            self.ephemeris_count,
            self.data_product_count,
        )

    def pretty_print(self):
        """
        A special print output for this class.
        """
        print("DataSourceStatistics:")
        print("  %-30s: %d" % ("ephemeris_count", self.ephemeris_count))
        print("  %-30s: %d" % ("data_product_count", self.data_product_count))
        print("  %-30s: %s" % ("earliest_ephemeris_loaded", self.earliest_ephemeris_loaded))
        print("  %-30s: %s" % ("latest_ephemeris_loaded", self.latest_ephemeris_loaded))
        print("  %-30s: %s" % ("earliest_data_product_loaded", self.earliest_data_product_loaded))
        print("  %-30s: %s" % ("latest_data_product_loaded", self.latest_data_product_loaded))
