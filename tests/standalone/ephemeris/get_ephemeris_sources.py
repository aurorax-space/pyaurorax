#! /usr/bin/env python

import aurorax
from tabulate import tabulate


def main():
    # get sources
    sources = aurorax.get_all_sources()

    # print in a nice table
    headers = ["ID", "Program", "Platform", "Instrument Type", "Source Type"]
    rows = []
    for source in sources["data"]:
        rows.append([
            int(source["identifier"]),
            source["program"],
            source["platform"],
            source["instrument_type"],
            source["source_type"],
        ])
    rows = sorted(rows, key=lambda i: (i[1], i[3], i[2]))
    print(tabulate(rows, headers=headers, tablefmt="presto"))


# ----------
if (__name__ == "__main__"):
    main()
