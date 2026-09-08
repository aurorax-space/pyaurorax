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

import multiprocessing
import matplotlib as mpl
import matplotlib.pyplot as plt


def get_mp_context():
    """
    Return the multiprocessing context to use for process pools.

    We prefer 'forkserver' where it is available (Linux, macOS). Forking a
    multi-threaded process can deadlock the child, and Python 3.12+ emits a
    DeprecationWarning for it. Python 3.14 switches the Linux default to
    'forkserver', so this just adopts that behaviour early. On platforms
    without it (Windows), 'spawn' is already the default and we return None
    to use it.
    """
    if ("forkserver" in multiprocessing.get_all_start_methods()):
        return multiprocessing.get_context("forkserver")
    return None


def set_theme(theme):
    if (theme == "default"):
        mpl.rcParams.update(mpl.rcParamsDefault)
    elif (theme == "light"):
        plt.style.use("default")
    elif (theme == "dark"):
        plt.style.use("dark_background")
    else:
        plt.style.use(theme)
