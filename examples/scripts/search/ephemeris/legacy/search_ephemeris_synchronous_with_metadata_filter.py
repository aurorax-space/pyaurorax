import pyaurorax
import datetime
import pprint


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # set timeframe and program values
    start = datetime.datetime(2008, 1, 1, 0, 0, 0)
    end = datetime.datetime(2008, 1, 31, 23, 59, 59)
    programs = ["themis-asi"]

    # set metadata filter
    metadata_filters_logical_operator = "AND"
    metadata_filters = [
        {
            "key": "calgary_apa_ml_v1",
            "operator": "in",
            "values": [
                "classified as APA"  # only find records that were classified as APA
            ]
        },
        {
            "key": "calgary_apa_ml_v1_confidence",
            "operator": ">=",
            "values": [
                "95"  # with a confidence of at least 95%
            ]
        }
    ]

    # perform the search
    s = aurorax.search.ephemeris.search(start=start,
                                        end=end,
                                        programs=programs,
                                        metadata_filters_logical_operator=metadata_filters_logical_operator,
                                        metadata_filters=metadata_filters,
                                        verbose=True)

    print()
    pprint.pprint(s.data[0:10])
    print("...")


# ----------
if (__name__ == "__main__"):
    main()
