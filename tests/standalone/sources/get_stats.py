import aurorax
import pprint


def main():
    # set parameters
    program = "themis"
    platform = "themise"
    instrument_type = "ssc-web"
    print("Retrieving statistics with the parameters:")
    print("  Program:\t\t%s" % (program))
    print("  Platform:\t\t%s" % (platform))
    print("  Instrument Type:\t%s\n" % (instrument_type))

    # get idendifier
    data_source = aurorax.sources.get_using_filters(program=program,
                                                    platform=platform,
                                                    instrument_type=instrument_type)

    # get statistics
    stats = aurorax.sources.get_stats(data_source["data"][0]["identifier"])
    pprint.pprint(stats)


# ----------
if (__name__ == "__main__"):
    main()
