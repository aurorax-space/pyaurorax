import aurorax
import pprint


def main():
    # get statistics
    stats = aurorax.sources.get_stats(10)
    pprint.pprint(stats)


# ----------
if (__name__ == "__main__"):
    main()
