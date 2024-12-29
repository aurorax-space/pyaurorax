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
The PyAuroraX package provides a way to interact with the [AuroraX Data Platform](https://aurorax.space), 
facilitating programmatic usage of AuroraX's search engine and data analysis tools.

For an overview of usage and examples, visit the
[AuroraX Developer Zone website](https://docs.aurorax.space/code/overview), or explore the examples contained
in the Github repository [here](https://github.com/aurorax-space/pyaurorax/tree/main/examples).

Installation:
```console
pip install pyaurorax
```

Basic usage:
```python
import pyaurorax
aurorax = pyaurorax.PyAuroraX()
```
"""

# versioning info
__version__ = "1.8.0"

# documentation excludes
__pdoc__ = {"cli": False, "pyaurorax": False}
__all__ = ["PyAuroraX"]

# pull in top level class
from .pyaurorax import PyAuroraX

# pull in top-level submodules
#
# NOTE: we do this only so that we can access classes within the
# submodules, like `pyaurorax.search.EphemerisSearch`. Without this,
# they are selectively addressable, such as within ipython, but not
# vscode. Currently, this is ONLY included for VSCode's sake. Will
# take more testing to explore other use-cases.
from . import search
from . import data
from . import models

# pull in exceptions
from .exceptions import (
    AuroraXError,
    AuroraXInitializationError,
    AuroraXPurgeError,
    AuroraXAPIError,
    AuroraXNotFoundError,
    AuroraXDuplicateError,
    AuroraXUnauthorizedError,
    AuroraXConflictError,
    AuroraXDataRetrievalError,
    AuroraXSearchError,
    AuroraXUploadError,
    AuroraXMaintenanceError,
    AuroraXUnsupportedReadError,
    AuroraXDownloadError,
)
