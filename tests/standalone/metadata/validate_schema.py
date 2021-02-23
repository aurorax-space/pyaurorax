import aurorax


def main():
    # get schema
    source = aurorax.sources.get_using_filters(program="swarm", platform="swarma", instrument_type="footprint")
    schema = aurorax.metadata.get_ephemeris_schema(source[0]["identifier"])

    # create an example metadata dictionary
    metadata = {
        "nbtrace_region": "north cleft",
        "sbtrace_region": "south auroral oval",
        "radial_distance": 150.25,
        "radial_trace_region": "low latitude",
        "spacecraft_region": "nightside magnetosheath",
        "state": "definitive",
    }

    # validate
    valid = aurorax.metadata.validate(schema, metadata)
    print("Metadata valid: %r" % (valid))


# ----------
if (__name__ == "__main__"):
    main()
