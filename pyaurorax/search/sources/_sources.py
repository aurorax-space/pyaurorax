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

import warnings
import datetime
from .classes.data_source import DataSource, FORMAT_FULL_RECORD
from .classes.data_source_stats import DataSourceStatistics
from ..api import AuroraXAPIRequest
from ...exceptions import (
    AuroraXNotFoundError,
    AuroraXDuplicateError,
    AuroraXConflictError,
    AuroraXAPIError,
)


def __serialize_data_source_stats(stats):
    """
    Takes in raw JSON format of data source stats, serializes it 
    to a DataSourceStatistics object.
    
    NOTE: this is done specially instead of DataSourceStatistics(**ds) because
    the data source stats item returned by the API includes the data source itself, 
    and we don't need that extra bit. We strip it out when creating this
    DataSourceStatistics object.
    """
    # set ephemeris values
    earliest_ephemeris_loaded = None
    latest_ephemeris_loaded = None
    if (stats["earliest_ephemeris_loaded"] is not None):
        earliest_ephemeris_loaded = datetime.datetime.fromisoformat(stats["earliest_ephemeris_loaded"])
    if (stats["latest_ephemeris_loaded"] is not None):
        latest_ephemeris_loaded = datetime.datetime.fromisoformat(stats["latest_ephemeris_loaded"])

    # set data product values
    earliest_data_product_loaded = None
    latest_data_product_loaded = None
    if (stats["earliest_data_product_loaded"] is not None):
        earliest_data_product_loaded = datetime.datetime.fromisoformat(stats["earliest_data_product_loaded"])
    if (stats["latest_data_product_loaded"] is not None):
        latest_data_product_loaded = datetime.datetime.fromisoformat(stats["latest_data_product_loaded"])

    # return
    return DataSourceStatistics(
        ephemeris_count=stats["ephemeris_count"],
        data_product_count=stats["data_product_count"],
        earliest_ephemeris_loaded=earliest_ephemeris_loaded,
        latest_ephemeris_loaded=latest_ephemeris_loaded,
        earliest_data_product_loaded=earliest_data_product_loaded,
        latest_data_product_loaded=latest_data_product_loaded,
    )


def list(aurorax_obj, program, platform, instrument_type, source_type, owner, format, order, include_stats):
    # make request
    params = {
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "source_type": source_type,
        "owner": owner,
        "format": format,
        "include_stats": include_stats,
    }
    url = "%s/%s" % (aurorax_obj.api_base_url, aurorax_obj.search.api.URL_SUFFIX_DATA_SOURCES)
    req = aurorax_obj.search.api.AuroraXAPIRequest(aurorax_obj, method="get", url=url, params=params)
    res = req.execute()

    # order results
    res.data = sorted(res.data, key=lambda x: x[order])

    # cast
    sources = []
    if len(res.data):
        for ds in res.data:
            source = DataSource(**ds, format=format)
            if ("stats" in ds and ds["stats"] is not None):
                source.stats = __serialize_data_source_stats(ds["stats"])
            sources.append(source)
    else:
        return []

    # remove not_applicable sources
    sources_pruned = []
    for source in sources:
        if (source.identifier is not None and source.identifier >= 0):
            # exclude under-the-hood adhoc data sources
            sources_pruned.append(source)

    # return
    return sources_pruned


def search(aurorax_obj, programs, platforms, instrument_types, format, order, include_stats):
    # make request
    request_data = {
        "programs": programs,
        "platforms": platforms,
        "instrument_types": instrument_types,
    }
    params = {
        "format": format,
        "include_stats": include_stats,
    }
    url = "%s/%s" % (aurorax_obj.api_base_url, aurorax_obj.search.api.URL_SUFFIX_DATA_SOURCES_SEARCH)
    req = aurorax_obj.search.api.AuroraXAPIRequest(aurorax_obj, method="post", url=url, params=params, body=request_data)
    res = req.execute()

    # order results
    res.data = sorted(res.data, key=lambda x: x[order])

    # cast
    sources = []
    if len(res.data):
        for ds in res.data:
            source = DataSource(**ds, format=format)
            if ("stats" in ds and ds["stats"] is not None):
                source.stats = __serialize_data_source_stats(ds["stats"])
            sources.append(source)
    else:
        return []

    # return
    return sources


def get(aurorax_obj, program, platform, instrument_type, format, include_stats):
    # get the data source
    sources = list(aurorax_obj=aurorax_obj,
                   program=program,
                   platform=platform,
                   instrument_type=instrument_type,
                   source_type=None,
                   owner=None,
                   format=format,
                   order="identifier",
                   include_stats=include_stats)

    # set results to the first thing found
    if (len(sources) == 1):
        return sources[0]
    elif (len(sources) > 1):
        warnings.warn("Found more than one data source matching this criteria, returning the first (found %d)" % (len(sources)), stacklevel=1)
        return sources[0]
    else:
        raise AuroraXNotFoundError("No matching data source found")


