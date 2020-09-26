from datetime import date
import argparse
import configparser
import os
import sys
import zipfile


# Constants for avoiding "magic" values.
DEFAULT_COMPRESSION_LEVEL = 0
DEFAULT_COMPRESSION_METHOD = "ZIP_STORED"


def zip_dir_rec(dirname, archive, verbose):
    """Zips a directory with all files recursively"""
    # This is very confusing, also what if archive is not an instance of zipfile?
    # Maybe try using isinstance(archive, zipfile.ZipFile)?
    for entry in os.scandir(dirname):
        # Scan directories recursively
        if os.path.isdir(entry):
            zip_dir_rec(entry, archive, verbose)
        else:
            if verbose:
                print("    + " + entry.name)
            archive.write(entry.path)


def get_compression_settings(config):
    """Return a tuple of (compression_level, compression_method)."""
    # Another issue: what if config is not an instance of config.ConfigParser?
    # I guess this could be a class method?
    # Or maybe run this code only as a script to avoid issues.
    
    # Switch-case-like dictionary.
    method_constant = {"ZIP_STORED": zipfile.ZIP_STORED,
                       "ZIP_DEFLATED": zipfile.ZIP_DEFLATED,
                       "ZIP_BZIP2": zipfile.ZIP_BZIP2,
                       "ZIP_LZMA": zipfile.ZIP_LZMA}

    # Get compression level.
    try:
        compresion_level = config.getint("compression", "level")
    except ValueError:
        print("Invalid compression level, using default value.")
        compression_level = DEFAULT_COMPRESSION_LEVEL

    # Get compression method.
    try:
        compression_method = method_constant[config["compression"]["method"]]
    except KeyError:
        print("Invalid compression method, using default value.")
        compression_method = DEFAULT_COMPRESSION_METHOD

    return compression_level, compression_method


def append_date(filename):
    """Appends current date (dd-mm-yy) to the filename"""
    basename = ".".join(filename.split(".")[:-1])
    ext = filename.split(".")[-1]
    today = date.today()
    str_date = today.strftime("%d-%m-%y")
    return "{}-{}.{}".format(basename, str_date, ext)


# This could run on a function or class, or under the if clause at the end.
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
# This is not necessary.
#config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
#                          "pybackup.ini")
config.read("pybackup.ini")


# Why is this here?
# Parse the settings from config file
# General overall settings
compression_method, compression_level = get_compression_settings(config)

# Archiving settings
archive_names = []
dirs_names = []
# Skip the DEFAULT section
# Making this a little more readable?
# Also, why list()? It's not like you're modifying the view-like object from .keys().
config_sections = list(config.keys())[1:]
for section in config_sections:
    if section.startswith("archive"):
        # Get the archive name
        # Append with date if needed
        if date_flag:
            archive_names.append(append_date(config[section]["name"]))
        else:
            archive_names.append(config[section]["name"])
    elif section.startswith("directories"):
        # Get all the directories
        current_dirs = []
        for directory in config[key].values():
            current_dirs.append(directory)
        dirs_names.append(current_dirs)


# Either im lazy or this is borderline unreadable.
# Shouldn't this be a function?
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


# If the code is run as a script then it should run under this if clause.
if __name__ == "__main__":
    # Read configuration.
    # Do things with zipfile.
    pass
