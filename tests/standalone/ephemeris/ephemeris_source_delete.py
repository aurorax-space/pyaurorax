#! /usr/bin/env python

import aurorax
import os


def main():
    # read API key from environment vars
    api_key = os.environ["AURORAX_API_KEY"]

    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"

    # get source record to pull out the identifier
    sources = aurorax.get_source_using_filters(program=program,
                                               platform=platform,
                                               instrument_type=instrument_type)
    if (len(sources["data"]) == 0):
        sources = aurorax.get_source_using_filters(program=program,
                                                   platform=platform,
                                                   instrument_type="test-instrument-type-updated")
        if (len(sources["data"]) == 0):
            print("No ephemeris source found")
            return
    identifier = sources[0]["identifier"]

    # remove source
    r = aurorax.remove_source(api_key, identifier)
    if (r["status_code"] == 200):
        print("Successfully removed source")
    else:
        print(r)


# ----------
if (__name__ == "__main__"):
    main()
