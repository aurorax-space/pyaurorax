import pyaurorax


def main():
    # get data source
    aurorax = pyaurorax.PyAuroraX()
    ds = aurorax.search.sources.get("swarm", "swarma", "footprint", format=pyaurorax.search.FORMAT_BASIC_INFO)
    print(ds)


# ----------
if (__name__ == "__main__"):
    main()
