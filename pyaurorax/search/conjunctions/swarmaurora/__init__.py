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

from typing import Optional, Any
from ..classes.search import ConjunctionSearch
from ._swarmaurora import create_custom_import_file as func_create_custom_import_file
from ._swarmaurora import get_url as func_get_url
from ._swarmaurora import open_in_browser as func_open_in_browser

__all__ = ["SwarmAuroraManager"]


class SwarmAuroraManager:
    """
    The SwarmAuroraManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    def __init__(self, aurorax_obj):
        self.__aurorax_obj = aurorax_obj

    def get_url(self, search_obj: ConjunctionSearch) -> str:
        """
        Get a URL that displays a conjunction search in the Swarm-Aurora
        Conjunction Finder

        Args:
            search_obj: a conjunction search object, must be a completed
                        search with the 'request_id' value populated

        Returns:
            the Swarm-Aurora Conjunction Finder URL for this conjunction search
        """
        return func_get_url(search_obj)

    def open_in_browser(self, search_obj: ConjunctionSearch, browser: Optional[str] = None) -> None:
        """
        In a browser, open a conjunction search in the Swarm-Aurora Conjunction Finder.

        Args:
            search_obj: a conjunction search object, must be a completed
                        search with the 'request_id' value populated
            browser: the browser type to load using. Default is your
                    default browser. Some common other options are
                    "google-chrome", "firefox", or "safari". For all available
                    options, refer to https://docs.python.org/3/library/webbrowser.html#webbrowser.get
        """
        return func_open_in_browser(search_obj, browser)

    def create_custom_import_file(self, search_obj: ConjunctionSearch, filename: Optional[str] = None, return_dict: bool = False) -> Any:
        """
        Generate a Swarm-Aurora custom import file for a given conjunction search

        Args:
            search_obj: a conjunction search object, must be a completed
                        search with the 'request_id' value populated
            filename: the output filename, default is 'swarmaurora_custom_import_file_{requestID}.json'
            return_dict: return the custom import file contents as a dictionary
                        instead of saving a file, default is False

        Returns:
            the filename of the saved custom import file, or a dictionary with the
            file contents if `return_dict` is set to True
        """
        return func_create_custom_import_file(self.__aurorax_obj, search_obj, filename, return_dict)
