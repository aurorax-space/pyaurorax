import pyaurorax
import datetime
import pprint
from typing import Dict, List, Union, Optional
from ._data_product import DataProduct

# pdoc init
__pdoc__: Dict = {}


class Search():
    """
    Class representing an AuroraX data products search

    Attributes:
        start: start timestamp of the search (inclusive)
        end: end timestamp of the search (inclusive)
        programs: list of program names to search
        platforms: list of platform names to search
        instrument_types: list of instrument types to search
        metadata_filters: list of dictionaries describing metadata keys and
            values to filter on, defaults to None

            e.g. {
                "key": "string",
                "operator": "=",
                "values": [
                    "string"
                ]
            }
        data_product_type_filters: list of dictionaries describing data product
            types to filter on e.g. "keogram", defaults to None

            e.g. {
                "key": "string",
                "operator": "=",
                "values": [
                    "string"
                ]
            }
        response_format: JSON representation of desired data response format
        request: pyaurorax.AuroraXResponse object returned when the search is executed
        request_id: unique AuroraX string ID assigned to the request
        request_url: unique AuroraX URL string assigned to the request
        executed: boolean, gets set to True when the search is executed
        completed: boolean, gets set to True when the search is checked to be finished
        data_url: the URL string where data is accessed
        query: dictionary of values sent for the search query
        status: dictionary of status updates
        data: list of pyaurorax.data_products.DataProduct objects returned, or a list of
            raw JSON results if response_format is specified
        logs: list of logging messages from the API
    """

    def __init__(self,
                 start: datetime.datetime,
                 end: datetime.datetime,
                 programs: Optional[List[str]] = None,
                 platforms: Optional[List[str]] = None,
                 instrument_types: Optional[List[str]] = None,
                 metadata_filters: Optional[List[Dict]] = None,
                 data_product_type_filters: Optional[List[str]] = None,
                 response_format: Optional[Dict] = None,
                 metadata_filters_logical_operator: Optional[str] = "AND") -> None:

        self.request: pyaurorax.api.AuroraXResponse = None
        self.request_id: str = ""
        self.request_url: str = ""
        self.executed: bool = False
        self.completed: bool = False
        self.data_url: str = ""
        self.query: Dict = {}
        self.status: Dict = {}
        self.data: List[Union[DataProduct, Dict]] = []
        self.logs: List[Dict] = []

        self.start = start
        self.end = end
        self.programs = programs
        self.platforms = platforms
        self.instrument_types = instrument_types
        self.metadata_filters = metadata_filters
        self.data_product_type_filters = data_product_type_filters
        self.response_format = response_format
        self.metadata_filters_logical_operator = metadata_filters_logical_operator

    def __str__(self) -> str:
        """
        String method

        Returns:
            string format of DataProduct Search object
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation

        Returns:
            object representation of DataProduct Search object
        """
        return pprint.pformat(self.__dict__)

    def execute(self) -> None:
        """
        Initiate data products search request
        """
        # set up request
        url = pyaurorax.api.urls.data_products_search_url
        post_data = {
            "data_sources": {
                "programs": [] if not self.programs else self.programs,
                "platforms": [] if not self.platforms else self.platforms,
                "instrument_types": [] if not self.instrument_types else self.instrument_types,
                "data_product_metadata_filters": {} if not self.metadata_filters
                else {
                    "logical_operator": self.metadata_filters_logical_operator,
                    "expressions": self.metadata_filters
                },
            },
            "start": self.start.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": self.end.strftime("%Y-%m-%dT%H:%M:%S"),
            "data_product_type_filters": [] if not self.data_product_type_filters else self.data_product_type_filters,
        }
        self.query = post_data

        # do request
        req = pyaurorax.AuroraXRequest(method="post",
                                       url=url,
                                       body=post_data,
                                       null_response=True)
        res = req.execute()

        # set request ID, request_url, executed
        self.executed = True
        if (res.status_code == 202):
            # request successfully dispatched
            self.executed = True
            self.request_url = res.request.headers["location"]
            self.request_id = self.request_url.rsplit("/", 1)[-1]
        self.request = res

    def update_status(self, status: Optional[Dict] = None) -> None:
        """
        Update the status of this data products search request

        Args:
            status: retrieved status dictionary (include to avoid requesting it
                from the API again), defaults to None
        """
        # get the status if it isn't passed in
        if (status is None):
            status = pyaurorax.requests.get_status(self.request_url)

        # update request status by checking if data URI is set
        if (status["search_result"]["data_uri"] is not None):
            self.completed = True
            self.data_url = "%s%s" % (pyaurorax.api.urls.base_url,
                                      status["search_result"]["data_uri"])

        # set class variable "status" and "logs"
        self.status = status
        self.logs = status["logs"]

    def check_for_data(self) -> bool:
        """
        Check to see if data is available for this data products
        search request

        Returns:
            True if data is available, else False
        """
        self.update_status()
        return self.completed

    def get_data(self) -> None:
        """
        Retrieve the data available for this data products search request
        """
        # check if it's completed yet
        if (self.completed is False):
            print("No data available, update status or check for data first")
            return

        # get data
        url = self.data_url
        raw_data = pyaurorax.requests.get_data(url, post_body=self.response_format)

        # set data variable
        if self.response_format is not None:
            self.data = raw_data
        else:
            self.data = [DataProduct(**dp) for dp in raw_data]

    def wait(self,
             verbose: Optional[bool] = False,
             poll_interval: Optional[float] = pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME) -> None:
        """
        Block and wait for the request to complete and data is available
        for retrieval

        Args:
            verbose: output poll times, defaults to False
            poll_interval: time in seconds to wait between polling attempts,
                defaults to pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME
        """
        url = pyaurorax.api.urls.data_products_request_url.format(self.request_id)
        self.update_status(pyaurorax.requests.wait_for_data(url,
                                                            poll_interval=poll_interval,
                                                            verbose=verbose))

    def cancel(self,
               wait: Optional[bool] = False,
               verbose: Optional[bool] = False,
               poll_interval: Optional[float] = pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME) -> int:
        """
        Cancel the data product search request at the API. This method
        returns asynchronously by default.

        Args:
            wait: set to True to block until the cancellation request
                has been completed (may wait for several minutes)
            verbose: if True then output poll times and other
                progress, defaults to False
            poll_interval: seconds to wait between polling
                calls, defaults to STANDARD_POLLING_SLEEP_TIME.

        Returns:
            1 on success

        Raises:
            pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
            pyaurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation
        """
        url = pyaurorax.api.urls.data_products_request_url.format(self.request_id)
        return pyaurorax.requests.cancel(url, wait=wait, poll_interval=poll_interval, verbose=verbose)
