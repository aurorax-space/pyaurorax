
# import pytest
# import datetime
# import time
# from pyaurorax.search import (
#     DataSource,
#     DataProductData,
#     DataProductSearch,
#     DATA_PRODUCT_TYPE_KEOGRAM,
#     DATA_PRODUCT_TYPE_MOVIE,
# )

# # globals
# MAX_WAIT_TIME = 30


# @pytest.mark.search_ro
# def test_create_data_product_object(aurorax):
#     # set values
#     program = "test-program"
#     platform = "test-platform"
#     instrument_type = "test-instrument-type"
#     start_dt = datetime.datetime(2020, 1, 1, 0, 0, 0)
#     end_dt = start_dt.replace(hour=23, minute=59, second=59)
#     data_product_type = DATA_PRODUCT_TYPE_KEOGRAM
#     url = "testing_url.jpg"
#     metadata = {}

#     # get identifier
#     data_source = aurorax.search.sources.get(program, platform, instrument_type)

#     # create DataProduct object
#     d = DataProductData(
#         data_source=data_source,
#         data_product_type=data_product_type,
#         url=url,
#         start=start_dt,
#         end=end_dt,
#         metadata=metadata,
#     )

#     assert isinstance(d, DataProductData) is True
#     assert isinstance(d.data_source, DataSource) is True
#     assert d.data_source.program == program
#     assert d.data_source.platform == platform
#     assert d.data_source.instrument_type == instrument_type


# @pytest.mark.search_ro
# def test_create_data_products_search_object(aurorax):
#     # set vars
#     start_dt = datetime.datetime(2020, 1, 1, 0, 0, 0)
#     end_dt = datetime.datetime(2020, 1, 1, 23, 59, 59)
#     programs = ["auroramax"]

#     s = DataProductSearch(aurorax, start_dt, end_dt, programs=programs)

#     assert isinstance(s, DataProductSearch) is True
#     assert s.start == start_dt
#     assert s.end == end_dt
#     assert s.programs == programs


# @pytest.mark.search_ro
# def test_search_data_products_synchronous(aurorax):
#     s = aurorax.search.data_products.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
#                                             datetime.datetime(2020, 1, 2, 23, 59, 59),
#                                             programs=["auroramax"],
#                                             data_product_types=[DATA_PRODUCT_TYPE_KEOGRAM],
#                                             verbose=False)

#     assert isinstance(s.data, list) is True
#     assert len(s.data) > 0
#     assert isinstance(s.data[0], DataProductData) is True


# @pytest.mark.search_ro
# def test_search_data_products_asynchronous(aurorax):
#     s = aurorax.search.data_products.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
#                                             datetime.datetime(2020, 1, 2, 23, 59, 59),
#                                             programs=["auroramax"],
#                                             return_immediately=True)

#     s.update_status()
#     total_sleep_time = 0
#     while (s.completed is False and total_sleep_time < MAX_WAIT_TIME):
#         time.sleep(1)
#         s.update_status()
#         total_sleep_time += 1

#     if (total_sleep_time == MAX_WAIT_TIME):
#         # search is taking too long to complete
#         raise AssertionError("Request took too long to complete")

#     s.get_data()

#     assert isinstance(s.data, list) is True
#     assert len(s.data) > 0
#     assert isinstance(s.data[0], DataProductData) is True


# @pytest.mark.search_ro
# def test_search_data_products_metadata_filters_synchronous(aurorax):
#     metadata_filters = [{
#         "key": "keogram_type",
#         "operator": "=",
#         "values": ["daily_hires"]
#     }, {
#         "key": "movie_type",
#         "operator": "=",
#         "values": ["real-time daily"]
#     }]
#     s = aurorax.search.data_products.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
#                                             datetime.datetime(2020, 1, 2, 23, 59, 59),
#                                             programs=["auroramax"],
#                                             data_product_types=[DATA_PRODUCT_TYPE_KEOGRAM, DATA_PRODUCT_TYPE_MOVIE],
#                                             metadata_filters=metadata_filters,
#                                             verbose=False,
#                                             metadata_filters_logical_operator="OR")

#     result = s.data
#     result_filter = list(
#         filter(
#             lambda dp: (dp.data_product_type == DATA_PRODUCT_TYPE_MOVIE and dp.metadata["movie_type"] == "real-time daily") or
#             (dp.data_product_type == DATA_PRODUCT_TYPE_KEOGRAM and dp.metadata["keogram_type"] == "daily_hires"), result))

