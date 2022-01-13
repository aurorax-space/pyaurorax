import pytest
import datetime
import time
import pyaurorax
from pyaurorax.data_products import DataProduct

# globals
MAX_WAIT_TIME = 30


@pytest.mark.data_products
def test_create_data_product_object():
    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    start_dt = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end_dt = start_dt.replace(hour=23, minute=59, second=59)
    data_product_type = pyaurorax.DATA_PRODUCT_TYPE_KEOGRAM
    url = "testing_url.jpg"
    metadata = {}

    # get identifier
    data_source = pyaurorax.sources.get(program, platform, instrument_type)

    # create DataProduct object
    d = pyaurorax.data_products.DataProduct(data_source=data_source,
                                            data_product_type=data_product_type,
                                            url=url,
                                            start=start_dt,
                                            end=end_dt,
                                            metadata=metadata)

    assert type(d) is DataProduct and \
        d.data_source.instrument_type == "test-instrument-type"


@pytest.mark.data_products
def test_create_data_products_search_object():
    s = pyaurorax.data_products.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                       datetime.datetime(2020, 1, 1, 23, 59, 59),
                                       programs=["auroramax"])

    assert type(s) is pyaurorax.data_products.Search \
        and s.end == datetime.datetime(2020, 1, 1, 23, 59, 59)


@pytest.mark.data_products
def test_search_data_products_synchronous():
    s = pyaurorax.data_products.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                       datetime.datetime(2020, 1, 2, 23, 59, 59),
                                       programs=["auroramax"],
                                       data_product_types=[pyaurorax.DATA_PRODUCT_TYPE_KEOGRAM],
                                       verbose=False)

    assert type(s.data) is list and type(s.data[0]) is DataProduct


@pytest.mark.data_products
def test_search_data_products_asynchronous():
    s = pyaurorax.data_products.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                       datetime.datetime(2020, 1, 2, 23, 59, 59),
                                       programs=["auroramax"],
                                       return_immediately=True)

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


@pytest.mark.data_products
def test_search_data_products_metadata_filters_synchronous():
    metadata_filters = [
        {
            "key": "keogram_type",
            "operator": "=",
            "values": [
                "daily_hires"
            ]
        },
        {
            "key": "movie_type",
            "operator": "=",
            "values": [
                "real-time daily"
            ]
        }
    ]
    s = pyaurorax.data_products.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                       datetime.datetime(2020, 1, 2, 23, 59, 59),
                                       programs=["auroramax"],
                                       data_product_types=[
                                           pyaurorax.DATA_PRODUCT_TYPE_KEOGRAM,
                                           pyaurorax.DATA_PRODUCT_TYPE_MOVIE],
                                       metadata_filters=metadata_filters,
                                       verbose=False,
                                       metadata_filters_logical_operator="OR")

    result = s.data
    result_filter = list(filter(lambda dp: (dp.data_product_type == pyaurorax.DATA_PRODUCT_TYPE_MOVIE
                                            and dp.metadata["movie_type"] == "real-time daily")
                                or (dp.data_product_type == pyaurorax.DATA_PRODUCT_TYPE_KEOGRAM
                                    and dp.metadata["keogram_type"] == "daily_hires"), result))

    assert len(s.data) == len(result_filter)


@pytest.mark.data_products
def test_search_data_products_response_format_asynchronous():
    s = pyaurorax.data_products.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                       datetime.datetime(2020, 1, 2, 23, 59, 59),
                                       programs=["auroramax"],
                                       response_format={"start": True,
                                                        "end": True,
                                                        "data_source": {
                                                            "identifier": True,
                                                            "program": True,

                                                        },
                                                        "url": True,
                                                        "metadata": True},
                                       return_immediately=True)

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

    assert type(s.data) is list \
        and type(s.data[0]) is dict \
        and "data_product_type" not in s.data[0].keys()


@pytest.mark.data_products
def test_search_data_products_logs():
    s = pyaurorax.data_products.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
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


@pytest.mark.data_products
def test_search_data_products_status():
    s = pyaurorax.data_products.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
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


@pytest.mark.data_products
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
    data_product_type = pyaurorax.DATA_PRODUCT_TYPE_KEOGRAM
    start_dt = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end_dt = start_dt.replace(hour=23, minute=59, second=59)

    # get the data source ID
    ds = pyaurorax.sources.get(program, platform, instrument_type)

    # create DataProducts object
    dp = pyaurorax.data_products.DataProduct(data_source=ds,
                                             data_product_type=data_product_type,
                                             url=url,
                                             start=start_dt,
                                             end=end_dt,
                                             metadata=metadata)

    start_dt2 = datetime.datetime(2020, 1, 2, 0, 0, 0)
    end_dt2 = start_dt2.replace(hour=23, minute=59, second=59)
    url2 = "test2.jpg"
    dp2 = pyaurorax.data_products.DataProduct(data_source=ds,
                                              data_product_type=data_product_type,
                                              url=url2,
                                              start=start_dt2,
                                              end=end_dt2,
                                              metadata=metadata)

    # set records array
    records = [dp, dp2]

    # upload record
    result = pyaurorax.data_products.upload(ds.identifier, records, True)

    s = pyaurorax.data_products.Search(datetime.datetime(2020, 1, 2, 0, 0, 0),
                                       datetime.datetime(2020, 1, 2, 23, 59, 59),
                                       programs=["test-program"])

    s.execute()
    s.wait()
    s.check_for_data()
    s.get_data()

    assert result == 1 and len(s.data) > 0


