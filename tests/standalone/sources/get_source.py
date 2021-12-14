import pyaurorax
import pprint


def main():
    # get data source
    source = pyaurorax.sources.get(
        "swarm", "swarma", "footprint", format="full_record")
    pprint.pprint(source)


# ----------
if (__name__ == "__main__"):
    main()
