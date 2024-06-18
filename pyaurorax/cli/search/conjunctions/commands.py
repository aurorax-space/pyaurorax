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
import pprint
import json
import os
import datetime
import pyaurorax
from dateutil.parser import parse
from ..helpers import (
    print_request_logs_table,
    print_request_status,
    get_search_data,
)
from ....search.api import URL_SUFFIX_CONJUNCTION_REQUEST
from ...templates import CONJUNCTION_SEARCH_TEMPLATE

# globals
__STANDARD_POLLING_SLEEP_TIME: float = 1.0
__BROWSER_TYPES = sorted([
    "default",
    "mozilla",
    "firefox",
    "netscape",
    "galeon",
    "epiphany",
    "skipstone",
    "kfmclient",
    "konqueror",
    "kfm",
    "mosaic",
    "opera",
    "grail",
    "links",
    "elinks",
    "lynx",
    "w3m",
    "windows-default",
    "macosx",
    "safari",
    "google-chrome",
    "chrome",
    "chromium",
    "chromium-browser",
])


def __create_search_object_from_query(aurorax_obj, q):
    start = parse(q["start"], ignoretz=True)
    end = parse(q["end"], ignoretz=True)
    max_distances = q["max_distances"]
    ground = None if "ground" not in q else q["ground"]
    space = None if "space" not in q else q["space"]
    events = None if "events" not in q else q["events"]
    conjunction_types = None if "conjunction_types" not in q else q["conjunction_types"]
    epoch_search_precision = None if "epoch_search_precision" not in q else q["epoch_search_precision"]
    s = pyaurorax.search.ConjunctionSearch(aurorax_obj,
                                           start,
                                           end,
                                           distance=max_distances,
                                           ground=ground,
                                           space=space,
                                           events=events,
                                           conjunction_types=conjunction_types,
                                           epoch_search_precision=epoch_search_precision)
    return s


@click.group("conjunctions", help="Interact with conjunction searches")
def conjunctions_group():
    pass


@conjunctions_group.command("get_status", short_help="Get status info for a conjunction search request")
@click.argument("request_uuid", type=str)
@click.option("--show-logs", "show_logs", is_flag=True, help="Show the logs for the request")
@click.option("--show-query", "show_query", is_flag=True, help="Show the query for the request")
@click.option("--filter-logs", type=click.Choice(["debug", "info", "warn", "error"]), help="Filter log messages (used with --show-logs)")
@click.option("--table-max-width", "--max-width", type=int, help="Max width for the logs table")
@click.pass_obj
def get_status(config, request_uuid, show_logs, show_query, filter_logs, table_max_width):
    """
    Get information for a conjunction search request

    \b
    REQUEST_UUID    the request unique identifier
    """
    # get request status
    try:
        url = "%s/%s" % (config.aurorax.api_base_url, URL_SUFFIX_CONJUNCTION_REQUEST.format(request_uuid))
        s = config.aurorax.search.requests.get_status(url)
    except pyaurorax.AuroraXNotFoundError as e:
        click.echo("%s occurred: request ID not found" % (type(e).__name__))
        sys.exit(1)
    except pyaurorax.AuroraXError as e:
        click.echo("%s occurred: %s" % (type(e).__name__, e.args[0]))
        sys.exit(1)

    # print status nicely
    print_request_status(
        config.aurorax,
        s,
        show_logs=show_logs,
        show_query=show_query,
        filter_logs=filter_logs,
        table_max_width=table_max_width,
    )


@conjunctions_group.command("get_logs", short_help="Get logs for a conjunction search request")
@click.argument("request_uuid", type=str)
@click.option("--filter", "--filter-logs", "filter_", type=click.Choice(["debug", "info", "warn", "error"]), help="Filter log messages")
@click.option("--table-max-width", "--max-width", type=int, help="Max width for the logs table")
@click.option("--no-truncate", is_flag=True, help="Do not truncate log messages that are >1000 characters long")
@click.pass_obj
def get_logs(config, request_uuid, filter_, table_max_width, no_truncate):
    """
    Get the logs for a conjunction search request

    \b
    REQUEST_UUID    the request unique identifier
    """
    # get request status
    try:
        url = "%s/%s" % (config.aurorax.api_base_url, URL_SUFFIX_CONJUNCTION_REQUEST.format(request_uuid))
        s = config.aurorax.search.requests.get_status(url)
    except pyaurorax.AuroraXNotFoundError as e:
        click.echo("%s occurred: request ID not found" % (type(e).__name__))
        sys.exit(1)
    except pyaurorax.AuroraXError as e:
        click.echo("%s occurred: %s" % (type(e).__name__, e.args[0]))
        sys.exit(1)

    # set truncate
    truncate = not no_truncate

    # print out the logs nicely
    if ("logs" in s):
        print_request_logs_table(s["logs"], filter_level=filter_, table_max_width=table_max_width, truncate=truncate)
    else:
        click.echo("Search logs: missing, unable to display")


