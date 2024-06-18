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

import click

from .availability import commands as availability_commands
from .conjunctions import commands as conjunctions_commands
from .data_products import commands as data_products_commands
from .ephemeris import commands as ephemeris_commands
from .sources import commands as sources_commands
from .util import commands as util_commands


@click.group("search", help="Search engine commands")
def search_group():
    pass


search_group.add_command(availability_commands.availability_group)
search_group.add_command(conjunctions_commands.conjunctions_group)
search_group.add_command(data_products_commands.data_products_group)
search_group.add_command(ephemeris_commands.ephemeris_group)
search_group.add_command(sources_commands.sources_group)
search_group.add_command(util_commands.utility_group)
