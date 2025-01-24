import pprint
import datetime
import pyaurorax


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # set up params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 2, 28, 23, 59, 59)
    distance = 200
    ground_params = [aurorax.search.GroundCriteriaBlock(programs=["themis-asi"])]
    space_params = [aurorax.search.SpaceCriteriaBlock(programs=["swarm"])]
    events_params = [aurorax.search.EventCriteriaBlock()]

    # perform search
    s = aurorax.search.conjunctions.search(
        start,
        end,
        ground=ground_params,
        space=space_params,
        distance=distance,
        events=events_params,
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
