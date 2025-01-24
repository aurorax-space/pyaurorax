import json
import os
import pyaurorax


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # read in json file, convert to dict
    query_dict = {}
    with open("%s/../../../queries/search/conjunctions/example1.json" % (os.path.dirname(os.path.realpath(__file__))), 'r') as fp:
        query_dict = json.load(fp)

    print()
    print(aurorax.search.conjunctions.describe(query_dict=query_dict))
    print()


# ----------
if (__name__ == "__main__"):
    main()
