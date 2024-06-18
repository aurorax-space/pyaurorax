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
import pprint
import click
import humanize
import pyaurorax
import textwrap
from texttable import Texttable

# globals
SUPPORTED_SOURCE_TYPES = [
    pyaurorax.search.SOURCE_TYPE_EVENT_LIST,
    pyaurorax.search.SOURCE_TYPE_GROUND,
    pyaurorax.search.SOURCE_TYPE_HEO,
    pyaurorax.search.SOURCE_TYPE_LEO,
    pyaurorax.search.SOURCE_TYPE_LUNAR,
]
ALLOWED_FORMATS = [
    pyaurorax.search.FORMAT_BASIC_INFO,
    pyaurorax.search.FORMAT_BASIC_INFO_WITH_METADATA,
    pyaurorax.search.FORMAT_IDENTIFIER_ONLY,
    pyaurorax.search.FORMAT_FULL_RECORD,
]


def __print_stats(stats):
    if (stats.ephemeris_count == 0):
        click.echo("Ephemeris Stats:\t0 records")
    else:
        click.echo("Ephemeris Stats:\t%s (%s to %s)" % (
            humanize.intcomma(stats.ephemeris_count),
            stats.earliest_ephemeris_loaded.strftime("%Y-%m-%dT%H:%M"),
            stats.latest_ephemeris_loaded.strftime("%Y-%m-%dT%H:%M"),
        ))
    if (stats.data_product_count == 0):
        click.echo("Data Product Stats:\t0 records")
    else:
        click.echo("Data Product Stats:\t%s (%s to %s)" % (
            humanize.intcomma(stats.data_product_count),
            stats.earliest_data_product_loaded.strftime("%Y-%m-%dT%H:%M"),
            stats.latest_data_product_loaded.strftime("%Y-%m-%dT%H:%M"),
        ))


def __print_metadata_schema_table(ephemeris_schema=[], data_product_schema=[]):
    # init
    wrap_threshold = 40

    # set table lists
    table_schemas = []
    table_allowed_values = []
    table_data_types = []
    table_descriptions = []
    table_additional_descriptions = []
    table_field_names = []
    table_searchable = []
    for item in ephemeris_schema:
        table_schemas.append("ephemeris")
        table_field_names.append(item["field_name"])
        table_data_types.append(item["data_type"])
        table_allowed_values.append('\n'.join(textwrap.wrap(str(item["allowed_values"]), wrap_threshold)))
        table_descriptions.append('\n'.join(textwrap.wrap(item["description"], wrap_threshold)))
        if ("additional_description" in item):
            table_additional_descriptions.append('\n'.join(textwrap.wrap(item["additional_description"], wrap_threshold)))
        else:
            table_additional_descriptions.append("-")
        if ("searchable" in item):
            table_searchable.append(item["searchable"])
        else:
            table_searchable.append("-")
    for item in data_product_schema:
        table_schemas.append("data_product")
        table_field_names.append(item["field_name"])
        table_data_types.append(item["data_type"])
        table_allowed_values.append('\n'.join(textwrap.wrap(str(item["allowed_values"]), wrap_threshold)))
        table_descriptions.append('\n'.join(textwrap.wrap(item["description"], wrap_threshold)))
        if ("additional_description" in item):
            table_additional_descriptions.append('\n'.join(textwrap.wrap(item["additional_description"], wrap_threshold)))
        else:
            table_additional_descriptions.append("-")
        if ("searchable" in item):
            table_searchable.append(item["searchable"])
        else:
            table_searchable.append("-")

    # set header values
    table_headers = ["Schema", "Field Name", "Data Type", "Allowed Values", "Searchable", "Description", "Additional Description"]

    # output information
    table = Texttable(max_width=400)
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(["t"] * len(table_headers))
    table.set_header_align(["l"] * len(table_headers))
    table.set_cols_align(["l"] * len(table_headers))
    table.header(table_headers)
    for i in range(0, len(table_field_names)):
        table.add_row([
            table_schemas[i], table_field_names[i], table_data_types[i], table_allowed_values[i], table_searchable[i], table_descriptions[i],
            table_additional_descriptions[i]
        ])
    click.echo(table.draw())