def get_using_filters(aurorax_obj, program, platform, instrument_type, source_type, owner, format, order, include_stats):
    # get data sources
    sources = list(aurorax_obj=aurorax_obj,
                   program=program,
                   platform=platform,
                   instrument_type=instrument_type,
                   source_type=source_type,
                   owner=owner,
                   format=format,
                   order=order,
                   include_stats=include_stats)

    # return
    return sources


def get_using_identifier(aurorax_obj, identifier, format, include_stats):
    # make request
    params = {
        "format": format,
        "include_stats": include_stats,
    }
    url = "%s/%s/%d" % (aurorax_obj.api_base_url, aurorax_obj.search.api.URL_SUFFIX_DATA_SOURCES, identifier)
    req = AuroraXAPIRequest(aurorax_obj, method="get", url=url, params=params)
    res = req.execute()

    # cast
    data_source = DataSource(**res.data, format=format)
    if ("stats" in res.data and res.data["stats"] is not None):
        data_source.stats = __serialize_data_source_stats(res.data["stats"])

    # return
    return data_source


def add(aurorax_obj, ds):
    # check that the length of the program, platform, and instrument type is
    # within API constraints
    #
    # NOTE: this check is done here because the API will return a generic 500
    # error with no details that the issue was due to these values being too
    # long. If we run into situation where these limits need to be increased,
    # we can definitely do it. We just need to change the below IF-statements,
    # and change the API's database code. The constraints are embedded in the API
    # at the database level (within the data sources table constraints). Also
    # note that the source type also has a limit, but because we control these
    # ourselves, we don't need a check for it.
    if not all([ds.program, ds.platform, ds.instrument_type, ds.source_type, ds.display_name]):
        raise AuroraXAPIError("Missing required fields. To create a data source, the program, platform, " +
                              "instrument_type, source_type, and display_name, are all required")
    if (len(ds.program) > 200):
        raise AuroraXAPIError("Program too long. Must be less than 200 characters")
    if (len(ds.platform) > 50):
        raise AuroraXAPIError("Platform too long. Must be less than 50 characters")
    if (len(ds.instrument_type) > 200):
        raise AuroraXAPIError("Instrument type too long. Must be less than 200 characters")
    if (len(ds.display_name) > 50):
        raise AuroraXAPIError("Display name too long. Must be less than 50 characters")

    # set up request
    request_data = {
        "program": ds.program,
        "platform": ds.platform,
        "instrument_type": ds.instrument_type,
        "source_type": ds.source_type,
        "display_name": ds.display_name,
        "ephemeris_metadata_schema": ds.ephemeris_metadata_schema,
        "data_product_metadata_schema": ds.data_product_metadata_schema,
        "metadata": ds.metadata
    }
    if (ds.identifier is not None):
        request_data["identifier"] = ds.identifier

    # make request
    url = "%s/%s" % (aurorax_obj.api_base_url, aurorax_obj.search.api.URL_SUFFIX_DATA_SOURCES)
    req = AuroraXAPIRequest(aurorax_obj, method="post", url=url, body=request_data)
    res = req.execute()

    # evaluate response
    if (res.status_code == 409):
        raise AuroraXDuplicateError("%s - %s" % (res.data["error_code"], res.data["error_message"]))

    # return
    try:
        return DataSource(**res.data)
    except Exception:
        raise AuroraXAPIError("Could not create data source") from None


def delete(aurorax_obj, identifier):
    # do request
    url = "%s/%s/%d" % (aurorax_obj.api_base_url, aurorax_obj.search.api.URL_SUFFIX_DATA_SOURCES, identifier)
    req = AuroraXAPIRequest(aurorax_obj, method="delete", url=url, null_response=True)
    res = req.execute()

    # evaluate response
    if (res.status_code == 400):
        raise AuroraXAPIError("%s - %s" % (res.data["error_code"], res.data["error_message"]))
    elif (res.status_code == 409):
        raise AuroraXConflictError("%s - %s" % (res.data["error_code"], res.data["error_message"]))

    # return
    return 0


def update(aurorax_obj, identifier, program, platform, instrument_type, source_type, display_name, metadata, owner, maintainers,
           ephemeris_metadata_schema, data_product_metadata_schema):
    # create a data source
    ds = DataSource(identifier=identifier,
                    program=program,
                    platform=platform,
                    instrument_type=instrument_type,
                    source_type=source_type,
                    display_name=display_name,
                    metadata=metadata,
                    owner=owner,
                    maintainers=maintainers,
                    ephemeris_metadata_schema=ephemeris_metadata_schema,
                    data_product_metadata_schema=data_product_metadata_schema)

    # set URL and request data
    url = "%s/%s/%d" % (aurorax_obj.api_base_url, aurorax_obj.search.api.URL_SUFFIX_DATA_SOURCES, ds.identifier)
    req_data = ds.__dict__
    del req_data["stats"]
    del req_data["format"]

    # make request
    req = AuroraXAPIRequest(aurorax_obj, method="patch", url=url, body=req_data)
    req.execute()

    # return
    try:
        return get_using_identifier(aurorax_obj, ds.identifier, FORMAT_FULL_RECORD, False)
    except Exception:
        raise AuroraXAPIError("Could not update data source") from None
