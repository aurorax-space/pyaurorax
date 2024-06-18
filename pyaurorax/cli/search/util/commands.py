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
import click
import datetime
import pyaurorax
import humanize
from dateutil.parser import parse
from texttable import Texttable
from termcolor import colored

__ALLOWED_SEARCH_LISTING_TYPES = ["conjunction", "data_product", "ephemeris"]


def __print_requests_table(search_requests, order):
    # set table lists
    table_search_types = []
    table_active = []
    table_error_conditions = []
    table_file_sizes = []
    table_ip_addresses = []
    table_query_durations = []
    table_request_ids = []
    table_requested_timestamps = []
    table_result_counts = []
    table_file_exists = []
    for search_request in search_requests:
        # standard values
        table_search_types.append(search_request["search_type"])
        table_active.append(search_request["active"])
        table_ip_addresses.append(search_request["ip_address"])
        table_request_ids.append(search_request["request_id"])
        table_requested_timestamps.append(search_request["requested"])
        table_file_exists.append(search_request["result_file_exists"])

        # result count
        if (search_request["result_count"] is not None):
            table_result_counts.append(humanize.intcomma(search_request["result_count"]))
        else:
            table_result_counts.append("-")

        # query duration
        if (search_request["result_count"] is not None):
            table_query_durations.append(
                "%.03fs (%s)" % (search_request["query_duration"] / 1000.0, humanize.naturaldelta(search_request["query_duration"] / 1000.0)))
        else:
            table_query_durations.append("-")

        # file size
        if (search_request["result_count"] is not None):
            table_file_sizes.append(humanize.naturalsize(search_request["file_size"]))
        else:
            table_file_sizes.append("-")

        # file size
        if (search_request["file_size"] is not None):
            table_file_sizes.append(humanize.naturalsize(search_request["file_size"]))
        else:
            table_file_sizes.append("-")

        # error condition
        if (search_request["error_condition"] is True):
            table_error_conditions.append(colored("True", "red"))
        else:
            table_error_conditions.append(search_request["error_condition"])

    # set header values
    table_headers = [
        "Requested Timestamp",
        "Search Type",
        "Request ID",
        "IP Address",
        "Active",
        "Query Duration",
        "Result Count",
        "File Size",
        "Result File Exists",
        "Error Condition",
    ]
    for i in range(0, len(table_headers)):
        if (table_headers[i].lower().replace(' ', '_') == order):
            table_headers[i] += " " + "\u2193"

    # output information
    table = Texttable(max_width=400)
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(["t"] * len(table_headers))
    table.set_header_align(["l"] * len(table_headers))
    table.set_cols_align(["l"] * len(table_headers))
    table.header(table_headers)
    for i in range(0, len(table_request_ids)):
        table.add_row([
            table_requested_timestamps[i], table_search_types[i], table_request_ids[i], table_ip_addresses[i], table_active[i],
            table_query_durations[i], table_result_counts[i], table_file_sizes[i], table_file_exists[i], table_error_conditions[i]
        ])
    click.echo(table.draw())


@click.group("util", help="Utility commands")
def utility_group():
    pass


@utility_group.command("ground_to_nbtrace", short_help="Convert ground location to north B-trace location")
@click.argument("lat", type=click.FloatRange(min=-90.0, max=90.0))
@click.argument("lon", type=click.FloatRange(min=-180.0, max=180.0))
@click.option("--timestamp",
              type=str,
              default=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
              show_default=True,
              help="timestamp to use when converting in ISO format "
              "(YYYY-mm-ddTHH:MM:SS), defaults to current time")
@click.pass_obj
def ground_to_nbtrace(config, lat, lon, timestamp):
    """
    Convert a geographic location (assumed to be on the ground) to a north
    B-trace location. Note that the timestamp is needed since the B-trace
    values are derived using magnetic coordinates

    \n
    Important! If you supply negative numbers, prefix it with '--' to
    tell the terminal to not evaluate dash (-) characters as options
    after it. For example, "aurorax-cli util ground_to_nbtrace -- 90.0 -120.0"

    \b
    LAT    the latitude, in geographic coordinates (-90 to 90)
    LON    the longitude, in geographic coordinates (-180 to 180)
    """
    # set location object
    input_location = pyaurorax.search.Location(lat=lat, lon=lon)
    click.echo("Inputted location:\t%s" % (input_location))

    # interpret time
    ts = parse(timestamp)
    click.echo("Timestamp:\t\t%s" % (ts.isoformat()))

    # get nbtrace location
    nbtrace = config.aurorax.search.util.ground_geo_to_nbtrace(input_location, ts)

    # output
    click.echo("\nDerived north B-trace:\t%s" % (nbtrace))


