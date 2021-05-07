import aurorax
import datetime
import time

MAX_WAIT_TIME = 30

api_key = "ff179c25-962f-4cc8-b77d-bf16768c0991:c2c008f9-c50f-445c-a459-982606e0b1b1"
aurorax.api.set_base_url("https://api.staging.aurorax.space")
aurorax.authenticate(api_key)

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
    identifier = data_source["identifier"]

    # create DataProduct object
    d = aurorax.data_products.DataProduct(identifier=identifier,
                                          program=program,
                                          platform=platform,
                                          instrument_type=instrument_type,
                                          data_product_type=data_product_type,
                                          url=url,
                                          start=start_dt,
                                          end=end_dt,
                                          metadata=metadata)

    assert type(d) is aurorax.data_products.DataProduct and d.instrument_type == "test-instrument-type"


def test_create_data_products_search_object():
    s = aurorax.data_products.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                     datetime.datetime(2020, 1, 1, 23, 59, 59),
                                     programs=["auroramax"])
    
    assert type(s) is aurorax.data_products.Search and s.end_dt ==  datetime.datetime(2020, 1, 1, 23, 59, 59)


def test_search_data_products_synchronous():
    s = aurorax.data_products.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                     datetime.datetime(2020, 1, 1, 23, 59, 59),
                                     programs=["auroramax"],
                                     verbose=True)

    assert len(s.data) > 0 and "data_source" in s.data[0]


def test_search_data_products_asynchronous():
    s = aurorax.data_products.search_async(datetime.datetime(2019, 1, 1, 0, 0, 0),
                                 datetime.datetime(2019, 1, 1, 0, 59, 59),
                                 programs=["swarm"])

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

    s.get_data()

    assert s.data_url


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


def test_upload_data_product():
    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    url = "test.jpg"
    metadata = {
        "test_meta1": "testing1",
        "test_meta2": "testing2",
    }
    data_product_type = "keogram"
    start_dt = datetime.datetime(2020, 1, 2, 0, 0, 0)
    end_dt = start_dt.replace(hour=23, minute=59, second=59)

    # get the data source ID
    ds = aurorax.sources.get(program, platform, instrument_type)
    identifier = ds["identifier"]

    # create DataProducts object
    e = aurorax.data_products.DataProduct(identifier=identifier,
                                          program=program,
                                          platform=platform,
                                          instrument_type=instrument_type,
                                          data_product_type=data_product_type,
                                          url=url,
                                          start=start_dt,
                                          end=end_dt,
                                          metadata=metadata)

    # set records array
    records = []
    records.append(e)

    # upload record
    result = aurorax.data_products.upload(identifier, records=records)

    s = aurorax.data_products.Search(datetime.datetime(2020, 1, 2, 0, 0, 0),
                                     datetime.datetime(2020, 1, 2, 23, 59, 59),
                                     programs=["test-program"])

    s.execute()
    s.wait()
    s.check_for_data()
    s.get_data()

    assert result == 0 and len(s.data) > 0


def test_delete_data_products():
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    start_dt = datetime.datetime(2020, 1, 1, 0, 0)
    end_dt = datetime.datetime(2020, 1, 10, 0, 0, 0)
    source = aurorax.sources.get(program, platform, instrument_type, format="identifier_only")

    if len(source) != 1:
        assert False

    # do synchronous search for existing records
    s = aurorax.data_products.search(start_dt,
                                 end_dt,
                                 programs=[program],
                                 platforms=[platform],
                                 instrument_types=[instrument_type])

    if len(s.data) == 0:
        print("No data products records exist to delete")
        assert False
    else:
        print(f"{len(s.data)} records found to be deleted")

    urls = []
    # get URLs to delete
    for dp in s.data:
        urls.append(dp["url"])

    params = {
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "urls": urls
    }

    delete_req = aurorax.AuroraXRequest(method="delete", url=aurorax.api.urls.data_products_upload_url.format(source["identifier"]), body=params)

    try:
        delete_req.execute()
    except KeyError as err:
        # this is here because the API does not return a "Content-Type" header
        pass

    # search data products again to see if they were deleted
    s = aurorax.data_products.search(start_dt,
                                 end_dt,
                                 programs=[program],
                                 platforms=[platform],
                                 instrument_types=[instrument_type])

    assert len(s.data) == 0