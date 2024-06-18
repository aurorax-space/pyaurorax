import pyaurorax
from tabulate import tabulate


def main():
    # get sources
    aurorax = pyaurorax.PyAuroraX()
    sources = aurorax.search.sources.list(format=pyaurorax.search.FORMAT_BASIC_INFO)

    # print in a nice table
    headers = ["ID", "Program", "Platform", "Instrument Type", "Source Type", "Display Name"]
    rows = []
    for source in sources:
        rows.append([
            int(source.identifier) if isinstance(source.identifier, int) else None,
            source.program,
            source.platform,
            source.instrument_type,
            source.source_type,
            source.display_name,
        ])
    rows = sorted(rows, key=lambda i: (i[1], i[3], i[2]))
    print("\n", tabulate(rows, headers=headers, tablefmt="presto"), "\n")


# ----------
if (__name__ == "__main__"):
    main()