#     assert len(s.data) == len(result_filter)


# @pytest.mark.search_ro
# def test_search_data_products_response_format_asynchronous(aurorax):
#     s = aurorax.search.data_products.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
#                                             datetime.datetime(2020, 1, 2, 23, 59, 59),
#                                             programs=["auroramax"],
#                                             response_format={
#                                                 "start": True,
#                                                 "end": True,
#                                                 "data_source": {
#                                                     "identifier": True,
#                                                     "program": True,
#                                                 },
#                                                 "url": True,
#                                                 "metadata": True
#                                             },
#                                             return_immediately=True)

#     s.update_status()
#     total_sleep_time = 0
#     while (s.completed is False and total_sleep_time < MAX_WAIT_TIME):
#         time.sleep(1)
#         s.update_status()
#         total_sleep_time += 1

#     if (total_sleep_time == MAX_WAIT_TIME):
#         # search is taking too long to complete
#         raise AssertionError("Request took too long to complete")

#     s.get_data()

#     assert isinstance(s.data, list) is True
#     assert len(s.data) > 0
#     assert isinstance(s.data[0], dict) is True
#     assert "data_product_type" not in s.data[0].keys()


# @pytest.mark.search_ro
# def test_search_data_products_logs(aurorax):
#     s = DataProductSearch(
#         aurorax,
#         datetime.datetime(2020, 1, 1, 0, 0, 0),
#         datetime.datetime(2020, 1, 1, 23, 59, 59),
#         programs=["auroramax"],
#     )

#     s.execute()
#     s.update_status()
#     total_sleep_time = 0
#     while (s.completed is False and total_sleep_time < MAX_WAIT_TIME):
#         time.sleep(1)
#         s.update_status()
#         total_sleep_time += 1

#     if (total_sleep_time == MAX_WAIT_TIME):
#         # search is taking too long to complete
#         raise AssertionError("Request took too long to complete")

#     assert len(s.logs) > 0


# @pytest.mark.search_ro
# def test_search_data_products_status(aurorax):
#     s = DataProductSearch(
#         aurorax,
#         datetime.datetime(2020, 1, 1, 0, 0, 0),
#         datetime.datetime(2020, 1, 1, 23, 59, 59),
#         programs=["auroramax"],
#     )

#     s.execute()
#     s.update_status()
#     total_sleep_time = 0
#     while (s.completed is False and total_sleep_time < MAX_WAIT_TIME):
#         time.sleep(1)
#         s.update_status()
#         total_sleep_time += 1

#     if (total_sleep_time == MAX_WAIT_TIME):
#         # search is taking too long to complete
#         raise AssertionError("Request took too long to complete")

#     assert s.completed is True


# @pytest.mark.search_rw
# def test_upload_and_delete_data_products(aurorax):
#     # set values
#     program = "test-program"
#     platform = "test-platform"
#     instrument_type = "test-instrument-type"

#     # get the data source ID
#     ds = aurorax.search.sources.get(program, platform, instrument_type)

#     # set values
#     metadata = {
#         "test_meta1": "testing1",
#         "test_meta2": "testing2",
#     }
#     url1 = "test.jpg"
#     start_dt1 = datetime.datetime(2020, 1, 1, 0, 0, 0)
#     end_dt1 = start_dt1.replace(hour=23, minute=59, second=59)
#     url2 = "test2.jpg"
#     start_dt2 = datetime.datetime(2020, 1, 2, 0, 0, 0)
#     end_dt2 = start_dt2.replace(hour=23, minute=59, second=59)
#     data_product_type = DATA_PRODUCT_TYPE_KEOGRAM

#     # create DataProducts objects
#     dp1 = DataProductData(data_source=ds, data_product_type=data_product_type, url=url1, start=start_dt1, end=end_dt1, metadata=metadata)
#     dp2 = DataProductData(data_source=ds, data_product_type=data_product_type, url=url2, start=start_dt2, end=end_dt2, metadata=metadata)

#     # set records array
#     records = [dp1, dp2]

#     # upload records
#     result = aurorax.search.data_products.upload(ds.identifier, records, True)
#     assert result == 0

