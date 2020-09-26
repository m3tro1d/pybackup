from datetime import date
import argparse
import configparser
import os
import sys
import zipfile


def zip_dir_rec(dirname, archive, verbose):
    """Zips a directory with all files recursively"""
    for entry in os.scandir(dirname):
        # Scan directories recursively
        if os.path.isdir(entry):
            zip_dir_rec(entry, archive, verbose)
        else:
            if verbose:
                print("    + " + entry.name)
            archive.write(entry.path)


def get_compression_settings(config):
    """Returns a tuple of (compression_method, compression_level)"""
    """And handles possible exceptions"""
    methods = [
        zipfile.ZIP_STORED,
        zipfile.ZIP_DEFLATED,
        zipfile.ZIP_BZIP2,
        zipfile.ZIP_LZMA
    ]
    try:
        # Get the values & handle exceptions
        cmp_method = methods[int(config["general"]["compression_method"])]
        cmp_lvl = int(config["general"]["compression_level"])

        # Check the level
        if not 0 <= cmp_lvl < len(methods):
            raise IndexError("Invalid compression level {}".format(cmp_lvl))

    except ValueError as er:
        # Handle invalid types (e.g. not numbers)
        print("Invalid compression settings format: {}".format(er))
        sys.exit(1)

    except IndexError as er:
        # Handle invalid values
        print("Error!")
        print("Invalid compression values: {}".format(er))
        print("Using the default values (method: 1 ZIP_DEFLATED; lvl: 5).\n")
        cmp_method = methods[1]
        cmp_lvl = 5

    return (cmp_method, cmp_lvl)


def append_date(filename):
    """Appends current date (dd-mm-yy) to the filename"""
    basename = ".".join(filename.split(".")[:-1])
    ext = filename.split(".")[-1]
    today = date.today()
    str_date = today.strftime("%d-%m-%y")
    return "{}-{}.{}".format(basename, str_date, ext)


# Parse the input arguments
parser = argparse.ArgumentParser(
    description="""A simple backup routine in python.""")

parser.add_argument("--date", "-d", action="store_true",
                    help="append archive names with current date")

parser.add_argument("--verbose", "-v", action="store_true",
                    help="be verbose, e.g. print all archived files")

args = parser.parse_args()
date_flag = args.date
verbose = args.verbose


# Parse the config file
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           "pybackup.ini")
config.read(config_path)


# Parse the settings from config file
# General overall settings
compression_method, compression_level = get_compression_settings(config)

# Archiving settings
archive_names = []
dirs_names = []
# Skip the DEFAULT section
for key in list(config.keys())[1:]:
    if key.startswith("archive"):
        # Get the archive name
        # Append with date if needed
        if date_flag:
            archive_names.append(append_date(config[key]["name"]))
        else:
            archive_names.append(config[key]["name"])
    elif key.startswith("directories"):
        # Get all the directories
        current_dirs = []
        for directory in config[key].values():
            current_dirs.append(directory)
        dirs_names.append(current_dirs)


# Add the directories to the specified archives
for archive_name, target_dirs in zip(archive_names, dirs_names):
    # Initialize a ZipFile
    archive_file = zipfile.ZipFile(archive_name, 'w',
        compression_method, compresslevel=compression_level)
    # Log the archive file
    print("Archiving to {}:".format(os.path.basename(archive_name)))

    # Loop through the directories
    for target_dir in target_dirs:
        # Check if the directory exists
        if os.path.isdir(target_dir):
            # Get the needed dirnames
            parent_dir = os.path.dirname(target_dir)
            archived_dir = os.path.basename(target_dir)
            os.chdir(parent_dir)
            # Log the action
            print("  + {}".format(archived_dir))
            # Zip the directories relatively to their parent directory
            zip_dir_rec(archived_dir, archive_file, verbose)
        else:
            print("'{}' is not a directory.".format(target_dir))

    # Close the file
    archive_file.close()
