import datetime
import time
import pprint
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
        return_immediately=True,
    )
    print(s)

    # get status
    print("Getting request status ...")
    s.update_status()
    pprint.pprint(s.status)
    print("----------------------------\n")

    # if the request isn't done, wait continuously
    print("Waiting for request to complete ...")
    while (s.completed is False):
        time.sleep(1)
        s.update_status()

    # print status
    pprint.pprint(s)


# ----------
if (__name__ == "__main__"):
    main()
