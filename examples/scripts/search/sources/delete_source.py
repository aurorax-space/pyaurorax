import pyaurorax
import os
from dotenv import load_dotenv


def main():
    # read API key from environment vars
    aurorax = pyaurorax.PyAuroraX()
    load_dotenv("%s/../../../../tests/test_suite/.env" % (os.path.dirname(os.path.realpath(__file__))))
    aurorax.api_base_url = "https://api.staging.aurorax.space"
    aurorax.api_key = os.environ["AURORAX_API_KEY"]

    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument"

    # get data source so we can determine its identifier (used for deletion)
    sources = aurorax.search.sources.get_using_filters(program=program, platform=platform, instrument_type=instrument_type)
    if (len(sources) == 0):
        sources = aurorax.search.sources.get_using_filters(program=program, platform=platform, instrument_type="test-instrument-updated")
        if (len(sources) == 0):
            print("No data source found")
            return
    identifier = sources[0].identifier
    if (identifier is None):
        return

    # remove source
    aurorax.search.sources.delete(identifier)
    print("Successfully removed data source")


# ----------
if (__name__ == "__main__"):
    main()
