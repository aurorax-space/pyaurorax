import json
import os
import pyaurorax


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # read in json file, convert to dict
    query_dict = {}
    with open("%s/../../../queries/search/ephemeris/example1.json" % (os.path.dirname(os.path.realpath(__file__))), 'r') as fp:
        query_dict = json.load(fp)

    print()
    print(aurorax.search.ephemeris.describe(query_dict=query_dict))
    print()


# ----------
if (__name__ == "__main__"):
    main()
