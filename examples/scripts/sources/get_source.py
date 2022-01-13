import pyaurorax


def main():
    # get data source
    ds = pyaurorax.sources.get("swarm",
                               "swarma",
                               "footprint",
                               format=pyaurorax.FORMAT_BASIC_INFO)
    print(ds)


# ----------
if (__name__ == "__main__"):
    main()
