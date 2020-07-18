import configparser
import os
import zipfile


# Parse the config file
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
	"pybackup.ini")
config.read(config_path)
print(config.sections())

# Zip the directories to the specified archives
