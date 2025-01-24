import pprint
import datetime
import pyaurorax


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # set up params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 6, 59, 59)
    ground_params = [{"programs": ["themis-asi"]}]
    space_params = [{"programs": ["swarm"]}]
    distance = 200

    # perform search
    s = aurorax.search.conjunctions.search(
        start,
        end,
        ground=ground_params,
        space=space_params,
        distance=distance,
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
