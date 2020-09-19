#! /usr/bin/env python

import aurorax
import pprint


def main():
    stats = aurorax.get_source_statistics(10)
    pprint.pprint(stats)


# ----------
if (__name__ == "__main__"):
    main()
