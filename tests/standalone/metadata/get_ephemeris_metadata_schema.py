import aurorax
import pprint


def main():
    # create object
    schema = aurorax.metadata.get_ephemeris_schema(3)

    # print
    pprint.pprint(schema)


# ----------
if (__name__ == "__main__"):
    main()