#     # check that records got uploaded
#     #
#     # NOTE: we periodically check a few times
#     max_tries = 10
#     for i in range(1, max_tries + 1):
#         # wait to it to be ingested
#         time.sleep(5)

#         # search for data
#         s = DataProductSearch(
#             aurorax,
#             start_dt1,
#             end_dt2,
#             programs=[program],
#             platforms=[platform],
#             instrument_types=[instrument_type],
#         )
#         s.execute()
#         s.wait()
#         s.get_data()

#         # check
#         if (len(s.data) == 0):
#             if (i == max_tries):
#                 # failed after all the tries for checking
#                 raise AssertionError("Max tries reached")
#             else:
#                 continue
#         assert len(s.data) > 0
#         break

#     # cleanup by deleting the data products data that was uploaded
#     delete_result = aurorax.search.ephemeris.delete(
#         ds,
#         datetime.datetime(2020, 1, 1, 0, 0),
#         datetime.datetime(2020, 1, 3, 0, 0),
#     )
#     assert delete_result == 0


# @pytest.mark.search_rw
# def test_upload_and_delete_urls_data_products(aurorax):
#     # get data source
#     program = "test-program"
#     platform = "test-platform"
#     instrument_type = "test-instrument-type"
#     ds = aurorax.search.sources.get(program, platform, instrument_type)

#     # upload record
#     url1 = "test_delete1.jpg"
#     start_dt1 = datetime.datetime(2020, 2, 1, 0, 0, 0)
#     end_dt1 = start_dt1.replace(hour=23, minute=59, second=59)
#     url2 = "test_delete2.jpg"
#     start_dt2 = datetime.datetime(2020, 2, 2, 0, 0, 0)
#     end_dt2 = start_dt2.replace(hour=23, minute=59, second=59)
#     dp1 = DataProductData(data_source=ds, data_product_type=DATA_PRODUCT_TYPE_KEOGRAM, url=url1, start=start_dt1, end=end_dt1)
#     dp2 = DataProductData(data_source=ds, data_product_type=DATA_PRODUCT_TYPE_KEOGRAM, url=url2, start=start_dt2, end=end_dt2)
#     records = [dp1, dp2]
#     result = aurorax.search.data_products.upload(ds.identifier, records, True)
#     assert result == 0

#     # set urls to delete
#     urls_to_delete = [dp1.url, dp2.url]

#     # delete data
#     delete_result = aurorax.search.data_products.delete_urls(ds, urls_to_delete)
#     assert delete_result == 0


# @pytest.mark.search_ro
# def test_cancel_data_products_search(aurorax):
#     # set up query params
#     start_dt = datetime.datetime(2018, 1, 1)
#     end_dt = datetime.datetime(2021, 12, 31, 23, 59, 59)
#     programs = ["themis-asi", "auroramax", "trex"]

#     # search for data products
#     s = DataProductSearch(aurorax, start=start_dt, end=end_dt, programs=programs)
#     s.execute()

#     # cancel the search request
#     result = s.cancel(wait=True)
#     assert result == 0


# @pytest.mark.search_ro
# def test_describe_data_products_search(aurorax):
#     # set params
#     start = datetime.datetime(2020, 1, 1, 0, 0, 0)
#     end = datetime.datetime(2020, 1, 2, 23, 59, 59)
#     programs = ["auroramax"]
#     data_product_types = [DATA_PRODUCT_TYPE_KEOGRAM]
#     expected_response_str = "Find data_products for ((program in (auroramax) filtered by " \
#         "metadata ()) AND  data_product_metadata_filters []) AND data_product start >= " \
#         "2020-01-01T00:00 UTC AND data_product end <= 2020-01-02T23:59:59 UTC AND " \
#         "data_product_type in (keogram)"

#     # create search object
#     s = DataProductSearch(aurorax, start, end, programs=programs, data_product_types=data_product_types)  # type: ignore

#     # get describe string
#     describe_str = aurorax.search.data_products.describe(s)

#     # test response
#     assert describe_str is not None
#     assert describe_str == expected_response_str


# @pytest.mark.search_ro
# def test_get_request_url(aurorax):
#     request_id = "testing-request-id"
#     expected_url = aurorax.api_base_url + "/api/v1/data_products/requests/" + request_id
#     returned_url = aurorax.search.data_products.get_request_url(request_id)
#     assert returned_url == expected_url
