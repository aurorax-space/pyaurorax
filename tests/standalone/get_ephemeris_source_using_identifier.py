#! /usr/bin/env python

import aurorax
import pprint


def main():
    source = aurorax.ephemeris.get_source_using_identifier(10)
    pprint.pprint(source)


# ----------
if (__name__ == "__main__"):
    main()
