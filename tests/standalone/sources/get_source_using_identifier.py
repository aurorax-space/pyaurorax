import aurorax
import pprint


def main():
    source = aurorax.sources.get_using_identifier(10, format="full_record")
    pprint.pprint(source)


# ----------
if (__name__ == "__main__"):
    main()
