import pyaurorax


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # get schema
    ds = aurorax.search.sources.get("swarm", "swarma", "footprint")
    assert ds.identifier is not None
    schema = aurorax.search.metadata.get_ephemeris_schema(ds.identifier)

    # create an example metadata dictionary
    metadata = {
        "nbtrace_region": "north cleft",
        "sbtrace_region": "south auroral oval",
        "radial_distance": 150.25,
        "radial_trace_region": "low latitude",
        "spacecraft_region": "nightside magnetosheath",
        "state": "definitive",
        "tii_on": True,
        "tii_quality_vixh": 0,
        "tii_quality_vixv": 1,
        "tii_quality_viy": 2,
        "tii_quality_viz": 3
    }

    # validate
    valid = aurorax.search.metadata.validate(schema, metadata)
    print("Metadata valid: %r" % (valid))


# ----------
if (__name__ == "__main__"):
    main()
