#! /usr/bin/env python
#
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
This script builds the test data that the test suite reads from disk, into
tests/test_data/data/ucalgary/read. It is what 'make get-test-data' runs.

Every file the test suite refers to still exists in the open data platform, and
is downloaded verbatim. The manifest is IMAGER_FILES, GRID_FILES, and the lists
below them.

Usage:

  python3 tools/build_test_data.py [--clean]

Files that are already in place are left alone, so an interrupted build only fetches
what it missed. Pass --tarball to also package the tree up, for hosting it somewhere
or handing it to someone.
"""

import argparse
import glob
import os
import shutil
import subprocess  # nosec
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

# globals
DATA_TREE = "https://data.phys.ucalgary.ca/sort_by_project"
TARBALL_FILENAME = "pyaurorax_test_data.tar.gz"
DEFAULT_DATA_DIR = "%s/tests/test_data" % (os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
READ_SUBDIR = "data/ucalgary/read"

# files that are downloaded from the open data platform as-is, grouped by where they live in the data tree
# raw imager data: <data tree>/<path>/<yyyy>/<mm>/<dd>/<site>_<device>/ut<hh>/<filename>
IMAGER_FILES = {
    "read_rego": ("GO-Canada/REGO/stream0", ["20180403_0600_gill_rego-652_6300.pgm.gz"]),
    "read_smile": ("SMILE/asi/l0/raw", ["20250315_0600_atha_smile-31_rgb-full.h5"]),
    "read_themis": ("THEMIS/asi/stream0", ["20140310_0600_gill_themis19_full.pgm.gz"]),
    "read_trex_blue": ("TREx/blueline/stream0", ["20220308_0600_gill_blue-814_full.pgm.gz"]),
    "read_trex_nir": ("TREx/NIR/stream0", ["20220307_0600_gill_nir-216_8446.pgm.gz"]),
    "read_trex_rgb": ("TREx/RGB/stream0", ["20210205_0600_gill_rgb-04_full.h5"]),
    "read_trex_spectrograph": ("TREx/spectrograph/l0/raw", ["20230503_0600_luck_spect-02_spectra.pgm.gz"]),
}

# grid data: <data tree>/<path>/grid_files/MOSv001/<yyyy>/<mm>/<dd>/ut<hh>/<filename>
GRID_FILES = {
    "read_grid": ("THEMIS/asi", ["20230324_0600_110km_MOSv001_grid_themis-asi.h5"]),
}

# REGO calibration data: <data tree>/<path>/<filename>
REGO_CALIBRATION_FILES_PATH = "GO-Canada/REGO/calibration"
REGO_CALIBRATION_FILES = [
    "REGO_Rayleighs_15651_20210908-+_v02.sav",
]

# skymaps: <data tree>/<path>/<filename>
SKYMAP_FILES = {
    "themis_skymap_atha_20230115-+_v02.sav": "THEMIS/asi/skymaps/atha/atha_20230115",
}


def parse_filename(filename):
    """
    Pull the date, hour, site UID and device UID out of a data filename, which is of the
    form <yyyymmdd>_<hhmm>_<site>_<device>_...
    """
    filename_split = filename.split('_')
    date_str = filename_split[0]
    return {
        "year": date_str[0:4],
        "month": date_str[4:6],
        "day": date_str[6:8],
        "hour": filename_split[1][0:2],
        "site_uid": filename_split[2],
        "device_uid": filename_split[3],
    }


def build_archive_manifest():
    """
    Work out the URL of every file that gets downloaded from the open data platform,
    returned as a dictionary of destination path in the test data tree --> URL.
    """
    manifest = {}

    # raw imager data
    for dest_dir, (path, filenames) in IMAGER_FILES.items():
        for filename in filenames:
            f = parse_filename(filename)
            manifest["%s/%s" % (dest_dir, filename)] = "%s/%s/%s/%s/%s/%s_%s/ut%s/%s" % (DATA_TREE, path, f["year"], f["month"], f["day"],
                                                                                         f["site_uid"], f["device_uid"], f["hour"], filename)

    # grid data
    for dest_dir, (path, filenames) in GRID_FILES.items():
        for filename in filenames:
            f = parse_filename(filename)
            manifest["%s/%s" % (dest_dir, filename)] = "%s/%s/grid_files/MOSv001/%s/%s/%s/ut%s/%s" % (DATA_TREE, path, f["year"], f["month"],
                                                                                                      f["day"], f["hour"], filename)

    # REGO calibration data
    for filename in REGO_CALIBRATION_FILES:
        manifest["read_calibration/%s" % (filename)] = "%s/%s/%s" % (DATA_TREE, REGO_CALIBRATION_FILES_PATH, filename)

    # skymaps
    for filename, path in SKYMAP_FILES.items():
        manifest["read_skymap/%s" % (filename)] = "%s/%s/%s" % (DATA_TREE, path, filename)

    return manifest


def download_file(url, output_filename):
    if (os.path.exists(output_filename) and os.path.getsize(output_filename) > 0):
        return 0
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "pyaurorax test data builder"})
    with urllib.request.urlopen(req, timeout=300) as r:  # nosec
        content_type = r.headers.get("Content-Type", "")
        data = r.read()

    # the data server redirects to the home page for files that don't exist, so a
    # page of HTML means we asked for something that isn't there
    if ("text/html" in content_type.lower()):
        raise IOError("Received a page of HTML instead of a file, the URL is likely no longer valid: %s" % (url))
    with open(output_filename, "wb") as fp:
        fp.write(data)
    return len(data)


def download_archive_files(read_dir, n_parallel):

    def do_download(item):
        dest, url = item
        try:
            return (dest, download_file(url, "%s/%s" % (read_dir, dest)), None)
        except Exception as e:
            return (dest, 0, str(e))

    archive_manifest = build_archive_manifest()
    print("[downloading] %d files from the open data platform" % (len(archive_manifest)))
    with ThreadPoolExecutor(max_workers=n_parallel) as executor:
        results = list(executor.map(do_download, sorted(archive_manifest.items())))
    failures = [r for r in results if r[2] is not None]
    for f in failures:
        print("  failed: %s (%s)" % (f[0], f[2]))
    if (len(failures) > 0):
        raise IOError("Failed to download %d file(s)" % (len(failures)))
    print("[downloading] retrieved %.1f MB" % (sum(r[1] for r in results) / 1e6))


def set_permissions(read_dir):
    for root, _, files in os.walk(read_dir):
        for f in files:
            os.chmod(os.path.join(root, f), 0o644)


def create_tarball(data_dir):
    tarball_filename = "%s/%s" % (os.path.dirname(data_dir), TARBALL_FILENAME)
    print("[packaging] creating %s" % (tarball_filename))
    if (os.path.exists(tarball_filename)):
        os.remove(tarball_filename)
    subprocess.run(  # nosec
        ["tar", "-C", data_dir, "-czf", tarball_filename, READ_SUBDIR.split('/')[0]],
        check=True,
    )
    return tarball_filename


def clean_read_dir(read_dir):
    print("[cleaning] removing the existing test data")
    for entry in sorted(glob.glob("%s/read_*" % (read_dir))):
        shutil.rmtree(entry, ignore_errors=True)


def main():
    # args
    parser = argparse.ArgumentParser(description="Build the test data that the test suite reads")
    parser.add_argument("--data-dir", default=DEFAULT_DATA_DIR, help="Directory to build the test data tree in (default: %s)" % (DEFAULT_DATA_DIR))
    parser.add_argument("--n-parallel", type=int, default=5, help="Number of parallel downloads (default: 5)")
    parser.add_argument("--clean", action="store_true", help="Remove the existing test data before building")
    parser.add_argument("--tarball", action="store_true", help="Also package the tree up as %s, beside the data directory" % (TARBALL_FILENAME))
    args = parser.parse_args()

    # set up paths
    data_dir = os.path.abspath(os.path.expanduser(args.data_dir))
    read_dir = "%s/%s" % (data_dir, READ_SUBDIR)
    os.makedirs(read_dir, exist_ok=True)

    # build it
    #
    # NOTE: files that are already there are left alone, so an interrupted build only has
    # to fetch what it didn't get to the first time
    if (args.clean is True):
        clean_read_dir(read_dir)
    download_archive_files(read_dir, args.n_parallel)
    set_permissions(read_dir)
    print("\nDone, the test data is in %s" % (read_dir))

    # package it up, if we were asked to
    if (args.tarball is True):
        tarball_filename = create_tarball(data_dir)
        print("Packaged %s (%.1f MB)" % (tarball_filename, os.path.getsize(tarball_filename) / 1e6))
    return 0


if (__name__ == "__main__"):
    sys.exit(main())
