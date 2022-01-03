#! /usr/bin/env python
#
# This script will bump the version number to the
# version specified as a CLI parameter by editing
# the version number in a few files in the repository
# automatically.

import argparse
import os
import shutil


def main():
    # args
    parser = argparse.ArgumentParser(description="Bump the version number for the AuroraX library")
    parser.add_argument("version", type=str, help="Version number to bump to")
    args = parser.parse_args()

    # bump pyproject.toml
    print("Updating pyproject.toml file ...")
    os.system("poetry version %s" % (args.version))
    print()

    # bump version test
    print("Updating tests/test_suite/test_version.py file ...")
    src_filename = "%s/../tests/test_suite/test_version.py" % (os.path.dirname(os.path.realpath(__file__)))
    dst_filename = "%s/../tests/test_suite/test_version.py.bak" % (os.path.dirname(os.path.realpath(__file__)))
    try:
        # open files for read/write
        shutil.copyfile(src_filename, dst_filename)
        fp_read = open(src_filename, 'r')
        fp_write = open(dst_filename, 'w')

        # update file
        for line in fp_read:
            if ("assert __version__" in line):
                fp_write.write("    assert __version__ == \"%s\"\n" % (args.version))
            else:
                fp_write.write(line)

        # close file handlers
        fp_read.close()
        fp_write.close()

        # swap files and remove bak file
        shutil.copyfile(dst_filename, src_filename)
        os.remove(dst_filename)
    except IOError as e:
        print("Error: %s" % (str(e)))
        return 1
    print()

    # bump __version__ variable in __init__.py
    print("Updating pyaurorax/__init__.py file ...")
    src_filename = "%s/../pyaurorax/__init__.py" % (os.path.dirname(os.path.realpath(__file__)))
    dst_filename = "%s/../pyaurorax/__init__.py.bak" % (os.path.dirname(os.path.realpath(__file__)))
    try:
        # open files for read/write
        shutil.copyfile(src_filename, dst_filename)
        fp_read = open(src_filename, 'r')
        fp_write = open(dst_filename, 'w')

        # update file
        for line in fp_read:
            if ("__version__ = " in line):
                fp_write.write("__version__ = \"%s\"\n" % (args.version))
            else:
                fp_write.write(line)

        # close file handlers
        fp_read.close()
        fp_write.close()

        # swap files and remove bak file
        shutil.copyfile(dst_filename, src_filename)
        os.remove(dst_filename)
    except IOError as e:
        print("Error: %s" % (str(e)))
        return 1
    print()

    # bump version variable in aurorax-cli
    print("Updating pyaurorax/cli/cli.py file ...")
    src_filename = "%s/../pyaurorax/cli/cli.py" % (os.path.dirname(os.path.realpath(__file__)))
    dst_filename = "%s/../pyaurorax/cli/cli.py.bak" % (os.path.dirname(os.path.realpath(__file__)))
    try:
        # open files for read/write
        shutil.copyfile(src_filename, dst_filename)
        fp_read = open(src_filename, 'r')
        fp_write = open(dst_filename, 'w')

        # update file
        for line in fp_read:
            if ("@click.version_option" in line):
                fp_write.write("@click.version_option(version=\"%s\")\n" % (args.version))
            else:
                fp_write.write(line)

        # close file handlers
        fp_read.close()
        fp_write.close()

        # swap files and remove bak file
        shutil.copyfile(dst_filename, src_filename)
        os.remove(dst_filename)
    except IOError as e:
        print("Error: %s" % (str(e)))
        return 1
    print()

    # end
    print("Successfully bumped version!")
    return 0


# -----------------
if (__name__ == "__main__"):
    main()
