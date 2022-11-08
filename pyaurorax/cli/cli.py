import requests
import click
import pyaurorax
from .availability import commands as availability_commands
from .conjunctions import commands as conjunctions_commands
from .data_products import commands as data_products_commands
from .ephemeris import commands as ephemeris_commands
from .sources import commands as sources_commands
from .util import commands as util_commands

# default context settings
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


class Config(object):
    def __init__(self, verbose=False, api_key=None):
        self.verbose = verbose
        self.api_key = api_key


def __test_connectivity(quiet=False, return_json=False):
    # make request
    try:
        r = requests.get(pyaurorax.api.get_base_url(), timeout=pyaurorax.api.REQUEST_TIMEOUT)
    except requests.exceptions.Timeout:
        click.echo("Error connecting to AuroraX API, got a %d response" % (r.status_code))
        return

    # check status code
    if (r.status_code == 200):
        if (quiet is False):
            click.echo("Connectivity to the AuroraX API looks good!")
        if (return_json is True):
            return r.json()
    else:
        click.echo("Error connecting to AuroraX API, got a %d response" % (r.status_code))


@click.group(invoke_without_command=True)
@click.version_option(version="0.13.0")
@click.option("--api-key", type=str, help="Specify an API key")
@click.option("--api-base-url", type=str, help="Set the AuroraX API base URL")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--test-connectivity", is_flag=True, help="Test connectivity to AuroraX API")
@click.pass_context
def cli(ctx, api_key, api_base_url, verbose, test_connectivity):
    """
    Welcome to the AuroraX CLI program!

    This program is meant to provide an easy interface with AuroraX
    from the command line. It uses the PyAuroraX library behind the scenes.
    """
    # set config
    ctx.obj = Config(verbose=verbose, api_key=api_key)

    # set the API base URL
    if (api_base_url is not None):
        pyaurorax.api.set_base_url(api_base_url)

    # authenticate
    if (api_key is not None):
        pyaurorax.authenticate(api_key)

    # evaluate options
    if (ctx.invoked_subcommand is None):
        if (test_connectivity is True):
            # evalualte --test-connectivity
            __test_connectivity(quiet=False)
        else:
            # no options called, output the help
            click.echo("""Welcome to the AuroraX CLI program!

This program is meant to provide an easy interface with AuroraX from the
command line. It uses the PyAuroraX library behind the scenes.

To learn more about usage, type:

  $> aurorax-cli --help
""")
    else:
        # subcommand was called, move on to that
        pass


# add sub commands
cli.add_command(availability_commands.availability_group)
cli.add_command(conjunctions_commands.conjunctions_group)
cli.add_command(data_products_commands.data_products_group)
cli.add_command(ephemeris_commands.ephemeris_group)
cli.add_command(sources_commands.sources_group)
cli.add_command(util_commands.utility_group)
