import sys
import click
import pyaurorax
from texttable import Texttable

# globals
SUPPORTED_SOURCE_TYPES = [
    pyaurorax.sources.SOURCE_TYPE_EVENT_LIST,
    pyaurorax.sources.SOURCE_TYPE_GROUND,
    pyaurorax.sources.SOURCE_TYPE_HEO,
    pyaurorax.sources.SOURCE_TYPE_LEO,
    pyaurorax.sources.SOURCE_TYPE_LUNAR,
]


@click.group("sources", help="Interact with data sources")
def sources_group():
    pass


@sources_group.command("list", short_help="List data sources")
@click.option("--program", type=str, help="Filter using program")
@click.option("--platform", type=str, help="Filter using platform")
@click.option("--instrument-type", type=str, help="Filter using instrument type")
@click.option("--source-type", type=click.Choice(SUPPORTED_SOURCE_TYPES),
              help="Filter using source type")
@click.option("--owner", type=str, help="Filter using an owner")
@click.option("--order", type=click.Choice(["identifier", "program", "platform",
                                            "instrument_type", "display_name",
                                            "owner"]),
              default="identifier", help="Order results using a certain column")
@click.option("--reversed", "reversed_", is_flag=True, help="Reverse ordering")
@click.pass_obj
def list(config, program, platform, instrument_type, source_type, owner, order, reversed_):
    """
    List data sources using the options to filter as desired
    """
    # get data sources
    try:
        sources = pyaurorax.sources.get_using_filters(program=program,
                                                      platform=platform,
                                                      instrument_type=instrument_type,
                                                      source_type=source_type,
                                                      owner=owner,
                                                      order=order)
    except pyaurorax.AuroraXException as e:
        click.echo("%s occurred: %s" % (type(e).__name__, e.args[0]))
        sys.exit(1)

    # reverse
    if (reversed_ is True):
        sources = reversed(sources)

    # set table lists
    table_identifiers = []
    table_programs = []
    table_platforms = []
    table_instrument_types = []
    table_source_types = []
    table_display_names = []
    table_owners = []
    for source in sources:
        table_identifiers.append(source.identifier)
        table_programs.append(source.program)
        table_platforms.append(source.platform)
        table_instrument_types.append(source.instrument_type)
        table_source_types.append(source.source_type)
        table_display_names.append(source.display_name)
        table_owners.append(source.owner)

    # set header values
    table_headers = ["Identifier", "Display Name", "Program",
                     "Platform", "Instrument Type", "Source Type",
                     "Owner"]
    for i in range(0, len(table_headers)):
        if (table_headers[i].lower().replace(' ', '_') == order):
            table_headers[i] += " " + "\u2193"

    # output information
    table = Texttable(max_width=400)
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype([
        't',  # text
        't',  # text
        't',  # text
        't',  # text
        't',  # text
        't',  # text
        't',  # text
    ])
    table.set_header_align(["l", "l", "l", "l", "l", "l", "l"])
    table.set_cols_align(["l", "l", "l", "l", "l", "l", "l"])
    table.header(table_headers)
    for i in range(0, len(table_identifiers)):
        table.add_row([table_identifiers[i],
                       table_display_names[i],
                       table_programs[i],
                       table_platforms[i],
                       table_instrument_types[i],
                       table_source_types[i],
                       table_owners[i]])
    click.echo(table.draw())


@sources_group.command("add", short_help="Add a data source")
@click.argument("program", type=str)
@click.argument("platform", type=str)
@click.argument("instrument_type", type=str)
@click.argument("source_type", type=click.Choice(SUPPORTED_SOURCE_TYPES))
@click.argument("display_name", type=str)
@click.option("--identifier", type=int, help="Custom identifier to use")
@click.pass_obj
def add(config, program, platform, instrument_type, source_type, display_name, identifier):
    """
    Add a data source

    \b
    PROGRAM             the program to set
    PLATFORM            the platform to set
    INSTRUMENT_TYPE     the instrument type to set
    SOURCE_TYPE         the source type to set
    DISPLAY_NAME        the display name to set

    """
    # add data source
    try:
        new_ds = pyaurorax.sources.DataSource(identifier=identifier,
                                              program=program,
                                              platform=platform,
                                              instrument_type=instrument_type,
                                              source_type=source_type,
                                              display_name=display_name)
        added_ds = pyaurorax.sources.add(new_ds)
        click.echo("Created data source successfully\n")
        click.echo(added_ds)
    except pyaurorax.AuroraXException as e:
        click.echo("%s occurred: %s" % (type(e).__name__, e.args[0]))
        sys.exit(1)
