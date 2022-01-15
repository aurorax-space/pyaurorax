import sys
import click
import pprint
import pyaurorax
from ..helpers import (print_request_logs_table,
                       print_request_status,
                       get_search_data)


@click.group("conjunctions", help="Interact with conjunction searches")
def conjunctions_group():
    pass


@conjunctions_group.command("get_status",
                            short_help="Get status info for a conjunction search request")
@click.argument("request_uuid", type=str)
@click.option("--show-logs", "show_logs", is_flag=True,
              help="Show the logs for the request")
@click.option("--show-query", "show_query", is_flag=True,
              help="Show the query for the request")
@click.option("--filter-logs",
              type=click.Choice(["debug", "info", "warn", "error"]),
              help="Filter log messages (used with --show-logs)")
@click.option("--table-max-width", "--max-width", type=int,
              help="Max width for the logs table")
@click.pass_obj
def get_status(config, request_uuid, show_logs, show_query, filter_logs, table_max_width):
    """
    Get information for a conjunction search request

    \b
    REQUEST_UUID    the request unique identifier
    """
    # get request status
    try:
        url = pyaurorax.api.urls.conjunction_request_url.format(request_uuid)
        s = pyaurorax.requests.get_status(url)
    except pyaurorax.AuroraXUnexpectedEmptyResponse as e:
        click.echo("%s occurred: request ID not found" % (type(e).__name__))
        sys.exit(1)
    except pyaurorax.AuroraXException as e:
        click.echo("%s occurred: %s" % (type(e).__name__, e.args[0]))
        sys.exit(1)

    # print status nicely
    print_request_status(s,
                         show_logs=show_logs,
                         show_query=show_query,
                         filter_logs=filter_logs,
                         table_max_width=table_max_width)


@conjunctions_group.command("get_logs",
                            short_help="Get logs for a conjunction search request")
@click.argument("request_uuid", type=str)
@click.option("--filter", "--filter-logs", "filter_",
              type=click.Choice(["debug", "info", "warn", "error"]),
              help="Filter log messages")
@click.option("--table-max-width", "--max-width", type=int,
              help="Max width for the logs table")
@click.pass_obj
def get_logs(config, request_uuid, filter_, table_max_width):
    """
    Get the logs for a conjunction search request

    \b
    REQUEST_UUID    the request unique identifier
    """
    # get request status
    try:
        url = pyaurorax.api.urls.conjunction_request_url.format(request_uuid)
        s = pyaurorax.requests.get_status(url)
    except pyaurorax.AuroraXUnexpectedEmptyResponse as e:
        click.echo("%s occurred: request ID not found" % (type(e).__name__))
        sys.exit(1)
    except pyaurorax.AuroraXException as e:
        click.echo("%s occurred: %s" % (type(e).__name__, e.args[0]))
        sys.exit(1)

    # print out the logs nicely
    if ("logs" in s):
        print_request_logs_table(s["logs"],
                                 filter_level=filter_,
                                 table_max_width=table_max_width)
    else:
        click.echo("Search logs: missing, unable to display")


@conjunctions_group.command("get_query",
                            short_help="Get query for a conjunction search request")
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
        url = pyaurorax.api.urls.conjunction_request_url.format(request_uuid)
        s = pyaurorax.requests.get_status(url)
    except pyaurorax.AuroraXUnexpectedEmptyResponse as e:
        click.echo("%s occurred: request ID not found" % (type(e).__name__))
        sys.exit(1)
    except pyaurorax.AuroraXException as e:
        click.echo("%s occurred: %s" % (type(e).__name__, e.args[0]))
        sys.exit(1)

    # print out query
    if ("query" in s["search_request"]):
        query_to_show = s["search_request"]["query"]
        del query_to_show["request_id"]
        click.echo(pprint.pformat(query_to_show))
    else:
        click.echo("\nSearch query missing from request status, unable to display")


@conjunctions_group.command("get_data",
                            short_help="Get data for a conjunction search request")
@click.argument("request_uuid", type=str)
@click.option("--outfile", type=str, help="output file to save data to (a .json file)")
@click.option("--output-to-terminal", type=click.Choice(["dict", "objects"]),
              help="output data to terminal in a certain format (instead of to file)")
@click.option("--indent", type=int, default=2, show_default=True,
              help="intendation when saving data to file or printing in 'dict' form")
@click.option("--minify", is_flag=True, help="Minify the JSON data saved to file")
@click.pass_obj
def get_data(config, request_uuid, outfile, output_to_terminal, indent, minify):
    """
    Get the data for a conjunction search request

    \b
    REQUEST_UUID    the request unique identifier
    """
    get_search_data("conjunctions",
                    request_uuid,
                    outfile,
                    output_to_terminal,
                    indent,
                    minify)
