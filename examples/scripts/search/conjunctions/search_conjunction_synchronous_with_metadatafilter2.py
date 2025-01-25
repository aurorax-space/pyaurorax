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
    start = datetime.datetime(2008, 1, 1, 0, 0, 0)
    end = datetime.datetime(2008, 1, 31, 23, 59, 59)
    distance = 500

    # set up metadata filters
    expression_1 = aurorax.search.MetadataFilterExpression("calgary_apa_ml_v1", "classified as APA", operator="=")
    expression_2 = aurorax.search.MetadataFilterExpression("calgary_apa_ml_v1_confidence", 95, operator=">=")
    metadata_filters = aurorax.search.MetadataFilter([expression_1, expression_2], operator="and")

    # set up criteria blocks
    ground_params = [aurorax.search.GroundCriteriaBlock(programs=["themis-asi"], metadata_filters=metadata_filters)]
    space_params = [aurorax.search.SpaceCriteriaBlock(programs=["themis"], hemisphere=["northern"])]

    # perform search
    s = aurorax.search.conjunctions.search(
        start,
        end,
        distance=distance,
        ground=ground_params,
        space=space_params,
        conjunction_types=["nbtrace"],
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
