"""
Author: Matt Nicholson
20 Jan 2020

This script reads two .csv files and "diffs", or compares, them

Usage
------

> python diff_csv.py /path/to/first.csv /path/to/second.csv
"""
import argparse
import yaml
import pandas as pd
from pathlib import Path
from os.path import isfile, join
from os import remove

# ==============================================================================
# Define some helper functions
# ==============================================================================
def validate_path(path1, path2):
    """
    Given two paths, ensure they both exist. If one or both do not exist, raise
    a FileNotFoundError
    
    Params
    ------
    path1 : str
        Absolute path of the first file to validate
    path2 : str
        Absolute path of the second file to validate
    
    Return
    ------
    None
    """
    for path in [path1, path2]:
        if (not isfile(path)):
            raise FileNotFoundError('File not found: {}'.format(path))
        
        
def clean_files(csv_1, csv_2):
    """
    Clean (remove) .csv files, if applicable
    
    Params
    ------
    csv_1 : Dict
        Dictionary representation of a .csv file from an input .yml file
    csv_2 : Dict
        Dictionary representation of a .csv file from an input .yml file
    
    Return
    ------
    None
    """
    for csv in [csv_1, csv_2]:
        if (csv['needs_clean']):
            csv_path = csv['path']
            csv_name = csv['file']
            csv_abs = join(csv_path, csv_name)
            print('Cleaning {}...'.format(csv_name))
            remove(csv_abs)

# ==============================================================================
# Initialize the argument parser
# ==============================================================================
parse_desc = """Diff two .csv files"""
parser = argparse.ArgumentParser(description=parse_desc)

### Positional arguments
parser.add_argument('-f', '--files', dest='files', required=False,
                    nargs=2, default=None, action='store',
                    help='Absolute paths of the csv files to compare')

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
                    
parser.add_argument('-i', '--in-file', metavar='in_file', dest='in_file',
                    default=None, action='store',
                    help="Name of the .yml file to get the .csv file names & paths from")
                    
parser.add_argument('-c', '--clean', dest='clean',
                    default=False, action='store_true',
                    help="Delete any .csv files that have 'needs_clean: True' in their .yml input file")
                    
args = parser.parse_args()

# ==============================================================================
# Read the two csv files
# ==============================================================================

# Determine column header arg
if (args.no_header):
    arg_header = 'infer'
else:
    arg_header = 0
    

### Determine file paths & validate
if (args.in_file):
    # The user passes a .yml file name
    if (isfile(args.in_file)):
        print('\nParsing {}...'.format(args.in_file))
        with open(args.in_file, 'r') as stream:
            try:
                csv_1, csv_2 = yaml.safe_load(stream)
                
                path_csv_1 = join(csv_1['path'], csv_1['file'])
                path_csv_2 = join(csv_2['path'], csv_2['file'])
            except yaml.YAMLError as err:
                print(err)
        
    else:
        raise FileNotFoundError('Input file {} not found'.format(args.in_file))
else:
    # User passes the names of the files
    path_csv_1 = Path(args.files[0])
    path_csv_2 = Path(args.files[1])
    
    if (args.common_dir):
        dir_cmn = Path(args.common_dir)
        path_csv_1 = join(dir_cmn, path_csv_1)
        path_csv_2 = join(dir_cmn, path_csv_2)
        
validate_path(path_csv_1, path_csv_2)

print('\nReading {}...'.format(path_csv_1))
csv_1 = pd.read_csv(path_csv_1, sep=args.sep, header=arg_header)

print('Reading {}...'.format(path_csv_2))
csv_2 = pd.read_csv(path_csv_2, sep=args.sep, header=arg_header)

# ==============================================================================
# Compare the two csv files
# ==============================================================================

print('\nDiffing...\n')

if (csv_1.equals(csv_2)):
    print('--- csv_1 & csv_2 are identical ---')
else:
    print('csv_1 shape: {}'.format(csv_1.shape))
    print('csv_2 shape: {}\n'.format(csv_2.shape))
    
    raise ValueError('csv_1 & csv_2 are not identical')
    
# ==============================================================================
# Clean .csv files, if needed
# ==============================================================================
if (args.in_file and args.clean):
    clean_files(csv_1, csv_2)