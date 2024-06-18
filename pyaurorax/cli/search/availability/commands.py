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
import humanize
import pyaurorax
from texttable import Texttable


@click.group("availability", help="Retrieve data availability")
def availability_group():
    pass


def __print_availability_table(type, availability, order):
    # check to see if there's anything to show
    if (len(availability) == 0):
        click.echo(f"No {type} availability information found!")
        return

    # set table lists
    table_identifiers = []
    table_programs = []
    table_platforms = []
    table_instrument_types = []
    table_source_types = []
    table_display_names = []
    table_dates = []
    table_counts = []
    for a in availability:
        # set which info to use, based on type
        dates_and_counts = None
        if (type == "ephemeris"):
            dates_and_counts = a.available_ephemeris
        elif (type == "data products"):
            dates_and_counts = a.available_data_products
        if (dates_and_counts is None):
            click.echo("Unexpected error occurred, please open an issue on the Github repository detailing "
                       "how you were able to make this message appear")
            return

        # for each date
        for date, count in dates_and_counts.items():
            table_identifiers.append(a.data_source.identifier)
            table_programs.append(a.data_source.program)
            table_platforms.append(a.data_source.platform)
            table_instrument_types.append(a.data_source.instrument_type)
            table_source_types.append(a.data_source.source_type)
            table_display_names.append(a.data_source.display_name)
            table_dates.append(date)
            table_counts.append(humanize.intcomma(count))

    # set header values
    table_headers = [
        "Identifier",
        "Display Name",
        "Program",
        "Platform",
        "Instrument Type",
        "Source Type",
        "Date",
        "Available Records",
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
    for i in range(0, len(table_identifiers)):
        table.add_row([
            table_identifiers[i],
            table_display_names[i],
            table_programs[i],
            table_platforms[i],
            table_instrument_types[i],
            table_source_types[i],
            table_dates[i],
            table_counts[i],
        ])
    click.echo(table.draw())


@availability_group.command("ephemeris", short_help="Get ephemeris data availability info")
@click.argument("start_date", type=str)
@click.argument("end_date", type=str)
@click.option("--program", type=str, help="The program to filter for")
@click.option("--platform", type=str, help="The platform to filter for")
@click.option("--instrument-type", type=str, help="The instrument type to filter for")
@click.option("--source-type", type=str, help="The source type to filter for")
@click.option("--order",
              type=click.Choice(["identifier", "program", "platform", "instrument_type", "display_name"]),
              default="identifier",
              show_default=True,
              help="Order results using a certain column")
@click.option("--reversed", "reversed_", is_flag=True, help="Reverse ordering")
@click.pass_obj
def ephemeris(config, start_date, end_date, program, platform, instrument_type, source_type, order, reversed_):
    """
    Get data availability information about ephemeris records

    \b
    START_DATE    the start date to retrieve info for, inclusive (valid formats: YYYY/MM/DD, YYYY-MM-DD, YYYYMMDD)
    END_DATE      the end date to retrieve info for, inclusive (valid formats: YYYY/MM/, YYYY-MM-DD, YYYYMMDD)
    """
    # set start and end datetime objects
    try:
        if ('/' in start_date):
            start_dt = datetime.datetime.strptime(start_date, "%Y/%m/%d")
        elif ('-' in start_date):
            start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        else:
            start_dt = datetime.datetime.strptime(start_date, "%Y%m%d")
    except Exception:
        click.echo("Error parsing start date, make sure it is in a valid format shown in help menu")
        sys.exit(1)
    try:
        if ('/' in end_date):
            end_dt = datetime.datetime.strptime(end_date, "%Y/%m/%d")
        elif ('-' in end_date):
            end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        else:
            end_dt = datetime.datetime.strptime(end_date, "%Y%m%d")
    except Exception:
        click.echo("Error parsing end date, make sure it is in a valid format shown in help menu")
        sys.exit(1)

    # get availability info
    try:
        a = config.aurorax.search.availability.ephemeris(start_dt,
                                                         end_dt,
                                                         program=program,
                                                         platform=platform,
                                                         instrument_type=instrument_type,
                                                         source_type=source_type)
    except pyaurorax.AuroraXError as e:
        click.echo("%s occurred: %s" % (type(e).__name__, e.args[0]))
        sys.exit(1)

    # order results
    if (order == "identifier"):
        a = sorted(a, key=lambda x: x.data_source.identifier)
    elif (order == "program"):
        a = sorted(a, key=lambda x: x.data_source.program)
    elif (order == "platform"):
        a = sorted(a, key=lambda x: x.data_source.platform)
    elif (order == "instrument_type"):
        a = sorted(a, key=lambda x: x.data_source.instrument_type)
    elif (order == "source_type"):
        a = sorted(a, key=lambda x: x.data_source.source_type)
    elif (order == "display_name"):
        a = sorted(a, key=lambda x: x.data_source.display_name)

    # reverse
    if (reversed_ is True):
        a = reversed(a)

    # print it out nicely
    __print_availability_table("ephemeris", a, order)


@availability_group.command("data_products", short_help="Get data products data availability info")
@click.argument("start_date", type=str)
@click.argument("end_date", type=str)
@click.option("--program", type=str, help="The program to filter for")
@click.option("--platform", type=str, help="The platform to filter for")
@click.option("--instrument-type", type=str, help="The instrument type to filter for")
@click.option("--source-type", type=str, help="The source type to filter for")
@click.option("--order",
              type=click.Choice(["identifier", "program", "platform", "instrument_type", "display_name"]),
              default="identifier",
              show_default=True,
              help="Order results using a certain column")
@click.option("--reversed", "reversed_", is_flag=True, help="Reverse ordering")
@click.pass_obj
def data_products(config, start_date, end_date, program, platform, instrument_type, source_type, order, reversed_):
    """
    Get data availability information about data product records

    \b
    START_DATE    the start date to retrieve info for, inclusive (valid formats: YYYY/MM/DD, YYYY-MM-DD, YYYYMMDD)
    END_DATE      the end date to retrieve info for, inclusive (valid formats: YYYY/MM/, YYYY-MM-DD, YYYYMMDD)
    """
    # set start and end datetime objects
    try:
        if ('/' in start_date):
            start_dt = datetime.datetime.strptime(start_date, "%Y/%m/%d")
        elif ('-' in start_date):
            start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        else:
            start_dt = datetime.datetime.strptime(start_date, "%Y%m%d")
    except Exception:
        click.echo("Error parsing start date, make sure it is in a valid format shown in help menu")
        sys.exit(1)
    try:
        if ('/' in end_date):
            end_dt = datetime.datetime.strptime(end_date, "%Y/%m/%d")
        elif ('-' in end_date):
            end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        else:
            end_dt = datetime.datetime.strptime(end_date, "%Y%m%d")
    except Exception:
        click.echo("Error parsing end date, make sure it is in a valid format shown in help menu")
        sys.exit(1)

    # get availability info
    try:
        a = config.aurorax.search.availability.data_products(start_dt,
                                                             end_dt,
                                                             program=program,
                                                             platform=platform,
                                                             instrument_type=instrument_type,
                                                             source_type=source_type)
    except pyaurorax.AuroraXError as e:
        click.echo("%s occurred: %s" % (type(e).__name__, e.args[0]))
        sys.exit(1)

    # reverse
    if (reversed_ is True):
        a = reversed(a)

    # print it out nicely
    __print_availability_table("data products", a, order)
