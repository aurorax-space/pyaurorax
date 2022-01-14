import pyaurorax
import pprint


def main():
    # set parameters
    program = "themis-asi"
    platform = "gillam"
    instrument_type = "panchromatic ASI"
    print("Retrieving data products metadata schema with the parameters:")
    print("  Program:\t\t%s" % (program))
    print("  Platform:\t\t%s" % (platform))
    print("  Instrument Type:\t%s\n" % (instrument_type))

    # get idendifier
    data_source = pyaurorax.sources.get_using_filters(program=program,
                                                      platform=platform,
                                                      instrument_type=instrument_type)

    # get schema
    schema = pyaurorax.metadata.get_data_products_schema(data_source[0].identifier)
    pprint.pprint(schema)


# ----------
if (__name__ == "__main__"):
    main()
