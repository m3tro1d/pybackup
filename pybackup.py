# TODO add logging
import configparser
import os
import zipfile


def zip_dir_rec(dirname, archive):
	"""Zips a directory with all files recursively"""
	for entry in os.scandir(dirname):
		# Scan directories recursively
		if os.path.isdir(entry):
			zip_dir_rec(entry, archive)
		else:
			archive.write(entry.path)


# Parse the config file
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
	"pybackup.ini")
config.read(config_path)


# Get the config values, but skip the DEFAULT
archive_names = []
dirs_names = []
for key in list(config.keys())[1:]:
	if key.startswith("archive"):
		# Get the archive name
		archive_names.append(config[key]["name"])
	elif key.startswith("directories"):
		# Get all the directories recutsively
		current_dirs = []
		for dir_key in config[key]:
			current_dirs.append(config[key][dir_key])
		dirs_names.append(current_dirs)


# Zip the directories to the specified archives
for archive_name, target_dirs in zip(archive_names, dirs_names):
	# Initialize a ZipFile
	archive_file = zipfile.ZipFile(archive_name, 'w',
		zipfile.ZIP_DEFLATED, compresslevel=5)

	# Loop through the directories
	for target_dir in target_dirs:
		# Zip the directories relatively to their parent directory
		parent_dir = os.path.dirname(target_dir)
		archived_dir = os.path.basename(target_dir)
		os.chdir(parent_dir)
		zip_dir_rec(archived_dir, archive_file)

	# Close the file
	archive_file.close()
