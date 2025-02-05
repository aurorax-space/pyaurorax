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

import pytest
import datetime
import time
from pyaurorax.search import DataProductSearch, DataProductData, DATA_PRODUCT_TYPE_KEOGRAM


@pytest.mark.search_rw
def test_upload_and_delete(aurorax):
    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"

    # get the data source ID
    ds = aurorax.search.sources.get(program, platform, instrument_type)

    # set values
    metadata = {
        "test_meta1": "testing1",
        "test_meta2": "testing2",
    }
    url1 = "test.jpg"
    start_dt1 = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end_dt1 = start_dt1.replace(hour=23, minute=59, second=59)
    url2 = "test2.jpg"
    start_dt2 = datetime.datetime(2020, 1, 2, 0, 0, 0)
    end_dt2 = start_dt2.replace(hour=23, minute=59, second=59)
    data_product_type = DATA_PRODUCT_TYPE_KEOGRAM

    # create DataProducts objects
    dp1 = DataProductData(data_source=ds, data_product_type=data_product_type, url=url1, start=start_dt1, end=end_dt1, metadata=metadata)
    dp2 = DataProductData(data_source=ds, data_product_type=data_product_type, url=url2, start=start_dt2, end=end_dt2, metadata=metadata)

    # set records array
    records = [dp1, dp2]

    # upload records
    result = aurorax.search.data_products.upload(ds.identifier, records, validate_source=True)
    assert result == 0

    # check that records got uploaded
    #
    # NOTE: we periodically check a few times
    max_tries = 10
    for i in range(1, max_tries + 1):
        # wait to it to be ingested
        time.sleep(5)

        # search for data
        s = DataProductSearch(
            aurorax,
            start_dt1,
            end_dt2,
            programs=[program],
            platforms=[platform],
            instrument_types=[instrument_type],
        )
        s.execute()
        s.wait()
        s.get_data()

        # check
        if (len(s.data) == 0):
            if (i == max_tries):
                # failed after all the tries for checking
                raise AssertionError("Max tries reached")
            else:
                continue
        assert len(s.data) > 0
        break

    # cleanup by deleting the data products data that was uploaded
    delete_result = aurorax.search.data_products.delete(
        ds,
        datetime.datetime(2020, 1, 1, 0, 0),
        datetime.datetime(2020, 1, 3, 0, 0),
    )
    assert delete_result == 0


@pytest.mark.search_rw
def test_upload_and_delete_urls(aurorax):
    # get data source
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    ds = aurorax.search.sources.get(program, platform, instrument_type)

    # upload record
    url1 = "test_delete1.jpg"
    start_dt1 = datetime.datetime(2020, 2, 1, 0, 0, 0)
    end_dt1 = start_dt1.replace(hour=23, minute=59, second=59)
    url2 = "test_delete2.jpg"
    start_dt2 = datetime.datetime(2020, 2, 2, 0, 0, 0)
    end_dt2 = start_dt2.replace(hour=23, minute=59, second=59)
    dp1 = DataProductData(data_source=ds, data_product_type=DATA_PRODUCT_TYPE_KEOGRAM, url=url1, start=start_dt1, end=end_dt1)
    dp2 = DataProductData(data_source=ds, data_product_type=DATA_PRODUCT_TYPE_KEOGRAM, url=url2, start=start_dt2, end=end_dt2)
    records = [dp1, dp2]
    result = aurorax.search.data_products.upload(ds.identifier, records, True)
    assert result == 0

    # set urls to delete
    urls_to_delete = [dp1.url, dp2.url]

    # delete data
    delete_result = aurorax.search.data_products.delete_urls(ds, urls_to_delete)
    assert delete_result == 0
