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

from .classes.availability_result import AvailabilityResult
from ..sources import DataSource
from ..api import AuroraXAPIRequest


def ephemeris(aurorax_obj, start, end, program, platform, instrument_type, source_type, owner, format, slow):
    # set parameters
    params = {
        "start": start.strftime("%Y-%m-%d"),
        "end": end.strftime("%Y-%m-%d"),
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "source_type": source_type,
        "owner": owner,
        "format": format,
        "slow": slow,
    }

    # do request
    url = "%s/%s" % (aurorax_obj.api_base_url, aurorax_obj.search.api.URL_SUFFIX_EPHEMERIS_AVAILABILITY)
    req = AuroraXAPIRequest(aurorax_obj, method="get", url=url, params=params)
    res = req.execute()

    # cast data source record
    for i in range(0, len(res.data)):
        ds = DataSource(**res.data[i]["data_source"], format=format)
        res.data[i]["data_source"] = ds

    # return
    return [AvailabilityResult(**av) for av in res.data]


def data_products(aurorax_obj, start, end, program, platform, instrument_type, source_type, owner, format, slow):
    # set parameters
    params = {
        "start": start.strftime("%Y-%m-%d"),
        "end": end.strftime("%Y-%m-%d"),
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "source_type": source_type,
        "owner": owner,
        "format": format,
        "slow": slow,
    }

    # do request
    url = "%s/%s" % (aurorax_obj.api_base_url, aurorax_obj.search.api.URL_SUFFIX_DATA_PRODUCTS_AVAILABILITY)
    req = AuroraXAPIRequest(aurorax_obj, method="get", url=url, params=params)
    res = req.execute()

    # cast data source record
    for i in range(0, len(res.data)):
        ds = DataSource(**res.data[i]["data_source"], format=format)
        res.data[i]["data_source"] = ds

    # return
    return [AvailabilityResult(**av) for av in res.data]