@conjunctions_group.command("get_query", short_help="Get query for a conjunction search request")
@click.argument("request_uuid", type=str)
@click.pass_obj
def get_query(config, request_uuid):
    """
    Get the query for a conjunction search request

    \b
    REQUEST_UUID    the request unique identifier
    """
    # get request status
    try:
        url = "%s/%s" % (config.aurorax.api_base_url, URL_SUFFIX_CONJUNCTION_REQUEST.format(request_uuid))
        s = config.aurorax.search.requests.get_status(url)
    except pyaurorax.AuroraXNotFoundError as e:
        click.echo("%s occurred: request ID not found" % (type(e).__name__))
        sys.exit(1)
    except pyaurorax.AuroraXError as e:
        click.echo("%s occurred: %s" % (type(e).__name__, e.args[0]))
        sys.exit(1)

    # print out query
    if ("query" in s["search_request"]):
        query_to_show = s["search_request"]["query"]
        del query_to_show["request_id"]
        click.echo(pprint.pformat(query_to_show))
    else:
        click.echo("\nSearch query missing from request status, unable to display")


@conjunctions_group.command("get_data", short_help="Get data for a conjunction search request")
@click.argument("request_uuid", type=str)
@click.option("--outfile", type=str, help="Output file to save data to (a .json file)")
@click.option("--output-to-terminal", type=click.Choice(["dict", "objects"]), help="Output data to terminal in a certain format (instead of to file)")
@click.option("--indent", type=int, default=2, show_default=True, help="Indentation when saving data to file")
@click.option("--minify", is_flag=True, help="Minify the JSON data saved to file")
@click.pass_obj
def get_data(config, request_uuid, outfile, output_to_terminal, indent, minify):
    """
    Get the data for a conjunction search request

    \b
    REQUEST_UUID    the request unique identifier
    """
    get_search_data(config.aurorax, "conjunctions", request_uuid, outfile, output_to_terminal, indent, minify)


@conjunctions_group.command("search_resubmit", short_help="Resubmit a conjunction search request")
@click.argument("request_uuid", type=str)
@click.pass_obj
def search_resubmit(config, request_uuid):
    """
    Resubmit a conjunction search request

    \b
    REQUEST_UUID    the request unique identifier
    """
    # get request status
    try:
        click.echo("Retrieving query for request '%s' ..." % (request_uuid))
        url = "%s/%s" % (config.aurorax.api_base_url, URL_SUFFIX_CONJUNCTION_REQUEST.format(request_uuid))
        status = config.aurorax.search.requests.get_status(url)
    except pyaurorax.AuroraXNotFoundError as e:
        click.echo("%s occurred: request ID not found" % (type(e).__name__))
        sys.exit(1)
    except pyaurorax.AuroraXError as e:
        click.echo("%s occurred: %s" % (type(e).__name__, e.args[0]))
        sys.exit(1)

    # set the query to use for resubmission
    if ("query" not in status["search_request"]):
        click.echo("Error resubmitting: missing query from original request ID")
        sys.exit(1)
    q = status["search_request"]["query"]

    # create search object
    click.echo("Preparing new search ...")
    s = __create_search_object_from_query(config.aurorax, q)

    # submit search
    click.echo("Submitting new search ...")
    s.execute()

    # output new request ID
    click.echo("Request has been resubmitted, new request ID is %s" % (s.request_id))


@conjunctions_group.command("search_template", short_help="Output template for a conjunction search request")
@click.option("--outfile", type=str, help="Save template to a file")
@click.option("--indent", type=int, default=2, show_default=True, help="Indentation to use when outputting template")
@click.pass_obj
def search_template(config, outfile, indent):
    """
    Output template for a conjunction search request
    """
    if (outfile is not None):
        with open(outfile, 'w', encoding="utf-8") as fp:
            json.dump(CONJUNCTION_SEARCH_TEMPLATE, fp, indent=indent)  # type: ignore
        click.echo("Saved template to %s" % (outfile))
    else:
        click.echo(json.dumps(CONJUNCTION_SEARCH_TEMPLATE, indent=indent))