def __print_single_data_source(ds, format, include_stats):
    if (format == pyaurorax.search.FORMAT_IDENTIFIER_ONLY):
        click.echo("Identifier:\t\t%d" % (ds.identifier))
        if (include_stats is True):
            __print_stats(ds.stats)
    elif (format == pyaurorax.search.FORMAT_BASIC_INFO):
        click.echo("Identifier:\t\t%d" % (ds.identifier))
        click.echo("Program:\t\t%s" % (ds.program))
        click.echo("Platform:\t\t%s" % (ds.platform))
        click.echo("Instument Type:\t\t%s" % (ds.instrument_type))
        click.echo("Source Type:\t\t%s" % (ds.source_type))
        click.echo("Display Name:\t\t%s" % (ds.display_name))
        if (include_stats is True):
            __print_stats(ds.stats)
    elif (format == pyaurorax.search.FORMAT_BASIC_INFO_WITH_METADATA):
        click.echo("Identifier:\t\t%d" % (ds.identifier))
        click.echo("Program:\t\t%s" % (ds.program))
        click.echo("Platform:\t\t%s" % (ds.platform))
        click.echo("Instument Type:\t\t%s" % (ds.instrument_type))
        click.echo("Source Type:\t\t%s" % (ds.source_type))
        click.echo("Display Name:\t\t%s" % (ds.display_name))
        if (ds.metadata == {}):
            click.echo("Metadata:\t\t%s" % (ds.metadata))
        else:
            click.echo("Metadata:\n%s" % (pprint.pformat(ds.metadata)))
        if (include_stats is True):
            __print_stats(ds.stats)
    elif (format == pyaurorax.search.FORMAT_FULL_RECORD):
        click.echo("Identifier:\t\t%d" % (ds.identifier))
        click.echo("Program:\t\t%s" % (ds.program))
        click.echo("Platform:\t\t%s" % (ds.platform))
        click.echo("Instument Type:\t\t%s" % (ds.instrument_type))
        click.echo("Source Type:\t\t%s" % (ds.source_type))
        click.echo("Display Name:\t\t%s" % (ds.display_name))
        click.echo("Owner:\t\t\t%s" % (ds.owner))
        click.echo("Maintainers:\t\t%s" % (ds.maintainers))
        if (ds.metadata == {}):
            click.echo("Metadata:\t\t%s" % (ds.metadata))
        else:
            click.echo("Metadata:\n%s" % (pprint.pformat(ds.metadata)))
        if (include_stats is True):
            __print_stats(ds.stats)
        if (ds.ephemeris_metadata_schema == []):
            click.echo("Ephemeris Schema:\t[]")
        else:
            click.echo("Ephemeris Schema:\tsee below table")
        if (ds.data_product_metadata_schema == []):
            click.echo("Data Product Schema:\t[]\n")
        else:
            click.echo("Data Product Schema:\tsee below table\n")
        __print_metadata_schema_table(ephemeris_schema=ds.ephemeris_metadata_schema, data_product_schema=ds.data_product_metadata_schema)


