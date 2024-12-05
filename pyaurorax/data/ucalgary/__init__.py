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
Data downloading and reading routines for data provided by the University of Calgary.
"""

import os
import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Optional, List, Union, Literal
from pyucalgarysrs.data import (
    Observatory,
    Dataset,
    FileDownloadResult,
    FileListingResponse,
    Data,
    Skymap,
    Calibration,
)
from pyucalgarysrs.exceptions import SRSAPIError, SRSDownloadError
from ...exceptions import AuroraXAPIError, AuroraXDownloadError
from .read import ReadManager
if TYPE_CHECKING:
    from ...pyaurorax import PyAuroraX

__all__ = [
    "UCalgaryManager",
    "Observatory",
    "Dataset",
    "FileDownloadResult",
    "FileListingResponse",
    "Data",
    "Skymap",
    "Calibration",
]


class UCalgaryManager:
    """
    The UCalgaryManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    __DEFAULT_DOWNLOAD_N_PARALLEL = 5

    def __init__(self, aurorax_obj):
        self.__aurorax_obj: PyAuroraX = aurorax_obj

        # initialize sub-modules
        self.__readers = ReadManager(self.__aurorax_obj)

    @property
    def readers(self):
        """
        Access to the `read` submodule from within a PyAuroraX object.
        """
        return self.__readers

    def list_datasets(self, name: Optional[str] = None, timeout: Optional[int] = None) -> List[Dataset]:
        """
        List available datasets

        Args:
            name (str): 
                Supply a name used for filtering. If that name is found in the available dataset 
                names received from the API, it will be included in the results. This parameter is
                optional.
            
            timeout (int): 
                Represents how many seconds to wait for the API to send data before giving up. The 
                default is 10 seconds, or the `api_timeout` value in the super class' `pyaurorax.PyAuroraX`
                object. This parameter is optional.
            
        Returns:
            A list of [`Dataset`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.Dataset)
            objects.
        
        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered.
        """
        try:
            return self.__aurorax_obj.srs_obj.data.list_datasets(
                name=name,
                timeout=timeout,
                supported_library="pyaurorax",
            )
        except SRSAPIError as e:
            raise AuroraXAPIError(e) from e

    def get_dataset(self, name: str, timeout: Optional[int] = None) -> Dataset:
        """
        Get a specific dataset

        Args:
            name (str): 
                The dataset name to get. Case is insensitive.
            
            timeout (int): 
                Represents how many seconds to wait for the API to send data before giving up. The 
                default is 10 seconds, or the `api_timeout` value in the super class' `pyaurorax.PyAuroraX`
                object. This parameter is optional.
            
        Returns:
            The found [`Dataset`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.Dataset)
            object. Raises an exception if not found.
        
        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered.
        """
        try:
            return self.__aurorax_obj.srs_obj.data.get_dataset(name, timeout=timeout)
        except Exception as e:
            raise AuroraXAPIError(e) from e

    def list_observatories(self,
                           instrument_array: Literal["themis_asi", "rego", "trex_rgb", "trex_nir", "trex_blue", "trex_spectrograph"],
                           uid: Optional[str] = None,
                           timeout: Optional[int] = None) -> List[Observatory]:
        """
        List information about observatories

        Args:
            instrument_array (str): 
                The instrument array to list observatories for. Valid values are: themis_asi, rego, 
                trex_rgb, trex_nir, trex_blue, and trex_spectrograph.

            uid (str): 
                Supply a observatory unique identifier used for filtering (usually 4-letter site code). If that UID 
                is found in the available observatories received from the API, it will be included in the results. This 
                parameter is optional.
            
            timeout (int): 
                Represents how many seconds to wait for the API to send data before giving up. The 
                default is 10 seconds, or the `api_timeout` value in the super class' `pyaurorax.PyAuroraX`
                object. This parameter is optional.
            
        Returns:
            A list of [`Observatory`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.Observatory)
            objects.
        
        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered.
        """
        try:
            return self.__aurorax_obj.srs_obj.data.list_observatories(instrument_array, uid=uid, timeout=timeout)
        except SRSAPIError as e:
            raise AuroraXAPIError(e) from e

    def list_supported_read_datasets(self) -> List[str]:
        """
        List the datasets which have file reading capabilities supported.

        Returns:
            A list of the dataset names with file reading support.
        """
        return self.__aurorax_obj.srs_obj.data.list_supported_read_datasets()

    def is_read_supported(self, dataset_name: str) -> bool:
        """
        Check if a given dataset has file reading support. 
        
        Not all datasets available in the UCalgary Space Remote Sensing Open Data Platform 
        have special readfile routines in this library. This is because some datasets are 
        in basic formats such as JPG or PNG, so unique functions aren't necessary. We leave 
        it up to the user to open these basic files in whichever way they prefer. Use the 
        `list_supported_read_datasets()` function to see all datasets that have special
        file reading functionality in this library.

        Args:
            dataset_name (str): 
                The dataset name to check if file reading is supported. This parameter 
                is required.
        
        Returns:
            Boolean indicating if file reading is supported.
        """
        return self.__aurorax_obj.srs_obj.data.is_read_supported(dataset_name)

    def download(self,
                 dataset_name: str,
                 start: datetime.datetime,
                 end: datetime.datetime,
                 site_uid: Optional[str] = None,
                 device_uid: Optional[str] = None,
                 n_parallel: int = __DEFAULT_DOWNLOAD_N_PARALLEL,
                 overwrite: bool = False,
                 progress_bar_disable: bool = False,
                 progress_bar_ncols: Optional[int] = None,
                 progress_bar_ascii: Optional[str] = None,
                 progress_bar_desc: Optional[str] = None,
                 timeout: Optional[int] = None) -> FileDownloadResult:
        """
        Download data from the UCalgary Space Remote Sensing Open Data Platform.

        The parameters `dataset_name`, `start`, and `end` are required. All other parameters
        are optional.

        Note that usage of the site and device UID filters applies differently to some datasets.
        For example, both fields can be used for most raw and keogram data, but only site UID can
        be used for skymap datasets, and only device UID can be used for calibration datasets. If 
        fields are specified during a call in which site or device UID is not used, a UserWarning
        is display to provide the user with feedback about this detail.

        Args:
            dataset_name (str): 
                Name of the dataset to download data for. Use the `list_datasets()` function
                to get the possible values for this parameter. One example is "THEMIS_ASI_RAW". 
                Note that dataset names are case sensitive. This parameter is required.

            start (datetime.datetime): 
                Start timestamp to use (inclusive), expected to be in UTC. Any timezone data 
                will be ignored. This parameter is required.

            end (datetime.datetime): 
                End timestamp to use (inclusive), expected to be in UTC. Any timezone data 
                will be ignored. This parameter is required.

            site_uid (str): 
                The site UID to filter for. If specified, data will be downloaded for only the 
                site matching the given value. If excluded, data for all available sites will 
                be downloaded. An example value could be 'atha', meaning all data from the 
                Athabasca observatory will be downloaded for the given dataset name, start, and 
                end times. This parameter is optional.

            device_uid (str): 
                The device UID to filter for. If specified, data will be downloaded for only the
                device matching the given value. If excluded, data for all available devices will
                be downloaded. An example value could be 'themis02', meaning all data matching that
                device will be downloaded for the given dataset name, start, and end times. This
                parameter is optional.

            n_parallel (int): 
                Number of data files to download in parallel. Default value is 5. Adjust as needed 
                for your internet connection. This parameter is optional.

            overwrite (bool): 
                By default, data will not be re-downloaded if it already exists locally. Use 
                the `overwrite` parameter to force re-downloading. Default is `False`. This 
                parameter is optional.

            progress_bar_disable (bool): 
                Disable the progress bar. Default is `False`. This parameter is optional.

            progress_bar_ncols (int): 
                Number of columns for the progress bar (straight passthrough of the `ncols` 
                parameter in a tqdm progress bar). This parameter is optional. See Notes section
                below for further information.
            
            progress_bar_ascii (str): 
                ASCII value to use when constructing the visual aspect of the progress bar (straight 
                passthrough of the `ascii` parameter in a tqdm progress bar). This parameter is 
                optional. See Notes section below for further details.

            timeout (int): 
                Represents how many seconds to wait for the API to send data before giving up. The 
                default is 10 seconds, or the `api_timeout` value in the super class' `pyaurorax.PyAuroraX`
                object. This parameter is optional.

        Returns:
            A [`FileDownloadResult`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.FileDownloadResult) 
            object containing details about what data files were downloaded.

        Raises:
            pyaurorax.exceptions.AuroraXDownloadError: an error was encountered while downloading a 
                specific file
            pyaurorax.exceptions.AuroraXAPIError: an API error was encountered

        Notes:
        --------
        The `progress_bar_*` parameters can be used to enable/disable/adjust the progress bar. 
        Excluding the `progress_bar_disable` parameter, all others are straight pass-throughs 
        to the tqdm progress bar function. The `progress_bar_ncols` parameter allows for 
        adjusting the width. The `progress_bar_ascii` parameter allows for adjusting the appearance 
        of the progress bar. And the `progress_bar_desc` parameter allows for adjusting the 
        description at the beginning of the progress bar. Further details can be found on the
        [tqdm documentation](https://tqdm.github.io/docs/tqdm/#tqdm-objects).

        Data downloading will use the `download_data_root_path` variable within the super class'
        object ([`PyAuroraX`](../../index.html#pyaurorax.PyAuroraX)) to determine where to save data to. If 
        you'd like to change this path to somewhere else you can change that variable before your
        download() call, like so:

        ```python
        import pyaurorax
        aurorax = pyaurorax.PyAuroraX()
        aurorax.data_download_root_path = "some_new_path"
        aurorax.data.download(dataset_name, start, end)
        ```
        """
        try:
            return self.__aurorax_obj.srs_obj.data.download(
                dataset_name,
                start,
                end,
                site_uid=site_uid,
                device_uid=device_uid,
                n_parallel=n_parallel,
                overwrite=overwrite,
                progress_bar_disable=progress_bar_disable,
                progress_bar_ncols=progress_bar_ncols,
                progress_bar_ascii=progress_bar_ascii,
                progress_bar_desc=progress_bar_desc,
                timeout=timeout,
            )
        except SRSDownloadError as e:
            raise AuroraXDownloadError(e) from e
        except SRSAPIError as e:
            raise AuroraXAPIError(e) from e

    def download_using_urls(self,
                            file_listing_response: FileListingResponse,
                            n_parallel: int = __DEFAULT_DOWNLOAD_N_PARALLEL,
                            overwrite: bool = False,
                            progress_bar_disable: bool = False,
                            progress_bar_ncols: Optional[int] = None,
                            progress_bar_ascii: Optional[str] = None,
                            progress_bar_desc: Optional[str] = None,
                            timeout: Optional[int] = None) -> FileDownloadResult:
        """
        Download data from the UCalgary Space Remote Sensing Open Data Platform using 
        a FileListingResponse object. This would be used in cases where more customization 
        is needed than the generic `download()` function. 
        
        One example of using this function would start by using `get_urls()` to retrieve the
        list of URLs available for download, then further process this list to fewer files
        based on some other requirement (ie. time down-sampling such as one file per hour). 
        Lastly using this function to download the new custom set URLs.

        Args:
            file_listing_response (FileListingResponse): 
                A [`FileListingResponse`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.FileListingResponse) 
                object returned from a `get_urls()` call, which contains a list of URLs to download 
                for a specific dataset. This parameter is required.

            n_parallel (int): 
                Number of data files to download in parallel. Default value is 5. Adjust as needed 
                for your internet connection. This parameter is optional.

            overwrite (bool): 
                By default, data will not be re-downloaded if it already exists locally. Use 
                the `overwrite` parameter to force re-downloading. Default is `False`. This 
                parameter is optional.

            progress_bar_disable (bool): 
                Disable the progress bar. Default is `False`. This parameter is optional.

            progress_bar_ncols (int): 
                Number of columns for the progress bar (straight passthrough of the `ncols` 
                parameter in a tqdm progress bar). This parameter is optional. See Notes section
                below for further information.
            
            progress_bar_ascii (str): 
                ASCII value to use when constructing the visual aspect of the progress bar (straight 
                passthrough of the `ascii` parameter in a tqdm progress bar). This parameter is 
                optional. See Notes section below for further details.

            timeout (int): 
                Represents how many seconds to wait for the API to send data before giving up. The 
                default is 10 seconds, or the `api_timeout` value in the super class' `pyaurorax.PyAuroraX`
                object. This parameter is optional.

        Returns:
            A [`FileDownloadResult`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.FileDownloadResult) 
            object containing details about what data files were downloaded.

        Raises:
            pyaurorax.exceptions.AuroraXDownloadError: an error was encountered while downloading a 
                specific file
            pyaurorax.exceptions.AuroraXAPIError: an API error was encountered

        Notes:
        --------
        The `progress_bar_*` parameters can be used to enable/disable/adjust the progress bar. 
        Excluding the `progress_bar_disable` parameter, all others are straight pass-throughs 
        to the tqdm progress bar function. The `progress_bar_ncols` parameter allows for 
        adjusting the width. The `progress_bar_ascii` parameter allows for adjusting the appearance 
        of the progress bar. And the `progress_bar_desc` parameter allows for adjusting the 
        description at the beginning of the progress bar. Further details can be found on the
        [tqdm documentation](https://tqdm.github.io/docs/tqdm/#tqdm-objects).

        Data downloading will use the `download_data_root_path` variable within the super class'
        object ([`PyAuroraX`](../../index.html#pyaurorax.PyAuroraX)) to determine where to save data to. If 
        you'd like to change this path to somewhere else you can change that variable before your
        download() call, like so:

        ```python
        import pyaurorax
        aurorax = pyaurorax.PyAuroraX()
        aurorax.data_download_root_path = "some_new_path"
        aurorax.data.download(dataset_name, start, end)
        ```
        """
        try:
            return self.__aurorax_obj.srs_obj.data.download_using_urls(
                file_listing_response,
                n_parallel=n_parallel,
                overwrite=overwrite,
                progress_bar_disable=progress_bar_disable,
                progress_bar_ncols=progress_bar_ncols,
                progress_bar_ascii=progress_bar_ascii,
                progress_bar_desc=progress_bar_desc,
                timeout=timeout,
            )
        except SRSDownloadError as e:
            raise AuroraXDownloadError(e) from e
        except SRSAPIError as e:
            raise AuroraXAPIError(e) from e

    def get_urls(self,
                 dataset_name: str,
                 start: datetime.datetime,
                 end: datetime.datetime,
                 site_uid: Optional[str] = None,
                 device_uid: Optional[str] = None,
                 timeout: Optional[int] = None) -> FileListingResponse:
        """
        Get URLs of data files

        The parameters `dataset_name`, `start`, and `end` are required. All other parameters
        are optional.

        Note that usage of the site and device UID filters applies differently to some datasets.
        For example, both fields can be used for most raw and keogram data, but only site UID can
        be used for skymap datasets, and only device UID can be used for calibration datasets. If 
        fields are specified during a call in which site or device UID is not used, a UserWarning
        is display to provide the user with feedback about this detail.

        Args:
            dataset_name (str): 
                Name of the dataset to download data for. Use the `list_datasets()` function
                to get the possible values for this parameter. One example is "THEMIS_ASI_RAW". 
                Note that dataset names are case sensitive. This parameter is required.

            start (datetime.datetime): 
                Start timestamp to use (inclusive), expected to be in UTC. Any timezone data 
                will be ignored. This parameter is required.

            end (datetime.datetime): 
                End timestamp to use (inclusive), expected to be in UTC. Any timezone data 
                will be ignored. This parameter is required.

            site_uid (str): 
                The site UID to filter for. If specified, data will be downloaded for only the 
                site matching the given value. If excluded, data for all available sites will 
                be downloaded. An example value could be 'atha', meaning all data from the 
                Athabasca observatory will be downloaded for the given dataset name, start, and 
                end times. This parameter is optional.

            device_uid (str): 
                The device UID to filter for. If specified, data will be downloaded for only the
                device matching the given value. If excluded, data for all available devices will
                be downloaded. An example value could be 'themis02', meaning all data matching that
                device will be downloaded for the given dataset name, start, and end times. This
                parameter is optional.

            timeout (int): 
                Represents how many seconds to wait for the API to send data before giving up. The 
                default is 10 seconds, or the `api_timeout` value in the super class' `pyaurorax.PyAuroraX`
                object. This parameter is optional.
    
        Returns:
            A [`FileListingResponse`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.FileListingResponse)
            object containing a list of the available URLs, among other values.

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: an API error was encountered
        """
        try:
            return self.__aurorax_obj.srs_obj.data.get_urls(
                dataset_name,
                start,
                end,
                site_uid=site_uid,
                device_uid=device_uid,
                timeout=timeout,
            )
        except SRSAPIError as e:
            raise AuroraXAPIError(e) from e

    def read(self,
             dataset: Dataset,
             file_list: Union[List[str], List[Path], str, Path],
             n_parallel: int = 1,
             first_record: bool = False,
             no_metadata: bool = False,
             start_time: Optional[datetime.datetime] = None,
             end_time: Optional[datetime.datetime] = None,
             quiet: bool = False) -> Data:
        """
        Read in data files for a given dataset. Note that only one type of dataset's data
        should be read in using a single call.

        Args:
            dataset (Dataset): 
                The dataset object for which the files are associated with. This parameter is
                required.
            
            file_list (List[str], List[Path], str, Path): 
                The files to read in. Absolute paths are recommended, but not technically
                necessary. This can be a single string for a file, or a list of strings to read
                in multiple files. This parameter is required.

            n_parallel (int): 
                Number of data files to read in parallel using multiprocessing. Default value 
                is 1. Adjust according to your computer's available resources. This parameter 
                is optional.
            
            first_record (bool): 
                Only read in the first record in each file. This is the same as the first_frame
                parameter in the themis-imager-readfile and trex-imager-readfile libraries, and
                is a read optimization if you only need one image per minute, as opposed to the
                full temporal resolution of data (e.g., 3sec cadence). This parameter is optional.
            
            no_metadata (bool): 
                Skip reading of metadata. This is a minor optimization if the metadata is not needed.
                Default is `False`. This parameter is optional.

            start_time (datetime.datetime): 
                The start timestamp to read data onwards from (inclusive). This can be utilized to 
                read a portion of a data file, and could be paired with the `end_time` parameter. 
                This tends to be utilized for datasets that are hour or day-long files where it is 
                possible to only read a smaller bit of that file. An example is the TREx Spectrograph 
                processed data (1 hour files), or the riometer data (1 day files). If not supplied, 
                it will assume the start time is the timestamp of the first record in the first 
                file supplied (ie. beginning of the supplied data). This parameter is optional.

            end_time (datetime.datetime): 
                The end timestamp to read data up to (inclusive). This can be utilized to read a 
                portion of a data file, and could be paired with the `start_time` parameter. This 
                tends to be utilized for datasets that are hour or day-long files where it is possible 
                to only read a smaller bit of that file. An example is the TREx Spectrograph processed 
                data (1 hour files), or the riometer data (1 day files). If not supplied, it will
                it will assume the end time is the timestamp of the last record in the last file
                supplied (ie. end of the supplied data). This parameter is optional.

            quiet (bool): 
                Do not print out errors while reading data files, if any are encountered. Any files
                that encounter errors will be, as usual, accessible via the `problematic_files` 
                attribute of the returned `Data` object. This parameter is optional.
        
        Returns:
            A [`Data`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.Data) 
            object containing the data read in, among other values.
        
        Raises:
            pyaurorax.exceptions.AuroraXUnsupportedReadError: an unsupported dataset was used when
                trying to read files.
            pyaurorax.exceptions.AuroraXError: a generic read error was encountered

        Notes:
        ---------
        For users who are familiar with the themis-imager-readfile and trex-imager-readfile
        libraries, the read function provides a near-identical usage. Further improvements have 
        been integrated, and those libraries are anticipated to be deprecated at some point in the
        future.
        """
        # NOTE: we do not wrap the exceptions here, instead we pass the call along
        # to the ReadManager object since the method and exception catching is
        # implemented there. No need to duplicate the exception handling logic.
        return self.__readers.read(
            dataset,
            file_list,
            n_parallel=n_parallel,
            first_record=first_record,
            no_metadata=no_metadata,
            start_time=start_time,
            end_time=end_time,
            quiet=quiet,
        )

    def download_best_skymap(
        self,
        dataset_name: str,
        site_uid: str,
        timestamp: datetime.datetime,
        timeout: Optional[int] = None,
        overwrite: bool = False,
    ) -> FileDownloadResult:
        """
        Download the skymap file that best matches the parameters supplied.

        Args:
            dataset_name (str): 
                Name of the dataset to download data for. Use the `list_datasets()` function
                to get the possible values for this parameter. One example is "THEMIS_ASI_SKYMAP_IDLSAV". 
                Note that dataset names are case sensitive. This parameter is required.

            site_uid (str): 
                The site UID to evaluate.

            timestamp (datetime.datetime): 
                The timestamp to use for deciding the best skymap, expected to be in UTC. Any timezone 
                data will be ignored. This parameter is required.

            timeout (int): 
                Represents how many seconds to wait for the API to send data before giving up. The 
                default is 10 seconds, or the `api_timeout` value in the super class' `pyaurorax.PyAuroraX`
                object. This parameter is optional.

        Returns:
            A [`FileDownloadResult`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.FileDownloadResult) 
            object containing details about what data files were downloaded.

        Raises:
            ValueError: issue with supplied timestamp
            pyaurorax.exceptions.AuroraXAPIError: an API error was encountered        
        """
        # get list of all skymap urls for the dataset and site
        start_dt = datetime.datetime(2000, 1, 1)
        end_dt = datetime.datetime.now() + datetime.timedelta(days=5)
        file_listing_obj = self.get_urls(dataset_name, start_dt, end_dt, site_uid=site_uid, timeout=timeout)

        # filter down and find the best skymap for the timestamp supplied
        best_skymap_filename = None
        for url in file_listing_obj.urls:
            # extract start date for this skymap
            url_short = url.replace(file_listing_obj.path_prefix + "/", "")

            # parse filename into several values
            filename_split = os.path.basename(url_short).split('_')
            filename_times_split = filename_split[3].split('-')
            valid_interval_start_dt = datetime.datetime.strptime(filename_times_split[0], "%Y%m%d")

            # check start time
            if (timestamp >= valid_interval_start_dt):
                # valid
                #
                # NOTE: this works because of the order that the list is in already
                best_skymap_filename = url

        # check if we found a skymap
        if (best_skymap_filename is None):
            raise ValueError("Unable to determine a skymap recommendation")

        # set the filename
        file_listing_obj.urls = [best_skymap_filename]
        download_obj = self.download_using_urls(
            file_listing_obj,
            progress_bar_disable=True,
            overwrite=overwrite,
            timeout=timeout,
        )

        # return
        return download_obj

    def download_best_flatfield_calibration(
        self,
        dataset_name: str,
        device_uid: str,
        timestamp: datetime.datetime,
        timeout: Optional[int] = None,
        overwrite: bool = False,
    ) -> FileDownloadResult:
        """
        Download the flatfield calibration file that best matches the parameters supplied.

        Args:
            dataset_name (str): 
                Name of the dataset to download data for. Use the `list_datasets()` function
                to get the possible values for this parameter. One example is "THEMIS_ASI_SKYMAP_IDLSAV". 
                Note that dataset names are case sensitive. This parameter is required.

            device_uid (str): 
                The device UID to evaluate.

            timestamp (datetime.datetime): 
                The timestamp to use for deciding the best skymap, expected to be in UTC. Any timezone 
                data will be ignored. This parameter is required.

            timeout (int): 
                Represents how many seconds to wait for the API to send data before giving up. The 
                default is 10 seconds, or the `api_timeout` value in the super class' `pyaurorax.PyAuroraX`
                object. This parameter is optional.

        Returns:
            A [`FileDownloadResult`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.FileDownloadResult) 
            object containing details about what data files were downloaded.

        Raises:
            ValueError: issue with supplied timestamp
            pyaurorax.exceptions.AuroraXAPIError: an API error was encountered        
        """
        # get list of all flatfield urls for the dataset and device
        start_dt = datetime.datetime(2000, 1, 1)
        end_dt = datetime.datetime.now() + datetime.timedelta(days=5)
        file_listing_obj = self.get_urls(dataset_name, start_dt, end_dt, device_uid=device_uid, timeout=timeout)

        # filter down and find the best skymap for the timestamp supplied
        best_cal_filename = None
        for url in file_listing_obj.urls:
            # extract start date for this skymap
            url_short = url.replace(file_listing_obj.path_prefix + "/", "")

            # parse filename into several values
            filename_split = os.path.basename(url_short).split('_')
            filename_times_split = filename_split[3].split('-')
            valid_interval_start_dt = datetime.datetime.strptime(filename_times_split[0], "%Y%m%d")

            # check start time
            if (timestamp >= valid_interval_start_dt):
                # valid
                #
                # NOTE: this works because of the order that the list is in already
                best_cal_filename = url

        # check if we found a skymap
        if (best_cal_filename is None):
            raise ValueError("Unable to determine a flatfield calibration recommendation")

        # set the filename
        file_listing_obj.urls = [best_cal_filename]
        download_obj = self.download_using_urls(
            file_listing_obj,
            progress_bar_disable=True,
            overwrite=overwrite,
            timeout=timeout,
        )

        # return
        return download_obj

    def download_best_rayleighs_calibration(
        self,
        dataset_name: str,
        device_uid: str,
        timestamp: datetime.datetime,
        timeout: Optional[int] = None,
        overwrite: bool = False,
    ) -> FileDownloadResult:
        """
        Download the Rayleighs calibration file that best matches the parameters supplied.

        Args:
            dataset_name (str): 
                Name of the dataset to download data for. Use the `list_datasets()` function
                to get the possible values for this parameter. One example is "REGO_CALIBRATION_RAYLEIGHS_IDLSAV". 
                Note that dataset names are case sensitive. This parameter is required.

            device_uid (str): 
                The device UID to evaluate.

            timestamp (datetime.datetime): 
                The timestamp to use for deciding the best calibration file, expected to be in 
                UTC. Any timezone data will be ignored. This parameter is required.

            timeout (int): 
                Represents how many seconds to wait for the API to send data before giving up. The 
                default is 10 seconds, or the `api_timeout` value in the super class' `pyaurorax.PyAuroraX`
                object. This parameter is optional.

        Returns:
            A [`FileDownloadResult`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.FileDownloadResult) 
            object containing details about what data files were downloaded.

        Raises:
            ValueError: issue with supplied timestamp
            pyaurorax.exceptions.AuroraXAPIError: an API error was encountered        
        """
        # get list of all rayleighs urls for the dataset and device
        start_dt = datetime.datetime(2000, 1, 1)
        end_dt = datetime.datetime.now() + datetime.timedelta(days=5)
        file_listing_obj = self.get_urls(dataset_name, start_dt, end_dt, device_uid=device_uid, timeout=timeout)

        # filter down and find the best skymap for the timestamp supplied
        best_cal_filename = None
        for url in file_listing_obj.urls:
            # extract start date for this skymap
            url_short = url.replace(file_listing_obj.path_prefix + "/", "")

            # parse filename into several values
            filename_split = os.path.basename(url_short).split('_')
            filename_times_split = filename_split[3].split('-')
            valid_interval_start_dt = datetime.datetime.strptime(filename_times_split[0], "%Y%m%d")

            # check start time
            if (timestamp >= valid_interval_start_dt):
                # valid
                #
                # NOTE: this works because of the order that the list is in already
                best_cal_filename = url

        # check if we found a skymap
        if (best_cal_filename is None):
            raise ValueError("Unable to determine a Rayleighs calibration recommendation")

        # set the filename
        file_listing_obj.urls = [best_cal_filename]
        download_obj = self.download_using_urls(
            file_listing_obj,
            progress_bar_disable=True,
            overwrite=overwrite,
            timeout=timeout,
        )

        # return
        return download_obj
