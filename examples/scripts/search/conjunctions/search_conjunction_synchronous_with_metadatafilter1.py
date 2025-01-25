import pprint
import datetime
import pyaurorax


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # search for conjunctions between Swarm A or Swarm B, and any THEMIS
    # spacecraft with the south B-trace region matching 'south polar cap'
    #
    # set up timeframe and distance
    start = datetime.datetime(2019, 2, 1, 0, 0, 0)
    end = datetime.datetime(2019, 2, 10, 23, 59, 59)
    distance = 500

    # set up metadata filters
    expression_1 = aurorax.search.MetadataFilterExpression("nbtrace_region", "north polar cap", operator="=")
    metadata_filters = aurorax.search.MetadataFilter([expression_1])

    # set up criteria blocks
    ground_params = [aurorax.search.GroundCriteriaBlock(programs=["themis-asi", "rego"])]
    space_params = [aurorax.search.SpaceCriteriaBlock(programs=["swarm"], metadata_filters=metadata_filters)]

    # perform search
    s = aurorax.search.conjunctions.search(
        start,
        end,
        distance=distance,
        ground=ground_params,
        space=space_params,
        verbose=True,
    )

    # print data
    print()
    pprint.pprint(s.data)
    print()

    pprint.pprint(s.__dict__)


# ----------
if (__name__ == "__main__"):
    main()
