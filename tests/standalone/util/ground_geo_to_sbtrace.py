import pyaurorax
import datetime


def main():
    # set timestamp
    timestamp = datetime.datetime.now()

    # set geographic lat/lon
    geo_location = pyaurorax.Location(lat=-56.0, lon=20.0)
    print("Geographic location: %s" % (geo_location))
    sbtrace = pyaurorax.util.ground_geo_to_sbtrace(geo_location, timestamp)
    print("South B-trace:       %s\n" % (sbtrace))

    # set geographic lat/lon
    geo_location = pyaurorax.Location(lat=56.0, lon=20.0)
    print("Geographic location: %s" % (geo_location))
    sbtrace = pyaurorax.util.ground_geo_to_sbtrace(geo_location, timestamp)
    print("South B-trace:       %s" % (sbtrace))


# ----------
if (__name__ == "__main__"):
    main()
