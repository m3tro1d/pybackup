import configparser
import os
import zipfile


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
