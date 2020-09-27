# pybackup
Basic backup routine written in python.

## Requirements
- Python 3

## Usage
```
usage: pybackup.py [-h] [--date] [--verbose]

optional arguments:
  -h, --help     show this help message and exit
  --date, -d     append archive names with current date
  --verbose, -v  be verbose, e.g. print all archived files
```

First off, you need to configure the program to your needs. Modify the settings in `pybackup.ini` file according to the instructions. If you configured wrong compression values (the `compression` section), the script will fallback to the default ones (`ZIP_STORED` at level `0`).

Then, just run the script in terminal:

```
python pybackup.py
```

This will store all marked files in a nice bunch of zip archives.

__Note__: archive files will be replaced with the new ones each time you run the script, so be careful. You can use `-d` argument to append archives names with current date to leave previous archives untouched is they weren't created today, of course.