def __print_sources_table(sources, order, show_owner, include_stats):
    # set table lists
    table_identifiers = []
    table_programs = []
    table_platforms = []
    table_instrument_types = []
    table_source_types = []
    table_display_names = []
    table_owners = []
    table_stats_ephemeris = []
    table_stats_data_products = []
    sum_ephemeris_count = 0
    sum_data_product_count = 0
    for source in sources:
        table_identifiers.append(source.identifier)
        table_programs.append(source.program)
        table_platforms.append(source.platform)
        table_instrument_types.append(source.instrument_type)
        table_source_types.append(source.source_type)
        table_display_names.append(source.display_name)
        table_owners.append(source.owner)
        if (source.stats is not None):
            if (source.stats.earliest_ephemeris_loaded is not None and source.stats.latest_ephemeris_loaded is not None):
                table_stats_ephemeris.append(
                    "%s records (%s to %s)" %
                    (humanize.intcomma(source.stats.ephemeris_count), source.stats.earliest_ephemeris_loaded.strftime("%Y-%m-%dT%H:%M"),
                     source.stats.latest_ephemeris_loaded.strftime("%Y-%m-%dT%H:%M")))
                sum_ephemeris_count += source.stats.ephemeris_count
            else:
                table_stats_ephemeris.append("%s records" % (humanize.intcomma(source.stats.ephemeris_count)))
            if (source.stats.earliest_data_product_loaded is not None and source.stats.latest_data_product_loaded is not None):
                table_stats_data_products.append(
                    "%s records (%s to %s)" %
                    (humanize.intcomma(source.stats.data_product_count), source.stats.earliest_data_product_loaded.strftime("%Y-%m-%dT%H:%M"),
                     source.stats.latest_data_product_loaded.strftime("%Y-%m-%dT%H:%M")))
                sum_data_product_count += source.stats.data_product_count
            else:
                table_stats_data_products.append("%s records" % (humanize.intcomma(source.stats.data_product_count)))
        else:
            table_stats_ephemeris.append("-")
            table_stats_data_products.append("-")

    # set header values
    table_headers = ["Identifier", "Display Name", "Program", "Platform", "Instrument Type", "Source Type"]
    if (show_owner is True):
        table_headers.append("Owner")
    if (include_stats is True):
        table_headers.append("Ephemeris stats")
        table_headers.append("Data Products stats")
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
        if (show_owner is True and include_stats is True):
            table.add_row([
                table_identifiers[i], table_display_names[i], table_programs[i], table_platforms[i], table_instrument_types[i], table_source_types[i],
                table_owners[i], table_stats_ephemeris[i], table_stats_data_products[i]
            ])
        elif (show_owner is True):
            table.add_row([
                table_identifiers[i], table_display_names[i], table_programs[i], table_platforms[i], table_instrument_types[i], table_source_types[i],
                table_owners[i]
            ])
        elif (include_stats is True):
            table.add_row([
                table_identifiers[i], table_display_names[i], table_programs[i], table_platforms[i], table_instrument_types[i], table_source_types[i],
                table_stats_ephemeris[i], table_stats_data_products[i]
            ])
        else:
            table.add_row([
                table_identifiers[i], table_display_names[i], table_programs[i], table_platforms[i], table_instrument_types[i], table_source_types[i]
            ])
    click.echo(table.draw())

    # show stats sums
    if (include_stats is True):
        print("\nTotal Ephemeris records:\t%s" % (humanize.intcomma(sum_ephemeris_count)))
        print("Total Data Product records:\t%s\n" % (humanize.intcomma(sum_data_product_count)))


@click.group("sources", help="Interact with data sources")
def sources_group():
    pass


@sources_group.command("list", short_help="List data sources")
@click.option("--program", type=str, help="Filter using program")
@click.option("--platform", type=str, help="Filter using platform")
@click.option("--instrument-type", type=str, help="Filter using instrument type")
@click.option("--source-type", type=click.Choice(SUPPORTED_SOURCE_TYPES), help="Filter using source type")
@click.option("--owner", type=str, help="Filter using an owner")
@click.option("--order",
              type=click.Choice(["identifier", "program", "platform", "instrument_type", "display_name", "owner"]),
              default="identifier",
              show_default=True,
              help="Order results using a certain column")
@click.option("--include-stats", is_flag=True, help="Include additional information about data sources")
@click.option("--reversed", "reversed_", is_flag=True, help="Reverse ordering")
@click.pass_obj
def list(config, program, platform, instrument_type, source_type, owner, order, include_stats, reversed_):
    """
    List data sources using the options to filter as desired
    """
    # get data sources
    try:
        sources = config.aurorax.search.sources.get_using_filters(program=program,
                                                                  platform=platform,
                                                                  instrument_type=instrument_type,
                                                                  source_type=source_type,
                                                                  owner=owner,
                                                                  order=order,
                                                                  include_stats=include_stats)
    except pyaurorax.AuroraXError as e:
        click.echo("%s occurred: %s" % (type(e).__name__, e.args[0]))
        sys.exit(1)

    # reverse
    if (reversed_ is True):
        sources = reversed(sources)

    # decide if we want to show the owner
    show_owner = False
    if (owner is not None or order == "owner"):
        show_owner = True

    # print the table
    __print_sources_table(sources, order, show_owner, include_stats)