@pytest.mark.data_products
def test_delete_data_products():
    program = "test-program"
    platform = "test-platform"
    instrument_type = "pytest"
    start_dt = datetime.datetime(2020, 1, 1, 0, 0)
    end_dt = datetime.datetime(2020, 1, 10, 0, 0, 0)
    source = pyaurorax.sources.get(program, platform, instrument_type)

    # do synchronous search for existing records
    s = pyaurorax.data_products.search(start_dt,
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

    # delete data
    pyaurorax.data_products.delete(source, urls)
    time.sleep(5)

    # search data products again to see if they were deleted
    s = pyaurorax.data_products.search(start_dt,
                                       end_dt,
                                       programs=[program],
                                       platforms=[platform],
                                       instrument_types=[instrument_type])

    assert len(s.data) == 0


@pytest.mark.data_products
def test_delete_data_products_daterange():
    program = "test-program"
    platform = "test-platform"
    instrument_type = "pytest"
    start_dt = datetime.datetime(2021, 6, 27, 0, 0)
    end_dt = datetime.datetime(2021, 6, 29, 0, 0, 0)
    source = pyaurorax.sources.get(program, platform, instrument_type)

    # create DataProducts objects
    dp1 = pyaurorax.data_products.DataProduct(data_source=source,
                                              data_product_type=pyaurorax.DATA_PRODUCT_TYPE_KEOGRAM,
                                              url="datrange-url-1.bmp",
                                              start=datetime.datetime(2021, 6, 27, 1, 0, 0),
                                              end=datetime.datetime(2021, 6, 27, 1, 59, 59),
                                              metadata={"keogram_type": "test"})
    dp2 = pyaurorax.data_products.DataProduct(data_source=source,
                                              data_product_type=pyaurorax.DATA_PRODUCT_TYPE_KEOGRAM,
                                              url="datrange-url-2.bmp",
                                              start=datetime.datetime(2021, 6, 28, 2, 0, 0),
                                              end=datetime.datetime(2021, 6, 28, 2, 59, 59),
                                              metadata=[])
    dp3 = pyaurorax.data_products.DataProduct(data_source=source,
                                              data_product_type=pyaurorax.DATA_PRODUCT_TYPE_MOVIE,
                                              url="datrange-url-3.bmp",
                                              start=datetime.datetime(2021, 6, 27, 1, 0, 0),
                                              end=datetime.datetime(2021, 6, 27, 1, 59, 59),
                                              metadata=[])
    dp4 = pyaurorax.data_products.DataProduct(data_source=source,
                                              data_product_type=pyaurorax.DATA_PRODUCT_TYPE_MOVIE,
                                              url="datrange-url-4.bmp",
                                              start=datetime.datetime(2021, 6, 28, 2, 0, 0),
                                              end=datetime.datetime(2021, 6, 28, 2, 59, 59),
                                              metadata=[])

    # set records array
    records = [dp1, dp2, dp3, dp4]

    # upload data products
    pyaurorax.data_products.upload(source.identifier, records)
    time.sleep(5)

    # delete range of data products
    pyaurorax.data_products.delete_daterange(data_source=source,
                                             start=start_dt,
                                             end=end_dt,
                                             data_product_types=[pyaurorax.DATA_PRODUCT_TYPE_KEOGRAM])
    time.sleep(5)

    # search data products again to see if they were deleted
    s1 = pyaurorax.data_products.search(start_dt,
                                        end_dt,
                                        programs=[program],
                                        platforms=[platform],
                                        instrument_types=[instrument_type],
                                        data_product_types=[pyaurorax.DATA_PRODUCT_TYPE_KEOGRAM])

    assert len(s1.data) == 0


@pytest.mark.data_products
def test_cancel_data_product_search():
    # set up query params
    start_dt = datetime.datetime(2018, 1, 1)
    end_dt = datetime.datetime(2021, 12, 31, 23, 59, 59)
    programs = [
        "themis-asi",
        "auroramax",
        "trex"
    ]

    # search for data products
    s = pyaurorax.data_products.Search(start=start_dt,
                                       end=end_dt,
                                       programs=programs)
    s.execute()

    # cancel the search request
    result = s.cancel(wait=True)
    assert result == 1
