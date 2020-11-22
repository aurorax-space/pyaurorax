import aurorax
import pprint


def main():
    # create location object
    loc = aurorax.Location(51.0447, -114.0719)

    # print
    print("__str__:\n----------")
    print(loc)
    print()
    print("__repr__:\n----------")
    pprint.pprint(loc)


# ----------
if (__name__ == "__main__"):
    main()