@sources_group.command("search", short_help="Search for data sources")
@click.option("--programs", type=str, help="Search for program (comma separate for multiple values)")
@click.option("--platforms", type=str, help="Search for platform (comma separate for multiple values)")
@click.option("--instrument-types", type=str, help="Search for instrument type (comma separate for multiple values)")
@click.option("--order",
              type=click.Choice(["identifier", "program", "platform", "instrument_type", "display_name", "owner"]),
              default="identifier",
              show_default=True,
              help="Order results using a certain column")
@click.option("--include-stats", is_flag=True, help="Include additional information about data sources")
@click.option("--reversed", "reversed_", is_flag=True, help="Reverse ordering")
@click.pass_obj
def search(config, programs, platforms, instrument_types, order, include_stats, reversed_):
    """
    Search for data sources using the options to filter as desired. Unlike
    the 'list' command filters, this command supports multiple programs,
    platforms, or instrument types (using commas).
    """
    # set programs values
    parsed_programs = []
    if (programs is None):
        pass
    elif (',' in programs):
        for p in programs.split(','):
            p = p.strip()
            if (len(p) > 0):
                parsed_programs.append(p)
    else:
        parsed_programs = [programs]

    # set platforms values
    parsed_platforms = []
    if (platforms is None):
        pass
    elif (',' in platforms):
        for p in platforms.split(','):
            p = p.strip()
            if (len(p) > 0):
                parsed_platforms.append(p)
    else:
        parsed_platforms = [platforms]

    # set instrument_types values
    parsed_instrument_types = []
    if (instrument_types is None):
        pass
    elif (',' in instrument_types):
        for p in instrument_types.split(','):
            p = p.strip()
            if (len(p) > 0):
                parsed_instrument_types.append(p)
    else:
        parsed_instrument_types = [instrument_types]

    # search for data sources
    try:
        sources = config.aurorax.search.sources.search(programs=parsed_programs,
                                                       platforms=parsed_platforms,
                                                       instrument_types=parsed_instrument_types,
                                                       order=order,
                                                       include_stats=include_stats)
    except pyaurorax.AuroraXError as e:
        click.echo("%s occurred: %s" % (type(e).__name__, e.args[0]))
        sys.exit(1)

    # reverse
    if (reversed_ is True):
        sources = reversed(sources)

    # decide if we want to show the owner
    show_owner = False
    if (order == "owner"):
        show_owner = True

    # print the table
    __print_sources_table(sources, order, show_owner, include_stats)


@sources_group.command("get", short_help="Get a single data source")
@click.argument("program", type=str)
@click.argument("platform", type=str)
@click.argument("instrument_type", type=str)
@click.option("--format",
              type=click.Choice(ALLOWED_FORMATS),
              default=pyaurorax.search.FORMAT_BASIC_INFO,
              help="Amount of data about the data source to retrieve")
@click.option("--include-stats", is_flag=True, help="Include additional information about data sources")
@click.pass_obj
def get(config, program, platform, instrument_type, format, include_stats):
    """
    Get a single data source record

    \b
    PROGRAM           the program value
    PLATFORM          the platform value
    INSTRUMENT_TYPE   the instrument type value
    """
    # get the data source
    try:
        ds = config.aurorax.search.sources.get(program=program,
                                               platform=platform,
                                               instrument_type=instrument_type,
                                               format=format,
                                               include_stats=include_stats)
    except pyaurorax.AuroraXError as e:
        click.echo("%s occurred: %s" % (type(e).__name__, e.args[0]))
        sys.exit(1)

    # print it out nicely
    __print_single_data_source(ds, format, include_stats)