@conjunctions_group.command("search", short_help="Perform a conjunction search request")
@click.argument("infile", type=str)
@click.option("--poll-interval", default=__STANDARD_POLLING_SLEEP_TIME, show_default=True, help="Polling interval when waiting for data (seconds)")
@click.option("--outfile", type=str, help="Output file to save data to (a .json file)")
@click.option("--output-to-terminal", type=click.Choice(["dict", "objects"]), help="Output data to terminal in a certain format (instead of to file)")
@click.option("--indent", type=int, default=2, show_default=True, help="indentation when saving data to file")
@click.option("--minify", is_flag=True, help="Minify the JSON data saved to file")
@click.option("--quiet", is_flag=True, help="Quiet output")
@click.option("--swarmaurora-show-url", is_flag=True, help="Display the URL for displaying conjunction results in Swarm-Aurora")
@click.option("--swarmaurora-open-browser", is_flag=True, help="In a browser, open the conjunction results in Swarm-Aurora")
@click.option("--swarmaurora-browser-type",
              default="default",
              type=click.Choice(__BROWSER_TYPES),
              help="Output data to terminal in a certain format (instead of to file)")
@click.option("--swarmaurora-save-custom-import-file", is_flag=True, help="Generate a Swarm-Aurora custom import file for the search")
@click.pass_obj
def search(config, infile, poll_interval, outfile, output_to_terminal, indent, minify, quiet, swarmaurora_show_url, swarmaurora_open_browser,
           swarmaurora_browser_type, swarmaurora_save_custom_import_file):
    """
    Perform a conjunction search request

    \b
    INFILE      input file with query (must be a JSON)
    """
    # check that infile exists
    if not (os.path.exists(infile)):
        click.echo("Error: infile doesn't exist (%s)" % (infile))
        sys.exit(1)

    # read in infile
    if (quiet is False):
        click.echo("[%s] Reading in query file ..." % (datetime.datetime.now()))
    with open(infile, 'r', encoding="utf-8") as fp:
        q = json.load(fp)

    # set search params
    if (quiet is False):
        click.echo("[%s] Preparing search ..." % (datetime.datetime.now()))
    start = parse(q["start"], ignoretz=True)
    end = parse(q["end"], ignoretz=True)
    max_distances = q["max_distances"]
    ground = None if "ground" not in q else q["ground"]
    space = None if "space" not in q else q["space"]
    events = None if "events" not in q else q["events"]
    conjunction_types = None if "conjunction_types" not in q else q["conjunction_types"]
    epoch_search_precision = None if "epoch_search_precision" not in q else q["epoch_search_precision"]
    verbose_search = True if quiet is False else False

    # start search
    s = config.aurorax.search.conjunctions.search(start,
                                                  end,
                                                  distance=max_distances,
                                                  ground=ground,
                                                  space=space,
                                                  events=events,
                                                  conjunction_types=conjunction_types,
                                                  epoch_search_precision=epoch_search_precision,
                                                  poll_interval=poll_interval,
                                                  verbose=verbose_search,
                                                  return_immediately=True)

    # wait for data
    s.wait(poll_interval=poll_interval, verbose=verbose_search)

    # search has finished, save results to a file or output to terminal
    get_search_data(config.aurorax, "conjunctions", s.request_id, outfile, output_to_terminal, indent, minify, show_times=True, search_obj=s)

    # do Swarm-Aurora tasks if requested
    if (swarmaurora_save_custom_import_file is True):
        print("[%s] Generating Swarm-Aurora custom import file ..." % (datetime.datetime.now()))
        swarmaurora_custom_import_filename = config.aurorax.search.conjunctions.swarmaurora.create_custom_import_file(s)
        print("[%s] Saved Swarm-Aurora custom import file to '%s'" % (datetime.datetime.now(), swarmaurora_custom_import_filename))
    if (swarmaurora_show_url is True):
        url = config.aurorax.search.conjunctions.swarmaurora.get_url(s)
        print("[%s] Swarm-Aurora URL: %s" % (datetime.datetime.now(), url))
    if (swarmaurora_open_browser is True):
        print(("[%s] Launching a browser to show this conjunction search in "
               "Swarm-Aurora (browser='%s') ...") % (datetime.datetime.now(), swarmaurora_browser_type))
        if (swarmaurora_browser_type == "default"):
            swarmaurora_browser_type = None
        config.aurorax.search.conjunctions.swarmaurora.open_in_browser(s, browser=swarmaurora_browser_type)


@conjunctions_group.command("describe", short_help="Describe a conjunction search request")
@click.argument("infile", type=str)
@click.pass_obj
def describe(config, infile):
    """
    Describe a conjunction search request using
    "SQL-like" syntax

    \b
    INFILE      input file with query (must be a JSON)
    """
    # check that infile exists
    if not (os.path.exists(infile)):
        click.echo("Error: infile doesn't exist (%s)" % (infile))
        sys.exit(1)

    # read in infile
    with open(infile, 'r', encoding="utf-8") as fp:
        q = json.load(fp)

    # create search object
    s = __create_search_object_from_query(config.aurorax, q)

    # describe the search
    d = config.aurorax.search.conjunctions.describe(s)

    # output
    click.echo(d)
