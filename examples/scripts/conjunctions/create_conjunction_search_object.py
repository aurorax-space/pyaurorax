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
    events_params = [
        {"programs": ["events"]}
    ]
    distance = 200

    # create search object
    s = pyaurorax.conjunctions.Search(start,
                                      end,
                                      ground=ground_params,
                                      space=space_params,
                                      events=events_params,
                                      distance=distance)
    print(s)


# ----------
if (__name__ == "__main__"):
    main()
