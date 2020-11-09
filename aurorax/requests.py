import aurorax as _aurorax
import datetime as _datetime
import time as _time
from typing import Dict as _Dict

# globals
FIRST_FOLLOWUP_SLEEP_TIME = 0.050  # 50ms
STANDARD_POLLING_SLEEP_TIME = 1.0  # 1s


def get_status(request_url: str) -> _Dict:
    """
    Retrieve the status of a request

    :param request_url: URL of the request information
    :type request_url: str

    :return: status response
    :rtype: Dict
    """
    # get request status
    req = _aurorax.AuroraXRequest(request_url)
    res = req.execute()

    # set return dict
    return_dict = {
        "status_code": res.status_code,
        "data": {},
        "request_status": {
            "completed": False,
            "data_url": ""
        }
    }

    # determine the status of the request
    if (res.status_code == 200):
        return_dict["data"] = res.data
        if (res.data["search_result"]["data_uri"] is not None):
            return_dict["request_status"]["completed"] = True
            return_dict["request_status"]["data_url"] = "%s%s" % (_aurorax.api._URL_API_STUB,
                                                                  res.data["search_result"]["data_uri"])

    # return
    return return_dict


def get_data(data_url: str) -> _Dict:
    """
    Retrieve the data for a request

    :param data_url: URL for the data of a request
    :type data_url: str

    :return: data response
    :rtype: Dict
    """
    # make request
    req = _aurorax.AuroraXRequest(data_url)
    res = req.execute()

    # set return dict
    return_dict = {
        "status_code": res.status_code,
        "data": []
    }
    if (res.status_code == 200):
        return_dict["data"] = res.data["result"]

    # serialize epochs to datetime objects
    for i in range(0, len(return_dict["data"])):
        if ("epoch" in return_dict["data"][i]):
            return_dict["data"][i]["epoch"] = _datetime.datetime.strptime(return_dict["data"][i]["epoch"],
                                                                          "%Y-%m-%dT%H:%M:%S")

    # return
    return return_dict


def get_logs(request_url: str) -> _Dict:
    """
    Retrieve the logs for a request

    :param request_url: URL of the request information
    :type request_url: str

    :return: logs response
    :rtype: Dict
    """
    status = get_status(request_url)
    return_dict = {
        "status_code": status["status_code"],
        "data": [],
    }
    if (status["status_code"] == 200 and "logs" in status["data"]):
        return_dict["data"] = status["data"]["logs"]
    return return_dict


def wait_for_data(request_url: str, poll_interval: float = STANDARD_POLLING_SLEEP_TIME) -> _Dict:
    """
    Block and wait for the data to be made available for a request

    :param request_url: URL of the request information
    :type request_url: str
    :param poll_interval: seconds to wait between polling calls, defaults to STANDARD_POLLING_SLEEP_TIME
    :type poll_interval: float, optional

    :return: status response
    :rtype: Dict
    """
    status = get_status(request_url)
    while (status["request_status"]["completed"] is False):
        _time.sleep(poll_interval)
        status = get_status(request_url)
    return status
