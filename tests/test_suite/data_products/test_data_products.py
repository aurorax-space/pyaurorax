from aurorax.data_products import DataProduct
import aurorax
import datetime
import os
import time

MAX_WAIT_TIME = 30

def test_create_data_product_object():
    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    start_dt = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end_dt = start_dt.replace(hour=23, minute=59, second=59)
    data_product_type = "keogram"
    url = "testing_url.jpg"
    metadata = {}

    # get identifier
    data_source = aurorax.sources.get(program, platform, instrument_type)

    # create DataProduct object
    d = aurorax.data_products.DataProduct(data_source=data_source,
                                          data_product_type=data_product_type,
                                          url=url,
                                          start=start_dt,
                                          end=end_dt,
                                          metadata=metadata)

    assert type(d) is DataProduct and d.data_source.instrument_type == "test-instrument-type"


def test_create_data_products_search_object():
    s = aurorax.data_products.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                     datetime.datetime(2020, 1, 1, 23, 59, 59),
                                     programs=["auroramax"])
    
    assert type(s) is aurorax.data_products.Search and s.end ==  datetime.datetime(2020, 1, 1, 23, 59, 59)


def test_search_data_products_synchronous():
    s = aurorax.data_products.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                     datetime.datetime(2020, 1, 2, 23, 59, 59),
                                     programs=["auroramax"],
                                     data_product_type_filters=["keogram"],
                                     verbose=False)

    assert type(s.data) is list and type(s.data[0]) is DataProduct


def test_search_data_products_asynchronous():
    s = aurorax.data_products.search_async(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                 datetime.datetime(2020, 1, 2, 23, 59, 59),
                                 programs=["auroramax"])

    s.update_status()
    tries = 0
    while not s.completed and tries < MAX_WAIT_TIME:
        time.sleep(1)
        s.update_status()
        tries += 1

    if tries == MAX_WAIT_TIME:
        # search is taking too long to complete
        assert False

    s.get_data()

    assert type(s.data) is list and type(s.data[0]) is DataProduct


def test_search_data_products_logs():
    s = aurorax.data_products.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                     datetime.datetime(2020, 1, 1, 23, 59, 59),
                                     programs=["auroramax"])

    s.execute()
    s.update_status()
    tries = 0
    while not s.completed and tries < 20:
        time.sleep(1)
        s.update_status()
        tries += 1

    if tries == 20:
        # search is taking too long to complete
        assert False

    assert len(s.logs) > 0


def test_search_data_products_status():
    s = aurorax.data_products.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                     datetime.datetime(2020, 1, 1, 23, 59, 59),
                                     programs=["auroramax"])

    s.execute()
    s.update_status()
    tries = 0
    while not s.completed and tries < MAX_WAIT_TIME:
        time.sleep(1)
        s.update_status()
        tries += 1

    if tries == MAX_WAIT_TIME:
        # search is taking too long to complete
        assert False

    assert s.completed


def test_upload_data_products():
    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "pytest"
    url = "test.jpg"
    metadata = {
        "test_meta1": "testing1",
        "test_meta2": "testing2",
    }
    data_product_type = "keogram"
    start_dt = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end_dt = start_dt.replace(hour=23, minute=59, second=59)

    # get the data source ID
    ds = aurorax.sources.get(program, platform, instrument_type)

    # create DataProducts object
    dp = aurorax.data_products.DataProduct(data_source=ds,
                                          data_product_type=data_product_type,
                                          url=url,
                                          start=start_dt,
                                          end=end_dt,
                                          metadata=metadata)

    start_dt2 = datetime.datetime(2020, 1, 2, 0, 0, 0)
    end_dt2 = start_dt2.replace(hour=23, minute=59, second=59)
    url2 = "test2.jpg"
    dp2 = aurorax.data_products.DataProduct(data_source=ds,
                                          data_product_type=data_product_type,
                                          url=url2,
                                          start=start_dt2,
                                          end=end_dt2,
                                          metadata=metadata)

    # set records array
    records = [dp, dp2]

    # upload record
    result = aurorax.data_products.upload(ds.identifier, records, True)

    s = aurorax.data_products.Search(datetime.datetime(2020, 1, 2, 0, 0, 0),
                                     datetime.datetime(2020, 1, 2, 23, 59, 59),
                                     programs=["test-program"])

    s.execute()
    s.wait()
    s.check_for_data()
    s.get_data()

    assert result == 1 and len(s.data) > 0


