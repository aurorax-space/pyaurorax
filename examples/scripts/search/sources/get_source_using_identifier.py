import pyaurorax


def main():
    # get data source
    aurorax = pyaurorax.PyAuroraX()
    ds = aurorax.search.sources.get_using_identifier(30, format=pyaurorax.search.FORMAT_FULL_RECORD, include_stats=True)
    import pprint
    pprint.pprint(ds.__dict__)


# ----------
if (__name__ == "__main__"):
    main()
