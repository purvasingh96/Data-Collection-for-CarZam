#!/usr/bin/env python3

"""csvHandler.py: General lib for handling CSV files"""

__author__      = "Purva Singh"
__version__ = "1.0"
__maintainer__ = "Purva Singh"
__email__ = "psingh359@gatech.edu"

import csv
import os

def exportCSV(filePath,listToExport):
    if not isinstance(listToExport,list) or len(listToExport) < 1:
        print("csvHandler Exception: Invalid list of ditionaries passed to exportCSV")
        exit(1)

    if not isinstance(listToExport[0],dict):
        print("csvHandler Exception: Invalid list of dictionaries passed to exportCSV")
        exit(1)

    keys = listToExport[0].keys()
    with open(filePath, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(listToExport)

def importCSV(filePath):
    if os.path.exists(filePath):
        with open(filePath) as f:
            reader = csv.reader(f, skipinitialspace=True)
            header = next(reader)
            data = [dict(zip(header, map(str, row))) for row in reader]
            f.close()
    else:
        print("csvHandler Exception: CSV file to import not found")
        exit(1)

    return data