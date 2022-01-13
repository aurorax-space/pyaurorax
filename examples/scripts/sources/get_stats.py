import pyaurorax
import pprint


def main():
    # set parameters
    program = "themis"
    platform = "themise"
    instrument_type = "footprint"
    print("Retrieving statistics with the parameters:")
    print("  Program:\t\t%s" % (program))
    print("  Platform:\t\t%s" % (platform))
    print("  Instrument Type:\t%s\n" % (instrument_type))

    # get identifier
    data_source = pyaurorax.sources.get_using_filters(program=program,
                                                      platform=platform,
                                                      instrument_type=instrument_type)

    # get statistics
    stats = pyaurorax.sources.get_stats(data_source[0]["identifier"])
    pprint.pprint(stats)


# ----------
if (__name__ == "__main__"):
    main()
