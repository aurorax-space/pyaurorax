import pyaurorax
import datetime
import pprint


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # set metadata filter
    expression1 = aurorax.search.MetadataFilterExpression("calgary_apa_ml_v1", "classified as APA", operator="=")
    expression2 = aurorax.search.MetadataFilterExpression("calgary_apa_ml_v1_confidence", 95, operator=">=")
    metadata_filter = aurorax.search.MetadataFilter(expressions=[expression1, expression2], operator="and")

    # do search
    s = aurorax.search.ephemeris.search(datetime.datetime(2008, 1, 1, 0, 0, 0),
                                        datetime.datetime(2008, 1, 9, 23, 59, 59),
                                        programs=["themis-asi"],
                                        metadata_filters=metadata_filter,
                                        verbose=True)
    print()
    pprint.pprint(s.data[0:10])
    print("...")


# ----------
if (__name__ == "__main__"):
    main()
