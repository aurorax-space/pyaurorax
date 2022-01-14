import pyaurorax


def main():
    # get schema
    source = pyaurorax.sources.get_using_filters(program="swarm",
                                                 platform="swarma",
                                                 instrument_type="footprint")
    schema = pyaurorax.metadata.get_ephemeris_schema(source[0].identifier)

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
    valid = pyaurorax.metadata.validate(schema, metadata)
    print("Metadata valid: %r" % (valid))


# ----------
if (__name__ == "__main__"):
    main()
