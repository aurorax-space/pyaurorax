import aurorax
import pprint


def main():
    # get data source
    source = aurorax.sources.get("swarm", "swarma", "footprint", format="full_record")
    pprint.pprint(source)


# ----------
if (__name__ == "__main__"):
    main()
