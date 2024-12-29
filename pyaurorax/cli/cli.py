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

import requests
import click
import pyaurorax
from .search import search_group

# default context settings
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


class Config(object):

    def __init__(self, verbose=False, api_key=None, api_base_url=None):
        self.verbose = verbose
        self.aurorax = pyaurorax.PyAuroraX()
        if (api_key is not None):
            self.aurorax.api_key = api_key
        if (api_base_url is not None):
            self.aurorax.api_base_url = api_base_url


def __test_connectivity(aurorax, quiet=False, return_json=False):
    # make request
    click.echo("Checking connectivity to %s ...\n" % (aurorax.api_base_url))
    try:
        r = requests.get(aurorax.api_base_url, timeout=aurorax.api_timeout)
    except requests.RequestException as e:
        click.echo("Error connecting to AuroraX API: %s" % (str(e)))
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
@click.version_option(version="1.8.0")
@click.option("--api-key", type=str, help="Specify an API key")
@click.option("--api-base-url", type=str, help="Set the AuroraX API base URL")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--test-connectivity", is_flag=True, help="Test connectivity to AuroraX API")
@click.pass_context
def cli(ctx, api_key, api_base_url, verbose, test_connectivity):
    """
    Welcome to the PyAuroraX CLI program!

    This program is meant to provide an easy interface with AuroraX
    from the command line. It uses the PyAuroraX library behind the scenes.
    """
    # set config
    ctx.obj = Config(verbose=verbose, api_key=api_key, api_base_url=api_base_url)

    # evaluate options
    if (ctx.invoked_subcommand is None):
        if (test_connectivity is True):
            # evaluate --test-connectivity
            __test_connectivity(ctx.obj.aurorax, quiet=False)
        else:
            # no options called, output the help
            click.echo("""Welcome to the PyAuroraX CLI program!

This program is meant to provide an easy interface with AuroraX from the
command line.

To learn more about usage, type:

  $> aurorax-cli --help
""")
    else:
        # subcommand was called, move on to that
        pass


# add sub commands
cli.add_command(search_group)
