import pyaurorax
import pprint


def main():
    # get data source
    source = pyaurorax.sources.get_using_filters(program="swarm",
                                                 instrument_type="footprint",
                                                 format=pyaurorax.FORMAT_FULL_RECORD)
    pprint.pprint(source)


# ----------
if (__name__ == "__main__"):
    main()
