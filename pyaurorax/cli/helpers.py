import click
import pprint
import datetime
import humanize
import textwrap
import pyaurorax
from termcolor import colored
from texttable import Texttable


def print_request_logs_table(logs, filter_level=None):
    # init
    wrap_threshold = 70

    # set table lists
    table_levels = []
    table_summaries = []
    table_timestamps = []
    for log in logs:
        if (filter_level is None or log["level"] == filter_level):
            table_levels.append(log["level"])
            table_summaries.append('\n'.join(textwrap.wrap(log["summary"], wrap_threshold)))
            table_timestamps.append(datetime.datetime.strptime(log["timestamp"][0:-1],
                                                               "%Y-%m-%dT%H:%M:%S.%f"))
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
        table.add_row([table_timestamps[i],
                       table_levels[i],
                       table_summaries[i]])
    click.echo(table.draw())


def print_request_status(s, show_logs=False, show_query=False, filter_logs=None):
    # set formatted output variables
    request_completed = colored("False", "yellow")
    request_completed_timestamp = "-"
    request_started_timestamp = datetime.datetime.strptime(s["search_request"]["requested"][0:-1],
                                                           "%Y-%m-%dT%H:%M:%S.%f")
    error_condition = "-"
    query_duration = "-"
    data_url = "-"
    file_size = "-"
    result_count = "-"
    if (s["search_result"]["completed_timestamp"] is not None):
        # set completed and completed timestamp
        request_completed = colored("True", "green")
        request_completed_timestamp = datetime.datetime.strptime(s["search_result"]["completed_timestamp"][0:-1],
                                                                 "%Y-%m-%dT%H:%M:%S.%f")

        # humanize some values
        query_duration = "%s (%.0fms)" % (humanize.precisedelta(
            datetime.timedelta(milliseconds=s["search_result"]["query_duration"])),
            s["search_result"]["query_duration"])
        data_url = "%s%s" % (pyaurorax.api.get_base_url(), s["search_result"]["data_uri"])
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
            print_request_logs_table(s["logs"], filter_level=filter_logs)
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
