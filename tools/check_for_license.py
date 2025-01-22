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
This script will scan all .py files in the codebase and check that the 
license text exists at the top of each.
"""

import argparse
import sys
import os
from termcolor import colored

# globals
return_success = True


def process_file(f, license_file_lines):
    # init
    global return_success

    # process the file
    try:
        # open
        fp = open(f, 'r')

        # read first line, check if the license is starting there
        line = fp.readline()
        if (line[0:2] == "#!"):
            line = fp.readline()
            line = fp.readline()
        if (line.strip() == license_file_lines[0].strip()):
            # license exists, check that the whole thing matches.
            fp.seek(0)
            success = True
            for license_line in license_file_lines:
                file_line = fp.readline()
                if (file_line[0:2] == "#!"):
                    file_line = fp.readline()
                    file_line = fp.readline()
                if (file_line.strip() != license_line.strip()):
                    success = False
                    break

            # check success
            if (success is False):
                print(colored("Error: license file line mismatch: %s" % (f), "red"))
                return_success = False
        else:
            # license does not exist
            print(colored("Error: license does not exist: %s" % (f), "red"))
            return_success = False

        # close
        fp.close()
    except IOError:
        print(colored("Error processing file: %s" % (f), "red"))
        return_success = False


def main():
    # args
    parser = argparse.ArgumentParser(description="Check source code files to ensure license exists at top of every file")
    _ = parser.parse_args()

    # read in license file
    license_file_data = ""
    try:
        fp = open("%s/../LICENSE" % (os.path.dirname(os.path.realpath(__file__))))
        for line in fp:
            if (line.strip() == ''):
                license_file_data += '#\n'
            else:
                license_file_data += "# " + line
        fp.close()
    except IOError as e:
        print("Error reading in LICENSE file: %s" % (str(e)))
        return 1
    license_file_lines = license_file_data.split('\n')

    # set up paths to search
    paths_to_search = [
        "%s/../pyaurorax" % (os.path.dirname(os.path.realpath(__file__))),
        "%s/../tests" % (os.path.dirname(os.path.realpath(__file__))),
        "%s/../tools" % (os.path.dirname(os.path.realpath(__file__))),
    ]

    # for each path
    for path_to_search in paths_to_search:
        # search for files
        file_list = []
        for dirpath, _, filenames in os.walk(path_to_search):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if (os.path.isfile(filepath) is True and filepath[-3:] == ".py" and "__pycache__" not in filepath):
                    file_list.append(filepath)

        # process files
        for f in file_list:
            process_file(f, license_file_lines)

    # return
    if (return_success is False):
        return 1
    else:
        return 0


# -----------------
if (__name__ == "__main__"):
    sys.exit(main())
