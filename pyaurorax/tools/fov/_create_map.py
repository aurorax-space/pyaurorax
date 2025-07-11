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

from ..classes.fov import FOV


def create_map(cartopy_projection, fov_data):

    # Store the projection information and FOVData objects (if there is any) in an
    # FOV Object and return it
    if fov_data is not None:
        if isinstance(fov_data, list):
            return FOV(cartopy_projection=cartopy_projection, fov_data=fov_data)
        else:
            return FOV(cartopy_projection=cartopy_projection, fov_data=[fov_data])
    else:
        return FOV(cartopy_projection=cartopy_projection)
