import aurorax
import datetime
import time


def test_get_request_logs():
    # start search
    r = aurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                 datetime.datetime(2020, 1, 1, 1, 0, 0),
                                 programs=["swarm"],
                                 platforms=["swarma"],
                                 instrument_types=["ssc-web"])
    r.execute()

    # sleep briefly
    time.sleep(1.0)

    # wait for data
    logs = aurorax.requests.get_logs(r.request_url)

    assert type(logs) is list


def test_get_request_status():
    # start search
    r = aurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                 datetime.datetime(2020, 1, 1, 1, 0, 0),
                                 programs=["swarm"],
                                 platforms=["swarma"],
                                 instrument_types=["footprint"])
    r.execute()

    # sleep briefly
    time.sleep(1.0)

    # get status
    status = aurorax.requests.get_status(r.request_url)
    print(status)

    assert status


def test_get_request_data():
    # start search
    r = aurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                 datetime.datetime(2020, 1, 1, 1, 0, 0),
                                 programs=["swarm"],
                                 platforms=["swarma"],
                                 instrument_types=["footprint"])
    r.execute()

    # sleep briefly
    time.sleep(1.0)

    # wait for data
    status = aurorax.requests.get_status(r.request_url)
    r.update_status(status=status)

    # get data
    data_res = aurorax.requests.get_data(r.data_url)

    assert len(data_res) > 0


def test_wait_for_request_data():
    # start search
    r = aurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                 datetime.datetime(2020, 1, 1, 1, 0, 0),
                                 programs=["swarm"],
                                 platforms=["swarma"],
                                 instrument_types=["footprint"])
    r.execute()

    # sleep briefly
    time.sleep(1.0)

    # wait for data
    status = aurorax.requests.wait_for_data(r.request_url)
    r.update_status(status=status)

    # get data
    r.get_data()

    assert len(r.data) > 0