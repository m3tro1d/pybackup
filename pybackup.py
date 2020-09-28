from datetime import date
import argparse
import configparser
import os
import sys
import zipfile


# Constants
DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   "pybackup.ini")
DEFAULT_COMPRESSION_LEVEL = 0
DEFAULT_COMPRESSION_METHOD = "ZIP_STORED"


def parse_arguments():
    """Process & return an argparse.ArgumentParser object"""
    parser = argparse.ArgumentParser(
        description="""A simple backup routine in python.""")

    parser.add_argument("--date", "-d", action="store_true",
                        help="append archive names with current date")

    parser.add_argument("--verbose", "-v", action="store_true",
                        help="be verbose, e.g. print all archived files")

    args = parser.parse_args()
    return args


def config_init():
    """Return a configparser.ConfigParser object with current options"""
    config = configparser.ConfigParser()
    config.read(DEFAULT_CONFIG_PATH)
    return config


def zip_dir_rec(dirname, archive, verbose):
    """Zips a directory with all files recursively"""
    # Scan directories recursively
    for entry in os.scandir(dirname):
        # If it's a directory, zip it recursively
        if os.path.isdir(entry):
            zip_dir_rec(entry, archive, verbose)
        # If it's a file, just add it
        else:
            if verbose:
                print("    + " + entry.name)
            archive.write(entry.path)


def get_compression_settings(config):
    """Return a tuple of (compression_level, compression_method)"""
    # Methods dictionary
    method_constant = {"ZIP_STORED"   : zipfile.ZIP_STORED,
                       "ZIP_DEFLATED" : zipfile.ZIP_DEFLATED,
                       "ZIP_BZIP2"    : zipfile.ZIP_BZIP2,
                       "ZIP_LZMA"     : zipfile.ZIP_LZMA}

    # Get compression level
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


def get_archives_settings(config, date_flag):
    """Return two lists: archive_names, dirs_names"""
    archive_names = []
    dirs_names = []

    # Skip the DEFAULT section (using list to make it subscriptable)
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
            for directory in config[section].values():
                current_dirs.append(directory)
            dirs_names.append(current_dirs)

    return archive_names, dirs_names


def append_date(filename):
    """Appends current date (dd-mm-yy) to the filename"""
    basename = ".".join(filename.split(".")[:-1])
    ext = filename.split(".")[-1]
    today = date.today()
    str_date = today.strftime("%d-%m-%y")
    return "{}-{}.{}".format(basename, str_date, ext)


def run_backup(archive_names, dirs_names,
               cmp_method, cmp_level,
               verbose):
    """Actual archiving happens here"""
    # Add the directories to the specified archives
    for archive_name, target_dirs in zip(archive_names, dirs_names):
        # Initialize a ZipFile
        archive_file = zipfile.ZipFile(archive_name, 'w',
            cmp_method, compresslevel=cmp_level)
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


def main():
    """Entry point of the script"""
    # Parse the input arguments
    args = parse_arguments()
    date_flag = args.date
    verbose = args.verbose

    # Parse the config & get all settings
    config = config_init()
    compression_method, compression_level = get_compression_settings(config)
    # TODO make date appending a separate function
    archive_names, dirs_names = get_archives_settings(config, date_flag)

    # Do the job
    run_backup(archive_names, dirs_names,
               compression_method, compression_level,
               verbose)


# Entry point
if __name__ == "__main__":
    main()
