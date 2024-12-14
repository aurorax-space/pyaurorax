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
"""
Functions for using conjunction searches with Swarm-Aurora
"""

import webbrowser
import json
from ...api import AuroraXAPIRequest
from ....exceptions import AuroraXError


def get_url(search_obj):
    return "https://swarm-aurora.com/conjunctionFinder?aurorax_request_id=%s" % (search_obj.request_id)


def open_in_browser(search_obj, browser):
    url = get_url(search_obj)
    try:
        w = webbrowser.get(using=browser)
        w.open_new_tab(url)
    except Exception as e:
        if ("could not locate runnable browser" in str(e)):
            raise AuroraXError(("Error: selected browser '%s' not found, please try another. For the list of options, refer to "
                                "https://docs.python.org/3/library/webbrowser.html#webbrowser.get") % (browser)) from e


def create_custom_import_file(aurorax_obj, search_obj, filename, return_dict):
    # make request
    url = "https://swarm-aurora.com/conjunctionFinder/generate_custom_import_json?aurorax_request_id=%s" % (search_obj.request_id)
    req = AuroraXAPIRequest(aurorax_obj, method="get", url=url, body=search_obj.query)
    res = req.execute()

    # return the contents as a dict if requested
    if (return_dict is True):
        return res.data

    # set default filename
    if (filename is None):
        filename = "swarmaurora_custom_import_%s.json" % (search_obj.request_id)

    # save data to file
    with open(filename, 'w', encoding="utf-8") as fp:
        json.dump(res.data, fp, indent=4)

    # return
    return filename
