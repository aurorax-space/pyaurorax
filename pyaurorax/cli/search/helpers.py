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

import sys
import os
import click
import pprint
import datetime
import humanize
import textwrap
import warnings
import json
import pyaurorax
from dateutil.parser import parse
from termcolor import colored
from texttable import Texttable
from ...search.api import URL_SUFFIX_CONJUNCTION_REQUEST, URL_SUFFIX_DATA_PRODUCTS_REQUEST, URL_SUFFIX_EPHEMERIS_REQUEST


def __echo_helper(message, show_times=False):
    if (show_times is True):
        click.echo("[%s] %s" % (datetime.datetime.now(), message))
    else:
        click.echo(message)


def print_request_logs_table(logs, filter_level=None, table_max_width=None, truncate=True):
    """
    Function to print request logs table

    This is a shared helper function because it is used by the
    conjunction, data products, and ephemeris command modules.
    """
    # init
    default_wrap_threshold = 70
    if (table_max_width is None):
        try:
            terminal_columns = os.get_terminal_size().columns
            wrap_threshold = terminal_columns - 38 - 5  # 38 is the size level+timestamp, 5 for some padding
            if (wrap_threshold < 0):
                warnings.warn("Terminal width is too small, using default table width which might not look good", stacklevel=1)
                wrap_threshold = default_wrap_threshold
        except Exception:
            wrap_threshold = default_wrap_threshold
    else:
        wrap_threshold = table_max_width - 38 - 5  # 38 is the size level+timestamp, 5 for some padding
        if (wrap_threshold < 0):
            warnings.warn("Terminal width is too small, using default table width which might not look good", stacklevel=1)
            wrap_threshold = default_wrap_threshold

    # set table lists
    table_levels = []
    table_summaries = []
    table_timestamps = []
    for log in logs:
        if (filter_level is None or log["level"] == filter_level):
            table_levels.append(log["level"])
            if (truncate is True and len(log["summary"]) > 1000):
                table_summaries.append('\n'.join(textwrap.wrap(log["summary"][0:1000] + "...", wrap_threshold)))
            else:
                table_summaries.append('\n'.join(textwrap.wrap(log["summary"], wrap_threshold)))
            table_timestamps.append(parse(log["timestamp"], ignoretz=True))
    # set header values
    table_headers = ["Timestamp", "Level", "Summary"]

    # output information
    table = Texttable(max_width=400)
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(["t"] * len(table_headers))
    table.set_header_align(["l"] * len(table_headers))
    table.set_cols_align(["l"] * len(table_headers))
    table.header(table_headers)
    for i in range(0, len(table_timestamps)):
        table.add_row([table_timestamps[i], table_levels[i], table_summaries[i]])
    click.echo(table.draw())


def print_request_status(aurorax_obj, s, show_logs=False, show_query=False, filter_logs=None, table_max_width=None):
    """
    Function to print request status information

    This is a shared helper function because it is used by the
    conjunction, data products, and ephemeris command modules.
    """
    # set formatted output variables
    request_completed = colored("False", "yellow")
    request_completed_timestamp = "-"
    request_started_timestamp = parse(s["search_request"]["requested"], ignoretz=True)
    error_condition = "-"
    query_duration = "-"
    data_url = "-"
    file_size = "-"
    result_count = "-"
    if (s["search_result"]["completed_timestamp"] is not None):
        # set completed and completed timestamp
        request_completed = "True"
        request_completed_timestamp = parse(s["search_result"]["completed_timestamp"], ignoretz=True)

        # humanize some values
        query_duration = "%s (%.0fms)" % (humanize.precisedelta(
            datetime.timedelta(milliseconds=s["search_result"]["query_duration"])), s["search_result"]["query_duration"])
        data_url = "%s%s" % (aurorax_obj.api_base_url, s["search_result"]["data_uri"])
        file_size = humanize.naturalsize(s["search_result"]["file_size"])
        result_count = humanize.intcomma(s["search_result"]["result_count"])

        # set error condition
        error_condition = "False"
        if (s["search_result"]["error_condition"] is True):
            error_condition = colored("True", "red")

    # print out status nicely
    click.echo("Completed:\t\t%s" % (request_completed))
    click.echo("Requested timestamp:\t%s" % (request_started_timestamp))
    click.echo("Completed timestamp:\t%s" % (request_completed_timestamp))
    click.echo("Query duration:\t\t%s" % (query_duration))
    click.echo("Error condition:\t%s" % (error_condition))
    click.echo("Data URL:\t\t%s" % (data_url))
    click.echo("File size:\t\t%s" % (file_size))
    click.echo("Result count:\t\t%s" % (result_count))

    # print out logs if we asked for them
    if (show_logs is True):
        if ("logs" in s):
            click.echo()
            print_request_logs_table(s["logs"], filter_level=filter_logs, table_max_width=table_max_width)
        else:
            click.echo("Search logs: missing, unable to display")

    # print out query if we asked for it
    if (show_query is True):
        if ("query" in s["search_request"]):
            click.echo("\nSearch query:\n==================")
            query_to_show = s["search_request"]["query"]
            del query_to_show["request_id"]
            click.echo(pprint.pformat(query_to_show))
        else:
            click.echo("\nSearch query: missing, unable to display")


