import aurorax
import pprint


def main():
    source = aurorax.sources.get_using_filters(program="swarm", instrument_type="ssc-web", format="full_record")
    pprint.pprint(source)


# ----------
if (__name__ == "__main__"):
    main()
