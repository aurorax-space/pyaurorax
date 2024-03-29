import pytest
import datetime
import time
import pyaurorax


@pytest.mark.requests
def test_get_request_logs():
    # start search
    r = pyaurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                   datetime.datetime(2020, 1, 1, 1, 0, 0),
                                   programs=["swarm"],
                                   platforms=["swarma"],
                                   instrument_types=["ssc-web"])
    r.execute()

    # sleep briefly
    time.sleep(1.0)

    # wait for data
    logs = pyaurorax.requests.get_logs(r.request_url)
    assert type(logs) is list


@pytest.mark.requests
def test_get_request_status():
    # start search
    r = pyaurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                   datetime.datetime(2020, 1, 1, 1, 0, 0),
                                   programs=["swarm"],
                                   platforms=["swarma"],
                                   instrument_types=["footprint"])
    r.execute()

    # sleep briefly
    r.wait()

    # get status
    status = pyaurorax.requests.get_status(r.request_url)
    assert status


@pytest.mark.requests
def test_get_request_data():
    # start search
    r = pyaurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                   datetime.datetime(2020, 1, 1, 1, 0, 0),
                                   programs=["swarm"],
                                   platforms=["swarma"],
                                   instrument_types=["footprint"])
    r.execute()

    # sleep briefly
    time.sleep(5)

    # wait for data
    status = pyaurorax.requests.get_status(r.request_url)
    r.update_status(status=status)
    r.wait()

    # get data
    data_res = pyaurorax.requests.get_data(r.data_url)
    assert len(data_res) > 0


@pytest.mark.requests
def test_wait_for_request_data():
    # start search
    r = pyaurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                   datetime.datetime(2020, 1, 1, 1, 0, 0),
                                   programs=["swarm"],
                                   platforms=["swarma"],
                                   instrument_types=["footprint"])
    r.execute()

    # sleep briefly
    time.sleep(1.0)

    # wait for data
    status = pyaurorax.requests.wait_for_data(r.request_url)
    r.update_status(status=status)

    # get data
    r.get_data()
    assert len(r.data) > 0
