import pyaurorax
import datetime


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # set timestamp
    timestamp = datetime.datetime.now()

    # set geographic lat/lon
    geo_location = pyaurorax.search.Location(lat=56.0, lon=20.0)
    print("\nGeographic location: %s" % (geo_location))
    nbtrace = aurorax.search.util.ground_geo_to_nbtrace(geo_location, timestamp)
    print("North B-trace:       %s\n" % (nbtrace))

    # set geographic lat/lon
    geo_location = pyaurorax.search.Location(lat=-56.0, lon=20.0)
    print("Geographic location: %s" % (geo_location))
    nbtrace = aurorax.search.util.ground_geo_to_nbtrace(geo_location, timestamp)
    print("North B-trace:       %s\n" % (nbtrace))


# ----------
if (__name__ == "__main__"):
    main()
