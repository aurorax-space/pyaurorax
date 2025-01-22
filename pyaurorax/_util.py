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

import warnings


def show_warning(message: str, stacklevel: int = 1) -> None:
    """
    This is a helper method for within the library to ensure warnings are displayed. Jupyter notebooks
    within VSCode suppress warnings by default, so this way ensures that they are shown.

    NOTE: This is a private method only meant for use within the library.
    """
    warnings.simplefilter("always", UserWarning)
    warnings.warn(message, UserWarning, stacklevel=stacklevel)
    warnings.resetwarnings()
