#! /usr/bin/env python

import aurorax
import pprint


def main():
    sources = aurorax.ephemeris.get_all_sources()
    pprint.pprint(sources)


# ----------
if (__name__ == "__main__"):
    main()