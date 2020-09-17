import datetime
import time
from typing import Dict
from .api import AuroraXRequest
from .api import URL_API_STUB

# globals
FIRST_FOLLOWUP_SLEEP_TIME = 0.050  # 50ms
STANDARD_POLLING_SLEEP_TIME = 1.0  # 1s


def get_status(request_url: str) -> Dict:
    # get request status
    req = AuroraXRequest(request_url)
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
            return_dict["request_status"]["data_url"] = "%s%s" % (URL_API_STUB, res.data["search_result"]["data_uri"])

    # return
    return return_dict


def get_data(data_url: str) -> Dict:
    # make request
    req = AuroraXRequest(data_url)
    res = req.execute()

    # set return dict
    return_dict = {
        "status_code": res.status_code,
        "data": []
    }
    if (res.status_code == 200):
        return_dict["data"] = res.data

    # serialize epochs to datetime objects
    for i in range(0, len(return_dict["data"])):
        if ("epoch" in return_dict["data"][i]):
            return_dict["data"][i]["epoch"] = datetime.datetime.strptime(return_dict["data"][i]["epoch"],
                                                                         "%Y-%m-%dT%H:%M:%S")

    # return
    return return_dict


def get_logs(request_url: str) -> Dict:
    status = get_status(request_url)
    return_dict = {
        "status_code": status["status_code"],
        "data": [],
    }
    if (status["status_code"] == 200 and "logs" in status["data"]):
        return_dict["data"] = status["data"]["logs"]
    return return_dict


def wait_for_data(request_url: str, poll_interval: float = STANDARD_POLLING_SLEEP_TIME) -> Dict:
    status = get_status(request_url)
    while (status["request_status"]["completed"] is False):
        time.sleep(poll_interval)
        status = get_status(request_url)
    return status
