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

import datetime
from pathlib import Path
from typing import TYPE_CHECKING, List, Union, Optional
from pyucalgarysrs.data import Dataset, Data
from pyucalgarysrs.exceptions import SRSError, SRSUnsupportedReadError
from ....exceptions import AuroraXError, AuroraXUnsupportedReadError
if TYPE_CHECKING:
    from ....pyaurorax import PyAuroraX


class ReadManager:
    """
    The UCalgaryManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    def __init__(self, aurorax_obj):
        self.__aurorax_obj: PyAuroraX = aurorax_obj

    def list_supported_datasets(self) -> List[str]:
        """
        List the datasets which have file reading capabilities supported.

        Returns:
            A list of the dataset names with file reading support.
        """
        return self.__aurorax_obj.srs_obj.data.readers.list_supported_datasets()

    def is_supported(self, dataset_name: str) -> bool:
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
        return self.__aurorax_obj.srs_obj.data.readers.is_supported(dataset_name)

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

            no_metadata (bool): 
                Skip reading of metadata. This is a minor optimization if the metadata is not needed.
                Default is `False`. This parameter is optional.
            
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
        try:
            return self.__aurorax_obj.srs_obj.data.readers.read(
                dataset,
                file_list,
                n_parallel=n_parallel,
                first_record=first_record,
                no_metadata=no_metadata,
                start_time=start_time,
                end_time=end_time,
                quiet=quiet,
            )
        except SRSUnsupportedReadError as e:
            raise AuroraXUnsupportedReadError(e) from e
        except SRSError as e:
            raise AuroraXError(e) from e

    def read_themis(self,
                    file_list: Union[List[str], List[Path], str, Path],
                    n_parallel: int = 1,
                    first_record: bool = False,
                    no_metadata: bool = False,
                    start_time: Optional[datetime.datetime] = None,
                    end_time: Optional[datetime.datetime] = None,
                    quiet: bool = False,
                    dataset: Optional[Dataset] = None) -> Data:
        """
        Read in THEMIS ASI raw data (stream0 full.pgm* files).

        Args:
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
            
            quiet (bool): 
                Do not print out errors while reading data files, if any are encountered. Any files
                that encounter errors will be, as usual, accessible via the `problematic_files` 
                attribute of the returned `Data` object. This parameter is optional.

            dataset (Dataset): 
                The dataset object for which the files are associated with. This parameter is
                optional.

        Returns:
            A [`Data`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.Data) 
            object containing the data read in, among other values.
        
        Raises:
            pyaurorax.exceptions.AuroraXError: a generic read error was encountered
        """
        try:
            return self.__aurorax_obj.srs_obj.data.readers.read_themis(
                file_list,
                n_parallel=n_parallel,
                first_record=first_record,
                no_metadata=no_metadata,
                start_time=start_time,
                end_time=end_time,
                quiet=quiet,
                dataset=dataset,
            )
        except SRSError as e:
            raise AuroraXError(e) from e

    def read_rego(self,
                  file_list: Union[List[str], List[Path], str, Path],
                  n_parallel: int = 1,
                  first_record: bool = False,
                  no_metadata: bool = False,
                  start_time: Optional[datetime.datetime] = None,
                  end_time: Optional[datetime.datetime] = None,
                  quiet: bool = False,
                  dataset: Optional[Dataset] = None) -> Data:
        """
        Read in REGO raw data (stream0 pgm* files).

        Args:
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

            dataset (Dataset): 
                The dataset object for which the files are associated with. This parameter is
                optional.

        Returns:
            A [`Data`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.Data) 
            object containing the data read in, among other values.
        
        Raises:
            pyaurorax.exceptions.AuroraXError: a generic read error was encountered
        """
        return self.__aurorax_obj.srs_obj.data.readers.read_rego(
            file_list,
            n_parallel=n_parallel,
            first_record=first_record,
            no_metadata=no_metadata,
            start_time=start_time,
            end_time=end_time,
            quiet=quiet,
            dataset=dataset,
        )

    def read_trex_nir(self,
                      file_list: Union[List[str], List[Path], str, Path],
                      n_parallel: int = 1,
                      first_record: bool = False,
                      no_metadata: bool = False,
                      start_time: Optional[datetime.datetime] = None,
                      end_time: Optional[datetime.datetime] = None,
                      quiet: bool = False,
                      dataset: Optional[Dataset] = None) -> Data:
        """
        Read in TREx near-infrared (NIR) raw data (stream0 pgm* files).

        Args:
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

            dataset (Dataset): 
                The dataset object for which the files are associated with. This parameter is
                optional.

        Returns:
            A [`Data`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.Data) 
            object containing the data read in, among other values.
        
        Raises:
            pyaurorax.exceptions.AuroraXError: a generic read error was encountered
        """
        return self.__aurorax_obj.srs_obj.data.readers.read_trex_nir(
            file_list,
            n_parallel=n_parallel,
            first_record=first_record,
            no_metadata=no_metadata,
            start_time=start_time,
            end_time=end_time,
            quiet=quiet,
            dataset=dataset,
        )

    def read_trex_blue(self,
                       file_list: Union[List[str], List[Path], str, Path],
                       n_parallel: int = 1,
                       first_record: bool = False,
                       no_metadata: bool = False,
                       start_time: Optional[datetime.datetime] = None,
                       end_time: Optional[datetime.datetime] = None,
                       quiet: bool = False,
                       dataset: Optional[Dataset] = None) -> Data:
        """
        Read in TREx Blueline raw data (stream0 pgm* files).

        Args:
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
                attribute of the returned `Data` object. This parameter
                is optional.

            dataset (Dataset): 
                The dataset object for which the files are associated with. This parameter is
                optional.

        Returns:
            A [`Data`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.Data) 
            object containing the data read in, among other values.
        
        Raises:
            pyaurorax.exceptions.AuroraXError: a generic read error was encountered
        """
        return self.__aurorax_obj.srs_obj.data.readers.read_trex_blue(
            file_list,
            n_parallel=n_parallel,
            first_record=first_record,
            no_metadata=no_metadata,
            start_time=start_time,
            end_time=end_time,
            quiet=quiet,
            dataset=dataset,
        )

    def read_trex_rgb(self,
                      file_list: Union[List[str], List[Path], str, Path],
                      n_parallel: int = 1,
                      first_record: bool = False,
                      no_metadata: bool = False,
                      start_time: Optional[datetime.datetime] = None,
                      end_time: Optional[datetime.datetime] = None,
                      quiet: bool = False,
                      dataset: Optional[Dataset] = None) -> Data:
        """
        Read in TREx RGB raw data (stream0 h5, stream0.burst png.tar, unstable stream0 and 
        stream0.colour pgm* and png*).

        Args:
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

            dataset (Dataset): 
                The dataset object for which the files are associated with. This parameter is
                optional.

        Returns:
            A [`Data`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.Data) 
            object containing the data read in, among other values.
        
        Raises:
            pyaurorax.exceptions.AuroraXError: a generic read error was encountered
        """
        return self.__aurorax_obj.srs_obj.data.readers.read_trex_rgb(
            file_list,
            n_parallel=n_parallel,
            first_record=first_record,
            no_metadata=no_metadata,
            start_time=start_time,
            end_time=end_time,
            quiet=quiet,
            dataset=dataset,
        )

    def read_trex_spectrograph(self,
                               file_list: Union[List[str], List[Path], str, Path],
                               n_parallel: int = 1,
                               first_record: bool = False,
                               no_metadata: bool = False,
                               start_time: Optional[datetime.datetime] = None,
                               end_time: Optional[datetime.datetime] = None,
                               quiet: bool = False,
                               dataset: Optional[Dataset] = None) -> Data:
        """
        Read in TREx Spectrograph raw data (stream0 pgm* files).

        Args:
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

            dataset (Dataset): 
                The dataset object for which the files are associated with. This parameter is
                optional.

        Returns:
            A [`Data`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.Data) 
            object containing the data read in, among other values.
        
        Raises:
            pyaurorax.exceptions.AuroraXError: a generic read error was encountered
        """
        return self.__aurorax_obj.srs_obj.data.readers.read_trex_spectrograph(
            file_list,
            n_parallel=n_parallel,
            first_record=first_record,
            no_metadata=no_metadata,
            start_time=start_time,
            end_time=end_time,
            quiet=quiet,
            dataset=dataset,
        )

    def read_skymap(
        self,
        file_list: Union[List[str], List[Path], str, Path],
        n_parallel: int = 1,
        quiet: bool = False,
        dataset: Optional[Dataset] = None,
    ) -> Data:
        """
        Read in UCalgary skymap files.

        Args:
            file_list (List[str], List[Path], str, Path): 
                The files to read in. Absolute paths are recommended, but not technically
                necessary. This can be a single string for a file, or a list of strings to read
                in multiple files. This parameter is required.

            n_parallel (int): 
                Number of data files to read in parallel using multiprocessing. Default value 
                is 1. Adjust according to your computer's available resources. This parameter 
                is optional.
                                    
            quiet (bool): 
                Do not print out errors while reading skymap files, if any are encountered. Any 
                files that encounter errors will be, as usual, accessible via the `problematic_files` 
                attribute of the returned `Skymap` object. This parameter is optional.

            dataset (Dataset): 
                The dataset object for which the files are associated with. This parameter is
                optional.

        Returns:
            A [`Data`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.Data) 
            object containing the data read in, among other values.
        
        Raises:
            pyaurorax.exceptions.AuroraXError: a generic read error was encountered        
        """
        return self.__aurorax_obj.srs_obj.data.readers.read_skymap(
            file_list,
            n_parallel=n_parallel,
            quiet=quiet,
            dataset=dataset,
        )

    def read_calibration(
        self,
        file_list: Union[List[str], List[Path], str, Path],
        n_parallel: int = 1,
        quiet: bool = False,
        dataset: Optional[Dataset] = None,
    ) -> Data:
        """
        Read in UCalgary calibration files.

        Args:
            file_list (List[str], List[Path], str, Path): 
                The files to read in. Absolute paths are recommended, but not technically
                necessary. This can be a single string for a file, or a list of strings to read
                in multiple files. This parameter is required.

            n_parallel (int): 
                Number of data files to read in parallel using multiprocessing. Default value 
                is 1. Adjust according to your computer's available resources. This parameter 
                is optional.

            quiet (bool): 
                Do not print out errors while reading calibration files, if any are encountered. 
                Any files that encounter errors will be, as usual, accessible via the `problematic_files` 
                attribute of the returned `Calibration` object. This parameter is optional.

            dataset (Dataset): 
                The dataset object for which the files are associated with. This parameter is
                optional.

        Returns:
            A [`Data`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.Data) 
            object containing the data read in, among other values.
        
        Raises:
            pyaurorax.exceptions.AuroraXError: a generic read error was encountered        
        """
        return self.__aurorax_obj.srs_obj.data.readers.read_calibration(
            file_list,
            n_parallel=n_parallel,
            quiet=quiet,
            dataset=dataset,
        )

    def read_grid(self,
                  file_list: Union[List[str], List[Path], str, Path],
                  n_parallel: int = 1,
                  first_record: bool = False,
                  no_metadata: bool = False,
                  start_time: Optional[datetime.datetime] = None,
                  end_time: Optional[datetime.datetime] = None,
                  quiet: bool = False,
                  dataset: Optional[Dataset] = None) -> Data:
        """
        Read in grid files.

        Args:
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
                attribute of the returned `pyucalgarysrs.data.classes.Data` object. This parameter
                is optional.

            dataset (pyucalgarysrs.data.classes.Dataset): 
                The dataset object for which the files are associated with. This parameter is
                optional.

        Returns:
            A `pyucalgarysrs.data.classes.Data` object containing the data read in, among other
            values.
        
        Raises:
            pyucalgarysrs.exceptions.SRSError: a generic read error was encountered
        """
        return self.__aurorax_obj.srs_obj.data.readers.read_grid(
            file_list,
            n_parallel=n_parallel,
            first_record=first_record,
            no_metadata=no_metadata,
            start_time=start_time,
            end_time=end_time,
            quiet=quiet,
            dataset=dataset,
        )
