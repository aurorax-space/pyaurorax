import pyaurorax
import pprint


def main():
    # create location object
    loc = pyaurorax.Location(lat=51.0447, lon=-114.0719)

    # print
    print("__str__:\n----------")
    print(loc)
    print()
    print("__repr__:\n----------")
    pprint.pprint(loc)


# ----------
if (__name__ == "__main__"):
    main()
