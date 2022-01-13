import pyaurorax


def main():
    # get data source
    ds = pyaurorax.sources.get_using_filters(program="swarm",
                                             instrument_type="footprint",
                                             format=pyaurorax.FORMAT_FULL_RECORD)
    print(ds)


# ----------
if (__name__ == "__main__"):
    main()
