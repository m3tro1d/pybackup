# pybackup
Basic backup routine written in python.

## Requirements
- Python 3

## Usage
```
Usage: pybackup.py [OPTIONS]

Options:
  -h,  --help      show help
  -d,  --date      append archive names with current date (def: False)
  -v,  --verbose   log all archived files (def: False)
```

First off, you need to configure the program to your needs. Modify the settings in `pybackup.ini` file according to the instructions. If you configured wrong compression values (the `compression` section), the script will fallback to the default ones (`ZIP_STORED` at level `0`).

Then, just run the script in terminal:

```
python pybackup.py
```

This will store all marked files in a nice bunch of zip archives.

**Note**: archive files will be replaced with the new ones each time you run the script, so be careful. You can use `-d` argument to append archives names with current date to leave previous archives untouched is they weren't created today, of course.
