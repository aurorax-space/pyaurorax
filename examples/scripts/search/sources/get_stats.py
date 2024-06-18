import pyaurorax
import pprint


def main():
    # set parameters
    aurorax = pyaurorax.PyAuroraX()
    program = "themis"
    platform = "themise"
    instrument_type = "footprint"

    # get identifier
    data_source = aurorax.search.sources.get(
        program=program,
        platform=platform,
        instrument_type=instrument_type,
        include_stats=True,
    )

    print()
    print(data_source)
    print()
    pprint.pprint(data_source.__dict__)
    print()


# ----------
if (__name__ == "__main__"):
    main()
