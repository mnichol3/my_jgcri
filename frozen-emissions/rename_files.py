"""
Python 3.6

Author: Matt Nicholson
23 Dec 2019

This script iterates through the files in a given directory and replaces a target
substring in filenames with a new substring

Example usage
--------------
$ python rename_files.py -d 'CEDS\final-emissions\previous-versions' -t '2019_08_25' -n 'frozen'

CEDS_BC_emissions_by_country_sector_v_2019_08_25.csv --> CEDS_BC_emissions_by_country_sector_v_frozen.csv
"""
import os
import argparse



def init_parser():
    """
    Create & return a parser for command line arguments
    
    Parameters
    ----------
    None
    
    Returns
    -------
    parser : argparse ArgumentParser object
    
    Arguments
    ----------
        -d, --dir (str)
            Directory that holds the files to rename
        -t, --target (str)
            Target string that we wish to replace
        -n, --newstr (str)
            String to replace the target string with
    """
    
    parse_desc = """A script to rename file names by replaceing a target substring
    with a new substring. Ex: python rename_files.py -d 'CEDS\final-emissions\previous-versions' 
    -t '2019_08_25' -n 'frozen'"""
    
    parser = argparse.ArgumentParser(description=parse_desc)
    
    parser.add_argument('-d', '--dir', metavar='dir', required=True,
                        dest='dir', action='store', type=str, default=None,
                        help='Directory that holds the files to rename')
                        
    parser.add_argument('-t', '--target', metavar='target', required=True,
                        dest='target', action='store', type=str, default=None,
                        help='Sub-string to replace')
                        
    parser.add_argument('-n', '--newstr', metavar='newstr', required=True,
                        dest='newstr', action='store', type=str, default=None,
                        help='Replacement sub-string')
                        
    return parser
    
    

def rename(dir, target_str, replace_str):
    print("\n   Changing working directory to {}...\n".format(dir))
    orig_wd = os.getcwd()
    os.chdir(dir)
    
    print("   Renaming files...")
    
    longest_str = max([len(x) for x in os.listdir() if target_str in x])
    
    for f in os.listdir():
        if (target_str) in f:
            src = f
            dest = src.replace(target_str, replace_str)
            print("   {} {} {}".format(src, '-->'.rjust(longest_str - len(f) + 3, '-'), dest))
            os.rename(src, dest)
    print("\n   Finished!\n   Changing working directory back to {}".format(orig_wd))
    os.chdir(orig_wd)
    

def main():

    parser = init_parser()
    args = parser.parse_args()
    
    rename(args.dir, args.target, args.newstr)
    
    
if __name__ == '__main__':
    main()