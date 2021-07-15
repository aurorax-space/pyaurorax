import aurorax
import datetime
import time
from typing import Dict, List

# globals
FIRST_FOLLOWUP_SLEEP_TIME = 0.050  # 50ms
STANDARD_POLLING_SLEEP_TIME = 1.0  # 1s


def get_status(request_url: str) -> Dict:
    """
    Retrieve the status of a request

    Attributes:
        request_url: URL of the request information

    Returns:
    Status dictionary for the request

    """
    # do request
    req = aurorax.AuroraXRequest(method="get", url=request_url)
    res = req.execute()

    # return
    return res.data


def get_data(data_url: str) -> List:
    """
    Retrieve the data for a request

    Attributes:
        data_url: URL for the data of a request

    Returns:
    List of JSON data objects in the response

    """
    # do request
    req = aurorax.AuroraXRequest(method="get", url=data_url)
    res = req.execute()

    # set data var
    data_result = res.data["result"]

    # serialize epochs and locations into datetimes and Locations
    for i in range(0, len(data_result)):
        if ("epoch" in data_result[i]):
            data_result[i]["epoch"] = datetime.datetime.strptime(data_result[i]["epoch"],
                                                                 "%Y-%m-%dT%H:%M:%S")
        if ("location_geo" in data_result[i]):
            data_result[i]["location_geo"] = aurorax.Location(lat=data_result[i]["location_geo"]["lat"],
                                                              lon=data_result[i]["location_geo"]["lon"])
        if ("location_gsm" in data_result[i]):
            data_result[i]["location_gsm"] = aurorax.Location(lat=data_result[i]["location_gsm"]["lat"],
                                                              lon=data_result[i]["location_gsm"]["lon"])
        if ("nbtrace" in data_result[i]):
            data_result[i]["nbtrace"] = aurorax.Location(lat=data_result[i]["nbtrace"]["lat"],
                                                         lon=data_result[i]["nbtrace"]["lon"])
        if ("sbtrace" in data_result[i]):
            data_result[i]["sbtrace"] = aurorax.Location(lat=data_result[i]["sbtrace"]["lat"],
                                                         lon=data_result[i]["sbtrace"]["lon"])

    # return
    return data_result


def get_logs(request_url: str) -> List:
    """
    Retrieve the logs for a request

    Attributes:
        request_url: URL of the request information

    Returns:
    List of logged messages for the request

    """
    # get status
    status = get_status(request_url)

    if ("logs" in status):
        return status["logs"]
    else:
        return []


def wait_for_data(request_url: str,
                  poll_interval: float = STANDARD_POLLING_SLEEP_TIME,
                  verbose: bool = False) -> Dict:
    """
    Block and wait for the data to be made available for a request

    Attributes:
        request_url: URL of the request information
        poll_interval: seconds to wait between polling calls, defaults to STANDARD_POLLING_SLEEP_TIME
        verbose: output poll times, defaults to False

    Returns:
    Status dictionary for the request
    
    """
    status = get_status(request_url)
    while (status["search_result"]["data_uri"] is None):
        time.sleep(poll_interval)
        if (verbose is True):
            print("[%s] Checking for data ..." % (datetime.datetime.now()))
        status = get_status(request_url)
    if (verbose is True):
        print("[%s] Data is now available" % (datetime.datetime.now()))
    return status
