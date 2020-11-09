import aurorax
import pprint


def main():
    # create object
    loc = aurorax.Location(51.049999, -114.066666)

    # print
    print("__str__:\n----------")
    print(loc)
    print()
    print("__repr__:\n----------")
    pprint.pprint(loc)


# ----------
if (__name__ == "__main__"):
    main()
