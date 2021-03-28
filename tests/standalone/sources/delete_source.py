import aurorax
import os


def main():
    # read API key from environment vars
    api_key = os.environ["AURORAX_API_KEY"]
    aurorax.api.set_base_url("https://api.staging.aurorax.space")
    aurorax.authenticate(api_key)

    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument"

    # get source record to pull out the identifier
    sources = aurorax.sources.get_using_filters(program=program,
                                                platform=platform,
                                                instrument_type=instrument_type)
    if (len(sources) == 0):
        sources = aurorax.sources.get_using_filters(program=program,
                                                    platform=platform,
                                                    instrument_type="test-instrument-updated")
        if (len(sources) == 0):
            print("No data source found")
            return
    identifier = sources[0]["identifier"]

    # remove source
    aurorax.sources.delete(identifier)
    print("Successfully removed data source")


# ----------
if (__name__ == "__main__"):
    main()
