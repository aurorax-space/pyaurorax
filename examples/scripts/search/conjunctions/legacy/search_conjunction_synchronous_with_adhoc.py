import pprint
import datetime
import pyaurorax


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # set up params
    start = datetime.datetime(2021, 1, 1, 0, 0, 0)
    end = datetime.datetime(2021, 1, 3, 23, 59, 59)
    distance = 400
    space_params = [{"programs": ["swarm"], "hemisphere": ["northern"]}]
    custom_params = [{"locations": [{"lat": 51.05, "lon": -114.07}]}]

    # perform search
    s = aurorax.search.conjunctions.search(
        start,
        end,
        space=space_params,
        custom_locations=custom_params,
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
