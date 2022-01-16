"""
This module contains the templates for different search
requests (conjunction, data products, ephemeris)
"""

CONJUNCTION_SEARCH_TEMPLATE = {
    "start": "2020-01-01T00:00:00",
    "end": "2020-01-01T23:59:59",
    "ground": [
        {
            "programs": [
                "string"
            ],
            "platforms": [
                "string"
            ],
            "instrument_types": [
                "string"
            ],
            "ephemeris_metadata_filters": {
                "logical_operator": "AND",
                "expressions": [
                    {
                        "key": "string",
                        "operator": "=",
                        "values": [
                            "string"
                        ]
                    }
                ]
            }
        }
    ],
    "space": [
        {
            "programs": [
                "string"
            ],
            "platforms": [
                "string"
            ],
            "instrument_types": [
                "string"
            ],
            "hemisphere": [
                "northern"
            ],
            "ephemeris_metadata_filters": {
                "logical_operator": "AND",
                "expressions": [
                    {
                        "key": "string",
                        "operator": "=",
                        "values": [
                            "string"
                        ]
                    }
                ]
            }
        }
    ],
    "events": [
        {
            "programs": [
                "string"
            ],
            "platforms": [
                "string"
            ],
            "instrument_types": [
                "string"
            ],
            "ephemeris_metadata_filters": {
                "logical_operator": "AND",
                "expressions": [
                    {
                        "key": "string",
                        "operator": "=",
                        "values": [
                            "string"
                        ]
                    }
                ]
            }
        }
    ],
    "conjunction_types": [
        "nbtrace"
    ],
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
        "programs": [
            "string"
        ],
        "platforms": [
            "string"
        ],
        "instrument_types": [
            "string"
        ],
        "data_product_metadata_filters": {
            "logical_operator": "AND",
            "expressions": [
                {
                    "key": "string",
                    "operator": "=",
                    "values": [
                        "string"
                    ]
                }
            ]
        }
    },
    "data_product_type_filters": [
        "keogram"
    ]
}


EPHEMERIS_SEARCH_TEMPLATE = {
    "start": "2020-01-01T00:00:00",
    "end": "2020-01-01T23:59:59",
    "data_sources": {
        "programs": [
            "string"
        ],
        "platforms": [
            "string"
        ],
        "instrument_types": [
            "string"
        ],
        "ephemeris_metadata_filters": {
            "logical_operator": "AND",
            "expressions": [
                {
                    "key": "string",
                    "operator": "=",
                    "values": [
                        "string"
                    ]
                }
            ]
        }
    },
}
