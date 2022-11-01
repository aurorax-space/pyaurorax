import sys
import click
import datetime
import humanize
import pyaurorax
from typing import List
from texttable import Texttable


@click.group("availability", help="Retrieve data availability")
def availability_group():
    pass


def __print_availability_table(type: str,
                               availability: List[pyaurorax.availability.AvailabilityResult],
                               order: str) -> None:
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
        if (type == "ephemeris"):
            dates_and_counts = a.available_ephemeris
        elif (type == "data products"):
            dates_and_counts = a.available_data_products
        else:
            click.echo("Unexpected error occurred, please open an issue on "
                       "the Github repository detailing how you were able "
                       "to make this message appear")

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
    table_headers = ["Identifier", "Display Name", "Program",
                     "Platform", "Instrument Type", "Source Type",
                     "Date", "Available Records"]
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
        table.add_row([table_identifiers[i],
                       table_display_names[i],
                       table_programs[i],
                       table_platforms[i],
                       table_instrument_types[i],
                       table_source_types[i],
                       table_dates[i],
                       table_counts[i]])
    click.echo(table.draw())


@availability_group.command("ephemeris",
                            short_help="Get ephemeris data availability info")
@click.argument("start_date", type=str)
@click.argument("end_date", type=str)
@click.option("--program", type=str, help="The program to filter for")
@click.option("--platform", type=str, help="The platform to filter for")
@click.option("--instrument-type", type=str, help="The instrument type to filter for")
@click.option("--source-type", type=str, help="The source type to filter for")
@click.option("--order", type=click.Choice(["identifier", "program", "platform",
                                            "instrument_type", "display_name"]),
              default="identifier", show_default=True,
              help="Order results using a certain column")
@click.option("--reversed", "reversed_", is_flag=True, help="Reverse ordering")
@click.pass_obj
def ephemeris(config, start_date, end_date, program, platform, instrument_type, source_type,
              order, reversed_):
    """
    Get data availability information about ephemeris records

    \b
    START_DATE    the start date to retrieve info for, inclusive (YYYY/MM/DD)
    END_DATE      the end date to retrieve info for, inclusive (YYYY/MM/DD)
    """
    # set start and end datetime objects
    try:
        start_dt = datetime.datetime.strptime(start_date, "%Y/%m/%d")
    except Exception as e:
        click.echo("Error parsing start date, make sure it is in YYYY/MM/DD format (%s)" % (str(e)))
        sys.exit(1)
    try:
        end_dt = datetime.datetime.strptime(end_date, "%Y/%m/%d")
    except Exception as e:
        click.echo("Error parsing end date, make sure it is in YYYY/MM/DD format (%s)" % (str(e)))
        sys.exit(1)

    # get availability info
    try:
        a = pyaurorax.availability.ephemeris(start_dt,
                                             end_dt,
                                             program=program,
                                             platform=platform,
                                             instrument_type=instrument_type,
                                             source_type=source_type)
    except pyaurorax.AuroraXException as e:
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


@availability_group.command("data_products",
                            short_help="Get data products data availability info")
@click.argument("start_date", type=str)
@click.argument("end_date", type=str)
@click.option("--program", type=str, help="The program to filter for")
@click.option("--platform", type=str, help="The platform to filter for")
@click.option("--instrument-type", type=str, help="The instrument type to filter for")
@click.option("--source-type", type=str, help="The source type to filter for")
@click.option("--order", type=click.Choice(["identifier", "program", "platform",
                                            "instrument_type", "display_name"]),
              default="identifier", show_default=True,
              help="Order results using a certain column")
@click.option("--reversed", "reversed_", is_flag=True, help="Reverse ordering")
@click.pass_obj
def data_products(config, start_date, end_date, program, platform, instrument_type, source_type,
                  order, reversed_):
    """
    Get data availability information about data product records

    \b
    START_DATE    the start date to retrieve info for, inclusive (YYYY/MM/DD)
    END_DATE      the end date to retrieve info for, inclusive (YYYY/MM/DD)
    """
    # set start and end datetime objects
    try:
        start_dt = datetime.datetime.strptime(start_date, "%Y/%m/%d")
    except Exception as e:
        click.echo("Error parsing start date, make sure it is in YYYY/MM/DD format (%s)" % (str(e)))
        sys.exit(1)
    try:
        end_dt = datetime.datetime.strptime(end_date, "%Y/%m/%d")
    except Exception as e:
        click.echo("Error parsing end date, make sure it is in YYYY/MM/DD format (%s)" % (str(e)))
        sys.exit(1)

    # get availability info
    try:
        a = pyaurorax.availability.data_products(start_dt,
                                                 end_dt,
                                                 program=program,
                                                 platform=platform,
                                                 instrument_type=instrument_type,
                                                 source_type=source_type)
    except pyaurorax.AuroraXException as e:
        click.echo("%s occurred: %s" % (type(e).__name__, e.args[0]))
        sys.exit(1)

    # print it out nicely
    __print_availability_table("data products", a, order)
