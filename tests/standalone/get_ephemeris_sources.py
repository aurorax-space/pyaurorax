#! /usr/bin/env python

import aurorax


def main():
    sources = aurorax.ephemeris.get_sources()
    print(sources)


# ----------
if (__name__ == "__main__"):
    main()
