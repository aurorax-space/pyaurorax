import pyaurorax


def main():
    # get data source
    aurorax = pyaurorax.PyAuroraX()
    ds = aurorax.search.sources.get_using_filters(program="swarm", instrument_type="footprint", format=pyaurorax.search.FORMAT_FULL_RECORD)
    print(ds)


# ----------
if (__name__ == "__main__"):
    main()
