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
    source_type = "ground"

    # make request
    r = aurorax.add_source(api_key, program, platform, instrument_type, source_type)

    # output results
    if (r["status_code"] == 200):
        print("Successfully added source\n")
    else:
        print("Error adding source\n")
    pprint.pprint(r)


# ----------
if (__name__ == "__main__"):
    main()
