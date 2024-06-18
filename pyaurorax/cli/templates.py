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
This module contains the templates for different search
requests (conjunction, data products, ephemeris)
"""

CONJUNCTION_SEARCH_TEMPLATE = {
    "start": "2020-01-01T00:00:00",
    "end": "2020-01-01T23:59:59",
    "ground": [{
        "programs": ["string"],
        "platforms": ["string"],
        "instrument_types": ["string"],
        "ephemeris_metadata_filters": {
            "logical_operator": "AND",
            "expressions": [{
                "key": "string",
                "operator": "=",
                "values": ["string"]
            }]
        }
    }],
    "space": [{
        "programs": ["string"],
        "platforms": ["string"],
        "instrument_types": ["string"],
        "hemisphere": ["northern"],
        "ephemeris_metadata_filters": {
            "logical_operator": "AND",
            "expressions": [{
                "key": "string",
                "operator": "=",
                "values": ["string"]
            }]
        }
    }],
    "events": [{
        "programs": ["string"],
        "platforms": ["string"],
        "instrument_types": ["string"],
        "ephemeris_metadata_filters": {
            "logical_operator": "AND",
            "expressions": [{
                "key": "string",
                "operator": "=",
                "values": ["string"]
            }]
        }
    }],
    "conjunction_types": ["nbtrace"],
    "max_distances": {
        "ground1-space1": 300,
        "ground2-space1": 400,
        "ground1-events1": 900,
        "space1-space2": None
    }
}

DATA_PRODUCTS_SEARCH_TEMPLATE = {
    "start": "2020-01-01T00:00:00",
    "end": "2020-01-01T23:59:59",
    "data_sources": {
        "programs": ["string"],
        "platforms": ["string"],
        "instrument_types": ["string"],
        "data_product_metadata_filters": {
            "logical_operator": "AND",
            "expressions": [{
                "key": "string",
                "operator": "=",
                "values": ["string"]
            }]
        }
    },
    "data_product_type_filters": ["keogram"]
}

EPHEMERIS_SEARCH_TEMPLATE = {
    "start": "2020-01-01T00:00:00",
    "end": "2020-01-01T23:59:59",
    "data_sources": {
        "programs": ["string"],
        "platforms": ["string"],
        "instrument_types": ["string"],
        "ephemeris_metadata_filters": {
            "logical_operator": "AND",
            "expressions": [{
                "key": "string",
                "operator": "=",
                "values": ["string"]
            }]
        }
    },
}
