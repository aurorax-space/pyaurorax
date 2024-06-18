import datetime
import pyaurorax


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # set parameters
    start_date = datetime.datetime(2020, 1, 1)
    end_date = datetime.date(2020, 1, 10)
    program = "trex"
    platform = "gillam"
    instrument_type = "RGB ASI"
    print("\nRetrieving data products availability with the parameters:")
    print("  Start Date:\t\t%s" % (start_date.strftime("%Y-%m-%d")))
    print("  End Date:\t\t%s" % (end_date.strftime("%Y-%m-%d")))
    print("  Program:\t\t%s" % (program))
    print("  Platform:\t\t%s" % (platform))
    print("  Instrument Type:\t%s\n" % (instrument_type))

    # get availability
    availability = aurorax.search.availability.data_products(start_date,
                                                             end_date,
                                                             program=program,
                                                             platform=platform,
                                                             instrument_type=instrument_type,
                                                             format=pyaurorax.search.FORMAT_IDENTIFIER_ONLY)
    print(availability)
    print()


# ----------
if (__name__ == "__main__"):
    main()
