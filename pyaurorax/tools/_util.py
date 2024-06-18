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

import matplotlib as mpl
import matplotlib.pyplot as plt


def set_theme(theme: str) -> None:
    """
    A handy wrapper for setting the matplotlib global theme. Common choices are `light`, 
    `dark`, or `default`.

    Args:
        theme (str): 
            Theme name. Common choices are `light`, `dark`, or `default`. If default, then
            matplotlib theme settings will be fully reset to their defaults.

            Additional themes can be found on the 
            [matplotlib documentation](https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html)
    """
    if ("theme" == "default"):
        mpl.rcParams.update(mpl.rcParamsDefault)
    elif (theme == "light"):
        plt.style.use("default")
    elif (theme == "dark"):
        plt.style.use("dark_background")
    else:
        plt.style.use(theme)
