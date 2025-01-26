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
This program searches the codebase for docstrings that are note
complete or formatted properly.
"""

import os
import sys
import datetime
import argparse
import glob
import ast
from texttable import Texttable

# globals
root_path = ""


def check_docstring_format(filename):
    """
    Checks the functions and classes in a Python file for properly formatted docstrings.
    """
    # init
    issues = []

    # read file
    with open(filename, "r") as file:
        tree = ast.parse(file.read())

    # traverse the AST to find function and class definitions
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # check the docstring for the function
            issues.extend(check_function_docstring(node, filename))
        elif isinstance(node, ast.ClassDef):
            # check the docstring for the class
            issues.extend(check_class_docstring(node, filename))

    # return
    return issues


def check_function_docstring(node, filename):
    """
    Checks a function's docstring for properly formatted 'Args'.
    """
    # init
    issues = []
    filename_to_record = filename.replace(root_path + "/", '')

    # process file
    docstring = ast.get_docstring(node)
    if (docstring and "Args:" in docstring):
        # split the docstring into lines
        doc_lines = docstring.splitlines()

        # extract parameter names from the function definition
        param_names = [arg.arg for arg in node.args.args if arg.arg != "self"]

        # check for each parameter in the docstring
        for param in param_names:
            param_found = False
            for i, line in enumerate(doc_lines):
                if (line.strip().startswith(f"{param} (") or line.strip().startswith(f"{param}:")):
                    param_found = True

                    # check if type hints (brackets) are present
                    if not ("(" in line and ")" in line):
                        issues.append((filename_to_record, f"Function: {node.name}", f"Missing type brackets for parameter '{param}'"))

                    # check for space after colon
                    if not line.endswith(": "):
                        issues.append((filename_to_record, f"Function: {node.name}", f"Missing space after colon for parameter '{param}'"))

                        # Check if the next line starts with a capital letter
                    if i + 1 < len(doc_lines):
                        next_line = doc_lines[i + 1].strip()
                        if next_line and not next_line[0].isupper():
                            issues.append((
                                filename_to_record,
                                f"Function: {node.name}",
                                f"The description for parameter '{param}' must start with a capital letter.",
                            ))
                    break

            if not param_found:
                issues.append((filename_to_record, f"Function: {node.name}", f"Missing docstring description for parameter '{param}'"))

    # return
    return issues


def check_class_docstring(node, filename):
    """
    Checks a class's docstring for properly formatted 'Attributes'.
    """
    # init
    issues = []
    filename_to_record = filename.replace(root_path + "/", '')

    # process file
    docstring = ast.get_docstring(node)
    if docstring and "Attributes:" in docstring:
        # split the docstring into lines
        doc_lines = docstring.splitlines()

        # collect all instance attributes (e.g., self.attribute) in the class
        instance_attributes = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Assign):
                for target in child.targets:
                    if (isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == "self"
                            and not target.attr.startswith("__")):
                        instance_attributes.add(target.attr)

        # check for each attribute in the docstring
        for attr in instance_attributes:
            attr_found = False
            for i, line in enumerate(doc_lines):
                if (line.strip().startswith(f"{attr} (") or line.strip().startswith(f"{attr}:")):
                    attr_found = True

                    # check if type hints (brackets) are present
                    if not ("(" in line and ")" in line):
                        issues.append((filename_to_record, f"Class: {node.name}", f"Missing type brackets for attribute '{attr}'"))

                    # check for space after colon
                    if not line.endswith(": "):
                        issues.append((filename_to_record, f"Class: {node.name}", f"Missing space after colon for attribute '{attr}'"))

                    # Check if the next line starts with a capital letter
                    if i + 1 < len(doc_lines):
                        next_line = doc_lines[i + 1].strip()
                        if next_line and not next_line[0].isupper():
                            issues.append((
                                filename_to_record,
                                f"Class: {node.name}",
                                f"The description for attribute '{attr}' must start with a capital letter.",
                            ))

                    break

            if not attr_found:
                issues.append((filename_to_record, f"Class: {node.name}", f"Missing docstring description for attribute '{attr}'"))

    # return
    return issues


def display_issues_table(issues):
    # determine max width for each column
    headers = ["File", "Location", "Issue"]
    columns = [headers] + issues
    col_widths = [max(len(str(row[i])) for row in columns) for i in range(len(headers))]

    # create a table
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_header_align(["l"] * len(headers))
    table.set_cols_align(["l"] * len(headers))
    table.set_cols_valign(["m"] * len(headers))
    table.set_cols_width(col_widths)

    # add headers
    table.add_rows([["Filename", "Location", "Issue"]] + issues)

    # print the table
    print(table.draw())


def main():
    # init
    global root_path

    # args
    parser = argparse.ArgumentParser(description="Search the codebase for improperly implemented docstrings")
    parser.add_argument("--path", type=str, help="Path to recursively search for .py files in")
    args = parser.parse_args()

    # set file path and glob string
    root_path = "%s/../pyaurorax" % (os.path.dirname(os.path.realpath(__file__)))
    if (args.path is not None):
        root_path = args.path
    glob_str = "%s/**/*.py" % (root_path)

    # search for files
    print("[%s] Searching for files ..." % (datetime.datetime.now()))
    file_list = sorted(glob.glob(glob_str, recursive=True))
    print("[%s] Found %d files to process" % (datetime.datetime.now(), len(file_list)))

    # search files for issues
    issues = []
    print("[%s] Analyzing files ..." % (datetime.datetime.now()))
    for filename in file_list:
        issues.extend(check_docstring_format(filename))

    # print out issues
    if (len(issues) == 0):
        print("[%s] Found 0 issues" % (datetime.datetime.now()))
    else:
        print("[%s] Found %d issues, printing the report\n" % (datetime.datetime.now(), len(issues)))
        display_issues_table(issues)

    # return
    if (len(issues) > 0):
        return 1
    else:
        return 0


# ---------------------------
if (__name__ == "__main__"):
    sys.exit(main())
