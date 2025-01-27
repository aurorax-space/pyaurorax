import datetime
import pyaurorax
import pprint


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # set query string
    #
    # pulled this directly from the More->About query modal, using the
    # copy-to-clipboard icon
    #
    # if there are issues in the dict (ie. if there's a distance as 'null'), then
    # put triple quotes around the query and pass it into the function as a string
    query = {
        "start": "2019-01-01T00:00:00.000Z",
        "end": "2019-01-03T23:59:59.000Z",
        "conjunction_types": ["nbtrace"],
        "ground": [{
            "programs": ["themis-asi"],
            "platforms": ["fort smith", "gillam"],
            "instrument_types": ["panchromatic ASI"],
            "ephemeris_metadata_filters": {}
        }],
        "space": [{
            "programs": ["swarm"],
            "platforms": [],
            "instrument_types": ["footprint"],
            "ephemeris_metadata_filters": {},
            "hemisphere": ["northern"]
        }],
        "events": [],
        "max_distances": {
            "ground1-space1": 500
        }
    }

    # do search
    s = aurorax.search.conjunctions.search_from_raw_query(query, verbose=True)

    # print data
    print()
    pprint.pprint(s.data)
    print()

    pprint.pprint(s.__dict__)


# ----------
if (__name__ == "__main__"):
    main()