def test_delete_data_products():
    program = "test-program"
    platform = "test-platform"
    instrument_type = "pytest"
    start_dt = datetime.datetime(2020, 1, 1, 0, 0)
    end_dt = datetime.datetime(2020, 1, 10, 0, 0, 0)
    source = aurorax.sources.get(program, platform, instrument_type)

    # do synchronous search for existing records
    s = aurorax.data_products.search(start_dt,
                                 end_dt,
                                 programs=[program],
                                 platforms=[platform],
                                 instrument_types=[instrument_type])

    if len(s.data) == 0:
        print("No data product records exist to delete")
        assert False
    else:
        print(f"{len(s.data)} records found to be deleted")

    urls = []
    # get URLs to delete
    for dp in s.data:
        urls.append(dp.url)

    aurorax.data_products.delete(source, urls)

    time.sleep(5)

    # search data products again to see if they were deleted
    s = aurorax.data_products.search(start_dt,
                                 end_dt,
                                 programs=[program],
                                 platforms=[platform],
                                 instrument_types=[instrument_type])

    assert len(s.data) == 0


def test_delete_data_products_daterange():
    program = "test-program"
    platform = "test-platform"
    instrument_type = "pytest"
    start_dt = datetime.datetime(2021, 6, 27, 0, 0)
    end_dt = datetime.datetime(2021, 6, 29, 0, 0, 0)
    source = aurorax.sources.get(program, platform, instrument_type)

    # create DataProducts objects
    dp1 = aurorax.data_products.DataProduct(data_source=source,
                                          data_product_type="keogram",
                                          url="datrange-url-1.bmp",
                                          start=datetime.datetime(2021, 6, 27, 1, 0, 0),
                                          end=datetime.datetime(2021, 6, 27, 1, 59, 59),
                                          metadata={
                                              "keogram_type": "test"
                                          })

    dp2 = aurorax.data_products.DataProduct(data_source=source,
                                          data_product_type="keogram",
                                          url="datrange-url-2.bmp",
                                          start=datetime.datetime(2021, 6, 28, 2, 0, 0),
                                          end=datetime.datetime(2021, 6, 28, 2, 59, 59),
                                          metadata=[])

    dp3 = aurorax.data_products.DataProduct(data_source=source,
                                          data_product_type="movie",
                                          url="datrange-url-3.bmp",
                                          start=datetime.datetime(2021, 6, 27, 1, 0, 0),
                                          end=datetime.datetime(2021, 6, 27, 1, 59, 59),
                                          metadata=[])

    dp4 = aurorax.data_products.DataProduct(data_source=source,
                                          data_product_type="movie",
                                          url="datrange-url-4.bmp",
                                          start=datetime.datetime(2021, 6, 28, 2, 0, 0),
                                          end=datetime.datetime(2021, 6, 28, 2, 59, 59),
                                          metadata=[])

    # set records array
    records = [dp1, dp2, dp3, dp4]

    aurorax.data_products.upload(source.identifier, records)

    time.sleep(5)

    aurorax.data_products.delete_daterange(data_source=source,
                                           start=start_dt,
                                           end=end_dt,
                                           data_product_types=["keogram"],
                                           metadata_filters=[{"key": "keogram_type", "values": ["test"], "operator": "="}])

    time.sleep(5)

    # search data products again to see if they were deleted
    s1 = aurorax.data_products.search(start_dt,
                                      end_dt,
                                      programs=[program],
                                      platforms=[platform],
                                      instrument_types=[instrument_type],
                                      data_product_type_filters=["keogram"])

    aurorax.data_products.delete_daterange(source, start_dt, end_dt)

    time.sleep(5)

    s2 = aurorax.data_products.search(start_dt, 
                                      end_dt,
                                      programs=[program],
                                      platforms=[platform],
                                      instrument_types=[instrument_type])

    assert len(s1.data) == 1 and len(s2.data) == 0