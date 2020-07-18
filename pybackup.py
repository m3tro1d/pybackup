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


# Parse the settings from config file
# General overall settings
# This is really messy... TODO fix this
methods = [
	zipfile.ZIP_STORED,
	zipfile.ZIP_DEFLATED,
	zipfile.ZIP_BZIP2,
	zipfile.ZIP_LZMA
]
compression_method = methods[int(config["general"]["compression_method"])]
compression_level = int(config["general"]["compression_level"])

# Archiving settings
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


# Add the directories to the specified archives
for archive_name, target_dirs in zip(archive_names, dirs_names):
	# Initialize a ZipFile
	archive_file = zipfile.ZipFile(archive_name, 'w',
		compression_method, compresslevel=compression_level)
	# Log the archive file
	print("Archiving to {}:".format(os.path.basename(archive_name)))

	# Loop through the directories
	for target_dir in target_dirs:
		# Get the needed dirnames
		parent_dir = os.path.dirname(target_dir)
		archived_dir = os.path.basename(target_dir)
		# Zip the directories relatively to their parent directory
		os.chdir(parent_dir)
		zip_dir_rec(archived_dir, archive_file)
		# Log the action
		print("  + {}".format(archived_dir))

	# Close the file
	archive_file.close()
