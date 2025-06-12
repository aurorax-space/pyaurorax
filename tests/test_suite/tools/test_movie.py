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
import shutil
import matplotlib.pyplot as plt


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


@pytest.mark.tools
def test_corrupt_videofile(at, themis_single_file):

    # First, create a test movie with 1 minute of themis data
    img = themis_single_file.data
    output_filename = "/tmp/pyaurorax_testing_%s.mp4" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    image_filenames = []

    # Plot each image, save it to a temporary dir, then append filename to list
    for i in range(0, img.shape[-1]):
        _, _ = at.display(img[:, :, i], cmap="gray", returnfig=True)
        filename = "/tmp/pyaurorax_testing_dir/%s_themis.png" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        plt.savefig(filename, bbox_inches="tight")
        plt.close()
        image_filenames.append(filename)

    # Create the movie
    at.movie(image_filenames, output_filename, n_parallel=5)

    # Check that file size is > 5 kb, indicating it was not corrupted
    size_kib = os.stat(output_filename).st_size / 1024.0
    assert size_kib > 5

    # Delete temporary files from system
    shutil.rmtree("/tmp/pyaurorax_testing_dir")
