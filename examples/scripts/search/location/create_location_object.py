import pyaurorax


def main():
    loc = pyaurorax.search.Location(lat=51.0447, lon=-114.0719)
    print(loc)


# ----------
if (__name__ == "__main__"):
    main()
