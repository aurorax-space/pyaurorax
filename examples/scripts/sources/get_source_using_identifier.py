import pyaurorax


def main():
    # get data source
    ds = pyaurorax.sources.get_using_identifier(10, format=pyaurorax.FORMAT_FULL_RECORD)
    print(ds)


# ----------
if (__name__ == "__main__"):
    main()
