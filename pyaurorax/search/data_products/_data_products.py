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
Functions for performing data product searches
"""

import datetime
import humanize
import numpy as np
from .classes.data_product import DataProductData
from .classes.search import DataProductSearch
from ..api import AuroraXAPIRequest
from ..sources.classes.data_source import FORMAT_DEFAULT
from ..sources._sources import get_using_identifier
from ...exceptions import (
    AuroraXError,
    AuroraXAPIError,
    AuroraXSearchError,
    AuroraXUploadError,
)

__STANDARD_POLLING_SLEEP_TIME: float = 1.0  # Polling sleep time when waiting for data (after the initial sleep time), in seconds


def __validate_data_source(aurorax_obj, identifier, records):
    # get data source
    try:
        ds = get_using_identifier(aurorax_obj, identifier, FORMAT_DEFAULT, False)
    except AuroraXAPIError as e:
        if ("no data source record found" in str(e).lower()):
            raise AuroraXAPIError("Data source with identifier %d could not be found" % (identifier)) from e
        else:
            raise e

    # process each record to make sure the program/platform/instrument_type matches
    # the identifier found for the data source
    for record in records:
        if not (record.data_source.program == ds.program and record.data_source.platform == ds.platform
                and record.data_source.instrument_type == ds.instrument_type):
            return record

    # found no bad records
    return None


def search(aurorax_obj, start, end, programs, platforms, instrument_types, data_product_types, metadata_filters, metadata_filters_logical_operator,
           response_format, poll_interval, return_immediately, verbose):
    # create a search object
    s = DataProductSearch(aurorax_obj,
                          start,
                          end,
                          programs=programs,
                          platforms=platforms,
                          instrument_types=instrument_types,
                          data_product_types=data_product_types,
                          metadata_filters=metadata_filters,
                          metadata_filters_logical_operator=metadata_filters_logical_operator,
                          response_format=response_format)
    if (verbose is True):
        print("[%s] Search object created" % (datetime.datetime.now()))

    # execute the search
    s.execute()
    if (verbose is True):
        print("[%s] Request submitted" % (datetime.datetime.now()))
        print("[%s] Request ID: %s" % (datetime.datetime.now(), s.request_id))
        print("[%s] Request details available at: %s" % (datetime.datetime.now(), s.request_url))

    # return immediately if we wanted to
    if (return_immediately is True):
        return s

    # wait for data
    if (verbose is True):
        print("[%s] Waiting for data ..." % (datetime.datetime.now()))
    s.wait(poll_interval=poll_interval, verbose=verbose)

    # check if error condition encountered
    if (s.status["search_result"]["error_condition"] is True):
        # error encountered
        raise AuroraXSearchError(s.logs[-1]["summary"])

    # get the data
    if (verbose is True):
        print("[%s] Retrieving data ..." % (datetime.datetime.now()))
    s.get_data()

    # return response with the data
    if (verbose is True):
        print("[%s] Retrieved %s of data containing %d records" % (
            datetime.datetime.now(),
            humanize.filesize.naturalsize(s.status["search_result"]["file_size"]),  # type: ignore
            s.status["search_result"]["result_count"],
        ))
    return s


def upload(aurorax_obj, identifier, all_records, validate_source, chunk_size):
    # validate record sources if the flag is set
    if (validate_source is True):
        validation_error = __validate_data_source(aurorax_obj, identifier, all_records)
        if (validation_error is not None):
            raise AuroraXError("Unable to validate data source found in record: {}".format(validation_error))

    # translate each data product record to a request-friendly
    # dict (ie. convert datetimes to strings, etc.)
    for i, _ in enumerate(all_records):
        if (isinstance(all_records[i], DataProductData) is True):
            all_records[i] = all_records[i].to_json_serializable()

    # chunk up the records
    #
    # NOTE: we do this so that upload requests that are large are able to
    # more consistently succeed. If a call is to upload 10,000 records, we
    # under-the-hood chunk it up into N-record calls.
    if (len(all_records) > chunk_size):
        chunked_indexes = np.array_split(np.array(range(0, len(all_records)), dtype=np.int32), int(np.floor(len(all_records) / chunk_size)))
    else:
        chunked_indexes = [np.arange(0, len(all_records), dtype=np.int32)]
    for idxs in chunked_indexes:
        records = []
        for idx in idxs:
            records.append(all_records[idx])

        # make request
        url = "%s/%s" % (aurorax_obj.api_base_url, aurorax_obj.search.api.URL_SUFFIX_DATA_PRODUCTS_UPLOAD.format(identifier))
        req = AuroraXAPIRequest(aurorax_obj, method="post", url=url, body=records, null_response=True)
        res = req.execute()

        # evaluate response
        if (res.status_code == 400):
            if isinstance(res.data, list):
                raise AuroraXUploadError("%s - %s" % (res.status_code, res.data[0]["message"]))
            raise AuroraXUploadError("%s - %s" % (res.data["error_code"], res.data["error_message"]))

    # return
    return 0


def delete_urls(aurorax_obj, data_source, urls):
    # check to make sure the identifier, program, platform, and instrument type are all set in the data source
    if not all([data_source.identifier, data_source.program, data_source.platform, data_source.instrument_type]):
        raise AuroraXError("One or more required data source parameters are missing, delete operation aborted")

    # do request
    url = "%s/%s" % (aurorax_obj.api_base_url, aurorax_obj.search.api.URL_SUFFIX_DATA_PRODUCTS_UPLOAD.format(data_source.identifier))
    params = {
        "program": data_source.program,
        "platform": data_source.platform,
        "instrument_type": data_source.instrument_type,
        "urls": urls,
    }
    delete_req = AuroraXAPIRequest(aurorax_obj, method="delete", url=url, body=params, null_response=True)
    res = delete_req.execute()

    # evaluate response
    if (res.status_code == 400):
        raise AuroraXAPIError("%s - %s" % (res.data["error_code"], res.data["error_message"]))

    # return
    return 0


def delete(aurorax_obj, data_source, start, end, data_product_types):
    # check to make sure the identifier, program, platform, and instrument type are all set in the data source
    if not all([data_source.identifier, data_source.program, data_source.platform, data_source.instrument_type]):
        raise AuroraXError("One or more required data source parameters are missing, delete operation aborted")

    # do request to get all data products between start and end datetimes
    try:
        s = search(aurorax_obj,
                   start,
                   end,
                   programs=[data_source.program],
                   platforms=[data_source.platform],
                   instrument_types=[data_source.instrument_type],
                   data_product_types=[] if not data_product_types else data_product_types,
                   metadata_filters=None,
                   metadata_filters_logical_operator=None,
                   response_format=None,
                   poll_interval=__STANDARD_POLLING_SLEEP_TIME,
                   return_immediately=False,
                   verbose=False)
    except Exception as e:
        raise AuroraXError(e) from e

    # collect URLs from search result
    urls = []
    for dp in s.data:
        urls.append(dp.url)

    # do delete request
    return delete_urls(aurorax_obj, data_source, urls)


def describe(aurorax_obj, search_obj, query_dict):
    # set query
    if (search_obj is not None):
        query = search_obj.query
    elif (query_dict is not None):
        query = query_dict
    else:
        raise AuroraXError("One of 'search_obj' or 'query_dict' must be supplied")

    # make request
    url = "%s/%s" % (aurorax_obj.api_base_url, aurorax_obj.search.api.URL_SUFFIX_DESCRIBE_DATA_PRODUCTS_QUERY)
    req = AuroraXAPIRequest(aurorax_obj, method="post", url=url, body=query)
    res = req.execute()

    # return
    return res.data


def get_request_url(aurorax_obj, request_id):
    url = "%s/%s" % (aurorax_obj.api_base_url, aurorax_obj.search.api.URL_SUFFIX_DATA_PRODUCTS_REQUEST.format(request_id))
    return url
