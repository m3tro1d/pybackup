import configparser
import zipfile


# Parse the config file
config = configparser.ConfigParser()
config.read("pybackup.ini")
print(config.sections())

# Zip the directories to the specified archives
