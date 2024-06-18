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
Class definition for a data product
"""

import datetime
from typing import Dict, Optional
from ...sources.classes.data_source import DataSource

# keogram data product type
DATA_PRODUCT_TYPE_KEOGRAM = "keogram"
"""
Data product type for keograms. Keograms are a 2-D
representation of a series of images, and are one of
the most popular data products that auroral science
uses. More information can be found at
https://docs.aurorax.space/about_the_data/standards/#keograms.
"""

# montage data product type
DATA_PRODUCT_TYPE_MONTAGE = "montage"
"""
Data product type for montages. Like keograms, montages are
another representation of a series of images. However, montages
are not a 2D representation but rather a collage of thumnbail
images for the period of time. An example can be found at
https://data.phys.ucalgary.ca/sort_by_project/THEMIS/asi/stream2/2021/12/28/gill_themis19/20211228__gill_themis19_full-montage.pgm.jpg
"""

# movie data product type
DATA_PRODUCT_TYPE_MOVIE = "movie"
"""
Data product type for movies. Movies are timelapse video
files of auroral data, usually as MP4 or MPEG. They can
consist of frames for a whole night, or an hour, and can
be at any cadence that is most appropriate.
"""

# summary plot data product type
DATA_PRODUCT_TYPE_SUMMARY_PLOT = "summary_plot"
"""
Data product type for summary plots. A summary plot can be any type
of plot that shows auroral data in a summary format, for example a
background-subtracted meridian scanning photometer plot showing
counts in Rayleighs.
"""

# data availability data product type
DATA_PRODUCT_TYPE_DATA_AVAILABILITY = "data_availability"
"""
Data product type for data availability. The AuroraX data availability
system does not account for times when data was not expected to be
collected, such as summer shutdowns due to inadequate night hours. This
data product type for 'data availability' is meant to be used as a smarter
data availability mechanism for Aurora.
"""


class DataProductData:
    """
    Data product object

    Attributes:
        data_source: data source that the ephemeris record is associated with
        data_product_type: data product type ("keogram", "movie", "summary_plot")
        start: starting timestamp for the record (assumed it is in UTC), inclusive
        end: ending timestamp for the record (assumed it is in UTC), inclusive
        url: the URL of data product
        metadata: metadata for this record (arbitrary keys and values)
    """

    def __init__(
        self,
        data_source: DataSource,
        data_product_type: str,
        start: datetime.datetime,
        end: datetime.datetime,
        url: str,
        metadata: Optional[Dict] = None,
    ):
        self.data_source = data_source
        self.data_product_type = data_product_type
        self.start = start
        self.end = end
        self.url = url
        self.metadata = metadata

    def to_json_serializable(self) -> Dict:
        """
        Convert object to a JSON-serializable object (ie. translate
        datetime objects to strings)

        Returns:
            a dictionary object that is JSON-serializable
        """
        # init
        d = self.__dict__

        # format epoch as str
        if (type(d["start"]) is datetime.datetime):
            d["start"] = d["start"].strftime("%Y-%m-%dT%H:%M:00.000")
        if (type(d["end"]) is datetime.datetime):
            d["end"] = d["end"].strftime("%Y-%m-%dT%H:%M:00.000")

        # format metadata
        if (self.metadata is not None):
            for key, value in self.metadata.items():
                if (isinstance(value, datetime.datetime) is True or isinstance(value, datetime.date) is True):
                    self.metadata[key] = self.metadata[key].strftime("%Y-%m-%dT%H:%M:%S.%f")
        # if (isinstance(self.metadata, list) is True):
        #     self.metadata = {}

        # format data source fields for query
        d["program"] = self.data_source.program
        d["platform"] = self.data_source.platform
        d["instrument_type"] = self.data_source.instrument_type
        del d["data_source"]

        # return
        return d

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        # shorten the metadata and url
        max_len = 20
        attr_metadata = f"{self.metadata}"
        if (len(attr_metadata) > max_len):
            attr_metadata = attr_metadata[0:max_len] + "...}"
        attr_url = f"{self.url}"
        if (len(attr_url) > max_len):
            attr_url = attr_url[0:max_len] + "..."

        # return formatted representation
        return f"DataProductData(start={repr(self.start)}, end={repr(self.end)}, data_product_type='{self.data_product_type}', " \
            f"url='{attr_url}', metadata={attr_metadata}, data_source=DataSource(...))"
