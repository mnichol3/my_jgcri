"""
Author: Matt Nicholson
20 Jan 2020

This script reads two .csv files and "diffs", or compares, them

Usage
------

> python diff_csv.py /path/to/first.csv /path/to/second.csv

> python diff_csv.py C:\Users\nich980\data\CEDS\CEDS-uncertainty\output\fullEmissions-BC-Pshift-ACTUAL.csv
  C:\Users\nich980\code\CEDS-dev\input\fullEmissions-BC-Pshift.csv
"""
import argparse
import pandas as pd
from os.path import isfile, join

# ==============================================================================
# Define some helper functions
# ==============================================================================
def validate_path(path1, path2):
    for path in [path1, path2]:
        if (not isfile(path)):
            raise FileNotFoundError('File not found: {}'.format(path))

# ==============================================================================
# Initialize the argument parser
# ==============================================================================
parse_desc = """Diff two .csv files"""
parser = argparse.ArgumentParser(description=parse_desc)

### Positional arguments
parser.add_argument('csv_1', help='First .csv file to compare')
parser.add_argument('csv_2', help='Second .csv file to compare')

### Optional arguments
parser.add_argument('--no--header', dest='no_header', required=False,
                    default=False, action='store_true',
                    help='Make Pandas infer column headers')
                    
parser.add_argument('-d', '--dir', metavar='common_dir', dest='common_dir',
                    default=None, action='store',
                    help='Directory that holds both .csv files')

parser.add_argument('-s', '--sep', metavar='sep', dest='sep',
                    default=',', action='store',
                    help="Delimiter for the .csv files. Default is ','")
                    
args = parser.parse_args()

# ==============================================================================
# Read the two csv files
# ==============================================================================

# Determine column header arg
if (args.no_header):
    arg_header = 'infer'
else:
    arg_header = 0

# Determine file paths & validate
if (args.common_dir):
    path_csv_1 = join(args.common_dir, args.csv_1)
    path_csv_2 = join(args.common_dir, args.csv_2)
else:
    path_csv_1 = args.csv_1
    path_csv_2 = args.csv_2

validate_path(path_csv_1, path_csv_2)

print('\nReading {}...'.format(path_csv_1))
csv_1 = pd.read_csv(path_csv_1, sep=args.sep, header=arg_header)

print('Reading {}...'.format(path_csv_2))
csv_2 = pd.read_csv(path_csv_2, sep=args.sep, header=arg_header)

print('csv_1 shape: {}'.format(csv_1.shape))
print('csv_2 shape: {}'.format(csv_2.shape))

# ==============================================================================
# Compare the two csv files
# ==============================================================================

print('\nDiffing...\n')

if (csv_1.equals(csv_2)):
    print('--- csv_1 & csv_2 are identical ---')
else:
    raise ValueError('csv_1 & csv_2 are not identical')