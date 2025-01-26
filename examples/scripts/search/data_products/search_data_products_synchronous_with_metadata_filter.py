import datetime
import pprint
import pyaurorax


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # set metadata filter
    metadata_filter = aurorax.search.MetadataFilter(expressions=[
        aurorax.search.MetadataFilterExpression("keogram_type", "hourly", operator="="),
    ])

    # do search
    s = aurorax.search.data_products.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                            datetime.datetime(2020, 1, 1, 23, 59, 59),
                                            programs=["auroramax"],
                                            metadata_filters=metadata_filter,
                                            verbose=True)
    print()
    pprint.pprint(s.data)


# ----------
if (__name__ == "__main__"):
    main()
