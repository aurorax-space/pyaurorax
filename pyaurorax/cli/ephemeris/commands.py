import sys
import click
import pprint
import pyaurorax
from ..helpers import (print_request_logs_table,
                       print_request_status)


@click.group("ephemeris", help="Interact with ephemeris searches")
def ephemeris_group():
    pass


@ephemeris_group.command("get_status",
                         short_help="Get status info for an ephemeris search request")
@click.argument("request_uuid", type=str)
@click.option("--show-logs", "show_logs", is_flag=True,
              help="Show the logs for the request")
@click.option("--show-query", "show_query", is_flag=True,
              help="Show the query for the request")
@click.option("--filter-logs",
              type=click.Choice(["debug", "info", "warn", "error"]),
              help="Filter log messages (used with --show-logs)")
@click.pass_obj
def get_status(config, request_uuid, show_logs, show_query, filter_logs):
    """
    Get information for an ephemeris search request

    \b
    REQUEST_UUID    the request unique identifier
    """
    # get request status
    try:
        url = pyaurorax.api.urls.ephemeris_request_url.format(request_uuid)
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
                         filter_logs=filter_logs)


@ephemeris_group.command("get_logs",
                         short_help="Get logs for an ephemeris search request")
@click.argument("request_uuid", type=str)
@click.option("--filter", "--filter-logs", "filter_",
              type=click.Choice(["debug", "info", "warn", "error"]),
              help="Filter log messages")
@click.pass_obj
def get_logs(config, request_uuid, filter_):
    """
    Get the logs for an ephemeris search request

    \b
    REQUEST_UUID    the request unique identifier
    """
    # get request status
    try:
        url = pyaurorax.api.urls.ephemeris_request_url.format(request_uuid)
        s = pyaurorax.requests.get_status(url)
    except pyaurorax.AuroraXUnexpectedEmptyResponse as e:
        click.echo("%s occurred: request ID not found" % (type(e).__name__))
        sys.exit(1)
    except pyaurorax.AuroraXException as e:
        click.echo("%s occurred: %s" % (type(e).__name__, e.args[0]))
        sys.exit(1)

    # print out the logs nicely
    if ("logs" in s):
        print_request_logs_table(s["logs"], filter_level=filter_)
    else:
        click.echo("Search logs: missing, unable to display")


@ephemeris_group.command("get_query",
                         short_help="Get query for an ephemeris search request")
@click.argument("request_uuid", type=str)
@click.pass_obj
def get_query(config, request_uuid):
    """
    Get the query for an ephemeris search request

    \b
    REQUEST_UUID    the request unique identifier
    """
    # get request status
    try:
        url = pyaurorax.api.urls.ephemeris_request_url.format(request_uuid)
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