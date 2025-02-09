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

import os
import pytest
import random
import string


@pytest.mark.tools
def test_simple(at, themis_movie_filenames):
    output_filename = "/tmp/pyaurorax_testing_%s.mp4" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    at.movie(themis_movie_filenames, output_filename)
    assert os.path.exists(output_filename)
    os.remove(output_filename)


@pytest.mark.tools
def test_nparallel(at, themis_movie_filenames):
    output_filename = "/tmp/pyaurorax_testing_%s.mp4" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    at.movie(themis_movie_filenames, output_filename, n_parallel=2)
    assert os.path.exists(output_filename)
    os.remove(output_filename)


@pytest.mark.tools
def test_simple_no_progress_bar(at, themis_movie_filenames):
    output_filename = "/tmp/pyaurorax_testing_%s.mp4" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    at.movie(themis_movie_filenames, output_filename, progress_bar_disable=True)
    assert os.path.exists(output_filename)
    os.remove(output_filename)


@pytest.mark.tools
def test_nparallel_no_progress_bar(at, themis_movie_filenames):
    output_filename = "/tmp/pyaurorax_testing_%s.mp4" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    at.movie(themis_movie_filenames, output_filename, n_parallel=2, progress_bar_disable=True)
    assert os.path.exists(output_filename)
    os.remove(output_filename)


@pytest.mark.tools
def test_no_filenames(at):
    output_filename = "/tmp/pyaurorax_testing_%s.mp4" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    with pytest.raises(IOError) as e_info:
        at.movie([], output_filename)
    assert "No images read in" in str(e_info)
    assert os.path.exists(output_filename) is False
