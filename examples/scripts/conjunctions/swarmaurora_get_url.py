import pyaurorax
import datetime


def main():
    # set up params
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 6, 59, 59)
    ground_params = [
        {"programs": ["themis-asi"]}
    ]
    space_params = [
        {"programs": ["swarm"]}
    ]
    distance = 200

    # create search object
    s = pyaurorax.conjunctions.search(start,
                                      end,
                                      ground=ground_params,
                                      space=space_params,
                                      distance=distance,
                                      verbose=True)

    # print the Swarm-Aurora URL
    url = pyaurorax.conjunctions.swarmaurora.get_url(s)
    print("\nSwarm-Aurora URL: %s" % (url))


# ----------
if (__name__ == "__main__"):
    main()