def get_search_data(aurorax_obj, type, request_uuid, outfile, output_to_terminal, indent, minify, show_times=False, search_obj=None):
    """
    Function to get search request data

    This is a shared helper function because it is used by the conjunction, data products, 
    and ephemeris command modules. Some IF statements are used to differentiate between the
    commands.
    """
    # get the data
    try:
        # check the status if we need to
        if (search_obj is None):
            # set status url
            __echo_helper("Checking request status ...", show_times=show_times)
            if (type == "conjunctions"):
                url = "%s/%s" % (aurorax_obj.api_base_url, URL_SUFFIX_CONJUNCTION_REQUEST.format(request_uuid))
            elif (type == "data_products"):
                url = "%s/%s" % (aurorax_obj.api_base_url, URL_SUFFIX_DATA_PRODUCTS_REQUEST.format(request_uuid))
            elif (type == "ephemeris"):
                url = "%s/%s" % (aurorax_obj.api_base_url, URL_SUFFIX_EPHEMERIS_REQUEST.format(request_uuid))
            else:
                click.echo("Unexpected error occurred, please open an issue on the Github repository detailing how "
                           "you were able to make this message appear")
                sys.exit(1)

            # get status
            try:
                s = aurorax_obj.search.requests.get_status(url)
            except pyaurorax.AuroraXNotFoundError:
                click.echo("Error: request ID not found")
                sys.exit(1)

            # check status
            if (s["search_result"]["completed_timestamp"] is None):
                click.echo("Error: Search is not done yet, not retrieving data")
                click.echo("\nNote: you can use the get_status command to "
                           "check if the search has completed. Try the command "
                           "\"aurorax-cli %s get_status %s\"" % (type, request_uuid))
                sys.exit(1)

            # set data url
            data_url = "%s/data" % (url)
        else:
            s = search_obj.status
            data_url = search_obj.data_url

        # get data
        try:
            __echo_helper(
                "Downloading %s results and %s of data ..." % (
                    humanize.intcomma(s["search_result"]["result_count"]),
                    humanize.naturalsize(s["search_result"]["file_size"]),
                ),
                show_times=show_times,
            )
            data = aurorax_obj.search.requests.get_data(data_url, skip_serializing=True)
        except pyaurorax.AuroraXDataRetrievalError as e:
            # parse error message
            if ("NotFound" in (str(e))):
                click.echo("\n%s" % ('\n'.join(
                    textwrap.wrap(
                        "Error downloading data: this request is too old and the data "
                        "file has been removed on the server. You can re-run the "
                        "search using the command \"aurorax-cli %s "
                        "search_resubmit %s\"." % (type, request_uuid), 110))))
            else:
                __echo_helper("Error downloading data: %s" % (str(e)), show_times=show_times)
            sys.exit(1)
    except pyaurorax.AuroraXNotFoundError as e:
        click.echo("%s occurred: request ID not found" % (type(e).__name__))  # type: ignore
        sys.exit(1)
    except pyaurorax.AuroraXError as e:
        __echo_helper("%s occurred: %s" % (type(e).__name__, e.args[0]), show_times=show_times)  # type: ignore
        sys.exit(1)

    # order data
    if (type == "conjunctions"):
        data = sorted(data, key=lambda x: x["start"])
    elif (type == "data_products"):
        data = sorted(data, key=lambda x: x["start"])
    elif (type == "ephemeris"):
        data = sorted(data, key=lambda x: x["epoch"])

    # save data to file, or print out
    if (output_to_terminal is not None):
        # print out to the terminal (don't save to file)
        #
        # format the data to objects if that was requested
        click.echo()  # one line spacer
        if (output_to_terminal == "dict"):
            # print dict format
            pprint.pprint(data)
        else:
            # serialize the data and print
            for d in data:
                if (type == "conjunctions"):
                    # serialize into Conjunction object
                    d_serialized = pyaurorax.search.Conjunction(**d)
                elif (type == "data_products"):
                    # serialize into DataProduct object
                    d_serialized = pyaurorax.search.DataProductData(**d)
                elif (type == "ephemeris"):
                    # serialize into Ephemeris object
                    d_serialized = pyaurorax.search.EphemerisData(**d)
                else:
                    click.echo("Unexpected error occurred, please open an issue on the Github repository detailing "
                               "how you were able to make this message appear")
                    sys.exit(1)

                # print to terminal
                click.echo(d_serialized)
    else:
        # write to file
        #
        # set filename
        if (outfile is None):
            outfile = "%s_data.json" % (request_uuid)

        # write data to the file
        __echo_helper("Writing data to file ...", show_times=show_times)
        with open(outfile, 'w', encoding="utf-8") as fp:
            if (minify is True):
                json.dump(data, fp)
            else:
                json.dump(data, fp, indent=indent)
        __echo_helper("Data has been saved to '%s'" % (outfile), show_times=show_times)
