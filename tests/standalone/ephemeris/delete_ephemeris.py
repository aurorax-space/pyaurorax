#! /usr/bin/env python

import aurorax
import os
import datetime
import pprint


def main():
    # read API key from environment vars
    api_key = os.environ["AURORAX_API_KEY"]

    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument"
    start_dt = datetime.datetime(2010, 1, 1, 0, 0, 0)
    end_dt = datetime.datetime.now()

    # get the ephemeris source ID
    sources = aurorax.sources.get_using_values(program=[program],
                                               platform=[platform],
                                               instrument_type=[instrument_type])
    if (len(sources["data"]) == 0):
        instrument_type = "test-instrument-type"
        sources = aurorax.sources.get_using_values(program=[program],
                                                   platform=[platform],
                                                   instrument_type=[instrument_type])
        if (len(sources["data"]) == 0):
            print("Source not found, aborting")
            return
    identifier = sources["data"][0]["identifier"]

    # delete records
    res = aurorax.ephemeris.delete(api_key, identifier, program, platform, instrument_type, start_dt, end_dt)

    # print result
    if (res["status_code"] == 200):
        print("Successfully deleted")
    else:
        print("Failed to delete")
        pprint.pprint(res)


# ----------
if (__name__ == "__main__"):
    main()
