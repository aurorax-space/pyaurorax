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
This script will insert the coverage report into the COVERAGE file at 
the root of the repository.
"""

import argparse
import sys
import os
import shutil
import subprocess
import traceback


def main():
    # args
    parser = argparse.ArgumentParser(description="Update the COVERAGE file with the latest report")
    _ = parser.parse_args()

    # retrieve coverage report
    try:
        p = subprocess.Popen(
            "cd %s/.. && coverage report" % (os.path.dirname(__file__)),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError:
        traceback.print_exc()
        return 1
    out, _ = p.communicate()

    # extract coverage report text from output
    coverage_report_text = out.decode().strip()

    # set filenames
    original_fname = "%s/../COVERAGE.md" % (os.path.dirname(__file__))
    new_fname = "%s/../COVERAGE.md.tmp" % (os.path.dirname(__file__))

    # write new COVERAGE file
    try:
        # open files
        fp_in = open(original_fname, 'r')
        fp_out = open(new_fname, 'w')

        # inject coverage lines
        reached_coverage_section = False
        written_new_coverage_text = False
        reached_first_coverage_code_mark = False
        for line in fp_in:
            if ("Current coverage report" in line):
                reached_coverage_section = True
                fp_out.write(line)
            elif (reached_coverage_section is True):
                if (written_new_coverage_text is True):
                    if (reached_first_coverage_code_mark is False):
                        if (line.strip() == "```"):
                            reached_first_coverage_code_mark = True
                    elif (reached_first_coverage_code_mark is True):
                        if (line.strip() == "```"):
                            reached_coverage_section = False
                else:
                    fp_out.write("\n```\n")
                    fp_out.write(coverage_report_text + "\n")
                    fp_out.write("```\n")
                    written_new_coverage_text = True
            else:
                fp_out.write(line)

        # close files
        fp_in.close()
        fp_out.close()

        # overwrite existing file with new one
        shutil.move(new_fname, original_fname)
    except Exception:
        traceback.print_exc()
        if (os.path.exists(new_fname)):
            os.remove(new_fname)
        return 1

    # return
    return 0


# -----------------
if (__name__ == "__main__"):
    sys.exit(main())
