# Copyright 2024 University of Calgary
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import datetime
import pyaurorax
from pyaurorax.search import Location
from dotenv import load_dotenv


def main():
    # read API key from environment vars
    aurorax = pyaurorax.PyAuroraX()
    load_dotenv("%s/../../../test_suite/.env" % (os.path.dirname(os.path.realpath(__file__))))
    aurorax.api_base_url = "https://api.staging.aurorax.space"
    aurorax.api_key = os.environ["AURORAX_API_KEY"]

    # get the data source ID
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    ds = aurorax.search.sources.get(program, platform, instrument_type)
    if (ds.identifier is None):
        print("Error retrieving valid data source, aborting")
        return 1

    # set values
    metadata = {
        "test_meta1": "testing1",
        "test_meta2": "testing2",
    }
    location_geo = Location(lat=51.049999, lon=-114.066666)
    location_gsm = Location(lat=150.25, lon=-10.75)
    nbtrace = Location(lat=1.23, lon=45.6)
    sbtrace = Location(lat=7.89, lon=101.23)
    records = []
    for i in range(0, 50):
        epoch = datetime.datetime(2020, 6, 1, 0, i)

        # create Ephemeris object
        e = pyaurorax.search.EphemerisData(data_source=ds,
                                           epoch=epoch,
                                           location_geo=location_geo,
                                           location_gsm=location_gsm,
                                           nbtrace=nbtrace,
                                           sbtrace=sbtrace,
                                           metadata=metadata)
        records.append(e)

    print("\nUploading records ...")

    # upload record
    aurorax.search.ephemeris.upload(ds.identifier, records)
    print("Successfully uploaded")


# ----------
if (__name__ == "__main__"):
    main()
