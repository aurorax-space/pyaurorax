#! /usr/bin/env python

import aurorax
import pprint
import os


def main():
    # read API key from environment vars
    api_key = os.environ["AURORAX_API_KEY"]

    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"

    # get source record to pull out the identifier
    sources = aurorax.ephemeris.get_source_using_filters(program=program,
                                                         platform=platform,
                                                         instrument_type=instrument_type)
    if (len(sources) == 0):
        print("No ephemeris source found")
        return
    identifier = sources[0]["identifier"]

    # update source
    r = aurorax.ephemeris.update_source(api_key, identifier, instrument_type="test-instrument-type-updated")
    if (r.status_code == 200):
        print("Successfully updated source\n")
        pprint.pprint(r.data)
    else:
        print(r)


# ----------
if (__name__ == "__main__"):
    main()
