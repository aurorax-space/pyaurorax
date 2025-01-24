import datetime
import pyaurorax


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # set up params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 6, 59, 59)
    distance = 200
    ground_params = [aurorax.search.GroundCriteriaBlock(programs=["themis-asi"])]
    space_params = [aurorax.search.SpaceCriteriaBlock(programs=["swarm"])]

    # create search object
    s = pyaurorax.search.ConjunctionSearch(
        aurorax,
        start,
        end,
        ground=ground_params,
        space=space_params,
        distance=distance,
    )

    print()
    print(aurorax.search.conjunctions.describe(search_obj=s))
    print()


# ----------
if (__name__ == "__main__"):
    main()