@utility_group.command("ground_to_sbtrace", short_help="Convert ground location to south B-trace location")
@click.argument("lat", type=click.FloatRange(min=-90.0, max=90.0))
@click.argument("lon", type=click.FloatRange(min=-180.0, max=180.0))
@click.option("--timestamp",
              type=str,
              default=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
              show_default=True,
              help="timestamp to use when converting in ISO format "
              "(YYYY-mm-ddTHH:MM:SS), defaults to current time")
@click.pass_obj
def ground_to_sbtrace(config, lat, lon, timestamp):
    """
    Convert a geographic location (assumed to be on the ground) to a south
    B-trace location. Note that the timestamp is needed since the B-trace
    values are derived using magnetic coordinates

    \n
    Important! If you supply negative numbers, prefix it with '--' to
    tell the terminal to not evaluate dash (-) characters as options
    after it. For example, "aurorax-cli util ground_to_nbtrace -- 90.0 -120.0"

    \b
    LAT    the latitude, in geographic coordinates (-90 to 90)
    LON    the longitude, in geographic coordinates (-180 to 180)
    """
    # set location object
    input_location = pyaurorax.search.Location(lat=lat, lon=lon)
    click.echo("Inputted location:\t%s" % (input_location))

    # interpret time
    ts = parse(timestamp)
    click.echo("Timestamp:\t\t%s" % (ts.isoformat()))

    # get nbtrace location
    nbtrace = config.aurorax.search.util.ground_geo_to_sbtrace(input_location, ts)

    # output
    click.echo("\nDerived south B-trace:\t%s" % (nbtrace))


@utility_group.command("list_search_requests", short_help="List search requests using various filters (admins only)")
@click.option("--search-type", type=click.Choice(__ALLOWED_SEARCH_LISTING_TYPES), help="Filter based on search request type")
@click.option("--active", is_flag=True, help="Reverse ordering")
@click.option("--start", help="Filter based on request start timestamp (YYYY-mm-ddTHH:MM:SS)")
@click.option("--end", help="Filter based on request end timestamp (YYYY-mm-ddTHH:MM:SS)")
@click.option("--file-size", type=int, help="Filter based on results file size (in KB)")
@click.option("--result-count", type=int, help="Filter based on number of results found")
@click.option("--query-duration", type=int, help="Filter based on search query duration (in milliseconds)")
@click.option("--error-condition", type=bool, help="Filter based on error condition (true/false)")
@click.option("--order",
              type=click.Choice([
                  "search_type",
                  "active",
                  "error_condition",
                  "file_size",
                  "ip_address",
                  "query_duration",
                  "requested",
                  "result_count",
                  "result_file_exists",
              ]),
              default="requested",
              show_default=True,
              help="Order requests using a certain column")
@click.option("--second-order",
              type=click.Choice([
                  "search_type",
                  "active",
                  "error_condition",
                  "file_size",
                  "ip_address",
                  "query_duration",
                  "requested",
                  "result_count",
                  "result_file_exists",
              ]),
              default="requested",
              show_default=True,
              help="Order requests using a certain column")
@click.option("--limit", type=int, help="Limit output to N search requests")
@click.option("--reversed", "reversed_", is_flag=True, help="Reverse ordering")
@click.pass_obj
def list_search_requests(config, search_type, active, start, end, file_size, result_count, query_duration, error_condition, order, second_order,
                         limit, reversed_):
    """
    Retrieve a list of matching search requests (admins only)
    """
    # set start and end datetime objects
    start_dt = None
    end_dt = None
    if (start is not None):
        try:
            start_dt = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            click.echo("Error parsing start timestamp, make sure it is in YYYY-MM-DDTHH:MM:SS format (%s)" % (str(e)))
            sys.exit(1)
    if (end is not None):
        try:
            end_dt = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            click.echo("Error parsing end timestamp, make sure it is in YYYY-MM-DDTHH:MM:SS format (%s)" % (str(e)))
            sys.exit(1)

    # make request
    search_requests = config.aurorax.search.requests.list(search_type=search_type,
                                                          active=active,
                                                          start=start_dt,
                                                          end=end_dt,
                                                          file_size=file_size,
                                                          result_count=result_count,
                                                          query_duration=query_duration,
                                                          error_condition=error_condition)

    # order results
    search_requests = sorted(search_requests, key=lambda x: (x[order], x[second_order]))

    # reverse
    if (reversed_ is True):
        search_requests = list(reversed(search_requests))

    # limit
    if (limit is not None):
        search_requests = search_requests[0:limit]

    # print the table
    __print_requests_table(search_requests, order)


@utility_group.command("delete_search_request", short_help="Delete a search request (admins only)")
@click.argument("request_uuid", type=str)
@click.pass_obj
def delete_search_request(config, request_uuid):
    """
    Delete a search request from AuroraX (admins only)

    REQUEST_UUID     the request unique identifier
    """
    config.aurorax.search.requests.delete(request_uuid)
    click.echo("Successfully deleted request '%s'" % (request_uuid))
