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
    events_params = [{"programs": ["events"]}]
    distance = 200

    # create search object
    s = pyaurorax.search.ConjunctionSearch(
        aurorax,
        start,
        end,
        ground=ground_params,
        space=space_params,
        events=events_params,
        distance=distance,
    )

    print()
    print(s)
    print()


# ----------
if (__name__ == "__main__"):
    main()
