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
    s = aurorax.search.conjunctions.search(
        start,
        end,
        ground=ground_params,
        space=space_params,
        distance=distance,
        verbose=True,
    )

    # print the Swarm-Aurora URL
    url = aurorax.search.conjunctions.swarmaurora.get_url(s)
    print("\nSwarm-Aurora URL: %s" % (url))


# ----------
if (__name__ == "__main__"):
    main()
