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
Unique exception classes utilized by PyAuroraX. These exceptions can be used to help trap specific 
errors raised by this library.

Note that all exceptions are imported at the root level of the library. They
can be referenced using [`pyaurorax.AuroraXError`](exceptions.html#pyaurorax.exceptions.AuroraXError) 
or `pyaurorax.exceptions.AuroraXError`.
"""


class AuroraXError(Exception):

    def __init__(self, *args, **kwargs):
        super(AuroraXError, self).__init__(*args, **kwargs)  # pragma: no cover


class AuroraXInitializationError(AuroraXError):
    """
    Error occurred during library initialization
    """
    pass


class AuroraXPurgeError(AuroraXError):
    """
    Error occurred during purging of download or tar extraction working directory
    """
    pass


class AuroraXAPIError(AuroraXError):
    """
    Error occurred during an API call
    """
    pass


class AuroraXNotFoundError(AuroraXError):
    """
    The AuroraX record was not found
    """
    pass


class AuroraXDuplicateError(AuroraXError):
    """
    A duplicate record already exists
    """
    pass


class AuroraXUnauthorizedError(AuroraXError):
    """
    A privileged operation was attempted without authorization
    """
    pass


class AuroraXConflictError(AuroraXError):
    """
    A conflict occurred while modifying records
    """
    pass


class AuroraXDataRetrievalError(AuroraXError):
    """
    Error occurred while retrieving search data
    """
    pass


class AuroraXSearchError(AuroraXError):
    """
    An error occurred in the API while performing a search
    """
    pass


class AuroraXUploadError(AuroraXError):
    """
    Error occurred during upload operation
    """
    pass


class AuroraXMaintenanceError(AuroraXError):
    """
    AuroraX API is in maintenance mode, read-only tasks are only possible
    """
    pass


class AuroraXUnsupportedReadError(AuroraXError):
    """
    Unsupported dataset for read function

    NOTE: this is primarily a PyUCalgarySRS error
    """
    pass


class AuroraXDownloadError(AuroraXError):
    """
    Error occurred during downloading of data

    NOTE: this is primarily a PyUCalgarySRS error
    """
    pass
