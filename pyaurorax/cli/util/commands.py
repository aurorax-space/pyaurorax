import click
import datetime
import pyaurorax
from dateutil.parser import parse


@click.group("util", help="Utility commands")
def utility_group():
    pass


@utility_group.command("ground_to_nbtrace",
                       short_help="Convert ground location to north B-trace location")
@click.argument("lat", type=click.FloatRange(min=-90.0, max=90.0))
@click.argument("lon", type=click.FloatRange(min=-180.0, max=180.0))
@click.option("--timestamp",
              type=str,
              default=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
              show_default=True,
              help="timestamp to use when converting in ISO format "
              "(YYYY-mm-ddTHH:MM:SS), defaults to current time")
@click.pass_obj
def ground_to_nbtrace(config, lat, lon, timestamp):
    """
    Convert a geographic location (assumed to be on the ground) to a north
    B-trace location. Note that the timestamp is needed since the B-trace
    values are derived using magnetic coordinates

    \n
    Important! If you supply negative numbers, prefix it with '--' to
    tell the terminal to not evaluate dash (-) characters as options
    after it. For example, "aurorax-cli util ground_to_nbtrace -- 90.0 -120.0"

    \b
    LAT    the latitude, in geographic coordinates (-90 to 90)
    LON    the longitude, in geographic coordinates (-180 to 180)
    """
    # set location object
    input_location = pyaurorax.Location(lat=lat, lon=lon)
    click.echo("Inputted location:\t%s" % (input_location))

    # interpret time
    ts = parse(timestamp)
    click.echo("Timestamp:\t\t%s" % (ts.isoformat()))

    # get nbtrace location
    nbtrace = pyaurorax.util.ground_geo_to_nbtrace(input_location, ts)

    # output
    click.echo("\nDerived north B-trace:\t%s" % (nbtrace))


@utility_group.command("ground_to_sbtrace",
                       short_help="Convert ground location to south B-trace location")
@click.argument("lat", type=click.FloatRange(min=-90.0, max=90.0))
@click.argument("lon", type=click.FloatRange(min=-180.0, max=180.0))
@click.option("--timestamp",
              type=str,
              default=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
              show_default=True,
              help="timestamp to use when converting in ISO format "
              "(YYYY-mm-ddTHH:MM:SS), defaults to current time")
@click.pass_obj
def ground_to_sbtrace(config, lat, lon, timestamp):
    """
    Convert a geographic location (assumed to be on the ground) to a south
    B-trace location. Note that the timestamp is needed since the B-trace
    values are derived using magnetic coordinates

    \n
    Important! If you supply negative numbers, prefix it with '--' to
    tell the terminal to not evaluate dash (-) characters as options
    after it. For example, "aurorax-cli util ground_to_nbtrace -- 90.0 -120.0"

    \b
    LAT    the latitude, in geographic coordinates (-90 to 90)
    LON    the longitude, in geographic coordinates (-180 to 180)
    """
    # set location object
    input_location = pyaurorax.Location(lat=lat, lon=lon)
    click.echo("Inputted location:\t%s" % (input_location))

    # interpret time
    ts = parse(timestamp)
    click.echo("Timestamp:\t\t%s" % (ts.isoformat()))

    # get nbtrace location
    nbtrace = pyaurorax.util.ground_geo_to_sbtrace(input_location, ts)

    # output
    click.echo("\nDerived south B-trace:\t%s" % (nbtrace))