@sources_group.command("get_using_identifier", short_help="Get a single data source (using an identifier)")
@click.argument("identifier", type=int)
@click.option("--format",
              type=click.Choice(ALLOWED_FORMATS),
              default=pyaurorax.search.FORMAT_BASIC_INFO,
              help="Amount of data about the data source to retrieve")
@click.option("--include-stats", is_flag=True, help="Include additional information about data sources")
@click.pass_obj
def get_using_identifier(config, identifier, format, include_stats):
    """
    Get a single data source record using an identifier

    \b
    IDENTIFIER     the identifier of the data source
    """
    # get data source
    try:
        ds = config.aurorax.search.sources.get_using_identifier(identifier, format=format, include_stats=include_stats)
    except pyaurorax.AuroraXError as e:
        click.echo("%s occurred: %s" % (type(e).__name__, e.args[0]))
        sys.exit(1)

    # print it out nicely
    __print_single_data_source(ds, format, include_stats=include_stats)


@sources_group.command("get_stats", short_help="Get statistics about a data source")
@click.argument("identifier", type=int)
@click.pass_obj
def get_stats(config, identifier):
    """
    Get statistics about a data source

    \b
    IDENTIFIER     the identifier of the data source
    """
    # get stats information
    try:
        ds = config.aurorax.search.sources.get_stats(identifier)
    except pyaurorax.AuroraXError as e:
        click.echo("%s occurred: %s" % (type(e).__name__, e.args[0]))
        sys.exit(1)

    # print it out nicely
    __print_single_data_source(ds, format=pyaurorax.search.FORMAT_BASIC_INFO, include_stats=True)


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
    PROGRAM           the program to set
    PLATFORM          the platform to set
    INSTRUMENT_TYPE   the instrument type to set
    SOURCE_TYPE       the source type to set
    DISPLAY_NAME      the display name to set
    """
    try:
        new_ds = config.aurorax.search.sources.DataSource(identifier=identifier,
                                                          program=program,
                                                          platform=platform,
                                                          instrument_type=instrument_type,
                                                          source_type=source_type,
                                                          display_name=display_name)
        added_ds = config.aurorax.search.sources.add(new_ds)
        click.echo("Created data source successfully\n")
        click.echo(added_ds)
    except pyaurorax.AuroraXError as e:
        click.echo("%s occurred: %s" % (type(e).__name__, e.args[0]))
        sys.exit(1)


@sources_group.command("update", short_help="Update a data source")
@click.argument("identifier", type=str)
@click.option("--program", type=str, help="New program value")
@click.option("--platform", type=str, help="New platform value")
@click.option("--instrument-type", type=str, help="New instrument type value")
@click.option("--source-type", type=click.Choice(SUPPORTED_SOURCE_TYPES), help="New source type value")
@click.option("--display-name", type=str, help="New display name value")
@click.pass_obj
def update(config, identifier, program, platform, instrument_type, source_type, display_name):
    """
    Update a data source

    \b
    IDENTIFIER     the identifier of the data source
    """
    try:
        ds = config.aurorax.search.sources.update_partial(identifier,
                                                          program=program,
                                                          platform=platform,
                                                          instrument_type=instrument_type,
                                                          source_type=source_type,
                                                          display_name=display_name)
        click.echo("Updated data source successfully\n")
        click.echo(ds)
    except pyaurorax.AuroraXError as e:
        click.echo("%s occurred: %s" % (type(e).__name__, e.args[0]))
        sys.exit(1)


@sources_group.command("delete", short_help="Delete a data source")
@click.argument("identifier", type=int)
@click.pass_obj
def delete(config, identifier):
    """
    Delete a data source

    \b
    IDENTIFIER     the identifier of the data source
    """
    try:
        config.aurorax.search.sources.delete(identifier)
        click.echo("Successfully deleted data source #%d" % (identifier))
    except pyaurorax.AuroraXError as e:
        click.echo("%s occurred: %s" % (type(e).__name__, e.args[0]))
        sys.exit(1)
