import pyaurorax
from tabulate import tabulate


def main():
    # get sources
    sources = pyaurorax.sources.list(format=pyaurorax.FORMAT_BASIC_INFO)

    # print in a nice table
    headers = ["ID",
               "Program",
               "Platform",
               "Instrument Type",
               "Source Type",
               "Display Name"]
    rows = []
    for source in sources:
        rows.append([
            int(source.identifier),
            source.program,
            source.platform,
            source.instrument_type,
            source.source_type,
            source.display_name
        ])
    rows = sorted(rows, key=lambda i: (i[1], i[3], i[2]))
    print(tabulate(rows, headers=headers, tablefmt="presto"))


# ----------
if (__name__ == "__main__"):
    main()
