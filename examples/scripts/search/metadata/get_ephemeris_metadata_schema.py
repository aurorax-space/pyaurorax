import pyaurorax
import pprint


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # set parameters
    program = "swarm"
    platform = "swarma"
    instrument_type = "footprint"
    print("Retrieving ephemeris metadata schema with the parameters:")
    print("  Program:\t\t%s" % (program))
    print("  Platform:\t\t%s" % (platform))
    print("  Instrument Type:\t%s\n" % (instrument_type))

    # get identifier
    ds = aurorax.search.sources.get(program, platform, instrument_type)

    # get schema
    if (ds.identifier is None):
        print("Unable to find data source")
        return 1
    schema = aurorax.search.metadata.get_ephemeris_schema(ds.identifier)
    pprint.pprint(schema)


# ----------
if (__name__ == "__main__"):
    main()
