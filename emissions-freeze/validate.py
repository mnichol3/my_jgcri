# -*- coding: utf-8 -*-
"""
Author: Matt Nicholson

"""
import pandas as pd
import numpy as np
import re
import logging

from os.path import isdir, isfile, join
from os import getcwd, listdir, mkdir, remove

import ceds_io



def nuke_logs():
    cwd = getcwd()
    log_dir = join(cwd, "logs")
    
    log_files = [f for f in listdir(log_dir) if "validate" in f]
   
    for f in log_files:
        remove(join(log_dir, f))



def setup_logger():
    nuke_logs()
    
    log_format = logging.Formatter("%(asctime)s %(levelname)6s: %(message)s", "%Y-%m-%d %H:%M:%S")
    
    cwd = getcwd()
    f_name = 'validate.log'.format()
    
    f_dir = join(cwd, 'logs')
    local_dir = join('logs', f_name)
    
    if (not isdir(f_dir)):
        mkdir(f_dir)
        
    handler = logging.FileHandler(local_dir)
    handler.setFormatter(log_format)
        
    logger = logging.getLogger("validate")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
    logger.info("Log created!\n")
    
    return logger



def diff_activity_files(dir_path):
        
    """
    Compare all activity files in the given directory to eachother
    
    This function acts to 'diff' Pandas DataFrames holding CMIP6 total activity 
    data using the Pandas DataFrame.Equals function 
    (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.equals.html)
    Each pair of activity .csv files that are not identical are printed at the
    end of execution.
    
    Parameters
    -----------
    dir_path : str
        Absolute path of the directory holding the activity files to compare
        
    Returns
    -------
    None
    
    """
    logger = logging.getLogger('main')
    logger.info('In validate::diff_activity_files()')
    
    activity_files = []
    mismatch = []
    file_re= r'(H\.\w+_total_activity_extended.csv)'
    
    print("\nFetching activity files to Diff from {}...".format(dir_path))
    logger.info("Searching for activity files in {}".format(dir_path))
    
    # Iterate through files in dir_path and cumulate names of activity files
    for f in listdir(dir_path):
        if (isfile(join(dir_path, f))):
            match = re.match(file_re, f)
            if (match):
                activity_files.append(match.group(1))
    
    info_str = "Activity files found: {}".format(len(activity_files))
    print("\n{}".format(info_str))
    print("-"*25)
    logger.info(info_str)
    
    for f in activity_files:
        print(f)
        logger.info(f)
    print("\n")
    
    for idx, act_file in enumerate(activity_files):
        path_f1 = join(dir_path, act_file)
        df1 = pd.read_csv(path_f1, sep=',', header=0)
        
        for j in range(len(activity_files) - idx):
            info_str = "Comparing {} and {}...".format(act_file, activity_files[j])
            print(info_str)
            logger.info(info_str)
            
            path_f2 = join(dir_path, activity_files[j])
            df2 = pd.read_csv(path_f2, sep=',', header=0)
            
            if (not df1.equals(df2)):
                # If the two dataframes are not identical, add them to a list
                # to be printed at the end of function execution
                mismatch_f1 = act_file
                mismatch_f2 = activity_files[j]
                
                # Only add a pair of mismatched activity files once
                if ([mismatch_f1, mismatch_f2] not in mismatch and 
                    [mismatch_f2, mismatch_f1] not in mismatch):
                    
                    mismatch.append([mismatch_f1, mismatch_f2])
            
            del df2
        del df1
    
    if (len(mismatch) >0 ):
        info_str = "The following activity files did not match:"
        logger.info(info_str)
        print("\n{}".format(info_str))
        print("-"*(55-12))
        
        for pair in mismatch:
            info_str = "{} and {}".format(pair[0], pair[1])
            logger.info(info_str)
            print("--- {} ---".format(info_str))
    else:
        info_str = "All activity files are identical"
        logger.info("{}\n".format(info_str))
        print("\n--- {} ---\n".format(info_str))



def ef_zscore(df, thresh=3):
    """
    Calculate the Z score for an Emission Factor file
    
    This function calculates the Z score for a CMIP6 Emission Factor (EF) file.
    The Z Score is applied to a DataFrame that has been trimmed to only contain
    yr +/- 'yr_rng' years worth of data
    
    Parameters
    ----------
    ef_df : Pandas DataFrame
        DataFrame containing CEDS CMIP6 Emission Factors
    thresh : int, optional
        Threshold used to identify outliers given a Z score. Default is 3
        
    Returns
    -------
    result : int
        0 if elements with Z-scores that fall outside the specified range are present,
        1 if all Z-scores are within range
    """
    from scipy.stats import zscore
    
    ignore_cols = ['iso', 'sector', 'fuel', 'units']
    
    cols = list(df.columns)
    
    # Remove str cols
    for x in ignore_cols:
        cols.remove(x)
        
    df_stripped = df[cols]
    
    df_arr = np.asarray(df_stripped, dtype=np.float32)
        
    score = np.abs(zscore(df_arr))
    
    bad_z = np.where(score > thresh)
    
    return bad_z



def run_zscores(df, isos, fuels, species):
    results = []
    out_path = ''
    df = ceds_io.subset_yr_span(df, 1970)
    
    isos = ceds_io.get_isos(df)
    
    for iso in isos:
        iso_df = ceds_io.subset_iso(df, iso)                # Subset for current iso
        for fuel in fuels:
            temp_df = ceds_io.subset_fuel(iso_df, fuel)     # Subset for current fuel
            
            print('Processing:')
            print('     Species: {}'.format(species))
            print('     iso:     {}'.format(iso))
            print('     fuel:    {}'.format(fuel))
            
            bad_z = ef_zscore(temp_df)
            
            num_outliers = bad_z[0].size
            
            print('     Outliers flagged: {}\n'.format(num_outliers))
            
            if (num_outliers != 0):
                results.append([species, iso, fuel])
                print(temp_df)
                print('\n')
        exit(0)
    
    out_path = join(out_path, 'bad_z.csv')
    ceds_io.arr_to_csv(results, out_path)
    


def pp_results(rslt):
    rslt_strs = [x[0] for x in rslt]
    max_len = len(max(rslt_strs, key=len))
    
    print('Z-Score Results')
    print('---------------')
    
    for pair in rslt:
        if (pair[1] == 1):
            z_str = 'OK'
        else:
            z_str = 'Bad Z-score(s) present'
        print('{}: {}'.format(pair[0], z_str.rjust(max_len - len(pair[0]) + 2)))
        
        
     
def calc_emissions(dir_dict):
    """
    Calculate the hypothetical emissions from the frozen emissions and the CMIP6
    activity files
    
    Emissions = EF x Activity
    
    Parameters
    -----------
    dir_dict : dictionary of {str: str}
        Dictionary holding the paths to directories for the various files needed.
        Keys: ['base_dir_ef', 'base_dir_act', 'out_path_ems']
        
    Return
    -------
    None, writes to file
    """
    logger = logging.getLogger('main')
    logger.info('In validate::calc_emissions()')
    
    # Unpack for better readability
    base_dir_ef = dir_dict['base_dir_ef']
    base_dir_act = dir_dict['base_dir_act']
    out_path_ems = dir_dict['out_path_ems']
    
    logger.info('Searing for available species in {}'.format(base_dir_ef))
    em_species = ceds_io.get_avail_species(base_dir_ef)
    
    for species in em_species:
        info_str = 'Calculating frozen total emissions for {}'.format(species)
        logger.info(info_str)
        print(info_str)
        
        # Get emission factor file for species
        logger.info('Fetching emission factor file from {}'.format(base_dir_ef))
        frozen_ef_file = ceds_io.get_file_for_species(base_dir_ef, species, "ef")
        
        # Get activity file for species
        logger.info('Fetching activity file from {}'.format(base_dir_act))
        activity_file = ceds_io.get_file_for_species(base_dir_act, species, "activity")
        
        ef_path = join(base_dir_ef, frozen_ef_file)
        act_path = join(base_dir_act, activity_file)
        
        # Create list of strings representing year column headers
        data_col_headers = ['X{}'.format(i) for i in range(1750, 2015)]
        
        # Read emission factor & activity files into DataFrames
        logger.info('Reading emission factor file from {}'.format(ef_path))
        ef_df = pd.read_csv(ef_path, sep=',', header=0)
        
        logger.info('Reading activity file from {}'.format(act_path))
        act_df = pd.read_csv(act_path, sep=',', header=0)
        
        # Get the 'iso', 'sector', 'fuel', & 'units' columns
        meta_cols = ef_df.iloc[:, 0:4]
        
        # Sanity check
        if (meta_cols.equals(act_df.iloc[:, 0:4])):
            err_str = 'Emission Factor & Activity DataFrames have mis-matched meta columns'
            logger.error(err_str)
            raise ValueError(err_str)
        
        # Get a subset of the emission factor & activity files that contain numerical
        # data so we can compute emissions
        logger.info('Subsetting emission factor & activity DataFrames')
        ef_subs = ef_df[data_col_headers]
        act_subs = act_df[data_col_headers]
        
        logger.info('Calculating total emissions')
        emissions_df = pd.DataFrame(ef_subs.values * act_subs.values,
                                    columns=ef_subs.columns, index=ef_subs.index)
        
        # Insert the meta ('iso', 'sector', 'fuel', 'units') columns at the 
        # beginning of the DataFrame
        logger.info('Concatinating meta_cols and emissions_df DataFrames along axis 1')
        emissions_df = pd.concat([meta_cols, emissions_df], axis=1)
       
        f_name = '{}_total_frozen_emissions.csv'.format(species)
        
        f_out = join(out_path_ems, f_name)
        
        info_str = 'Writing emissions DataFrame to {}'.format(f_out)
        logger.info(info_str)
        print('     {}\n'.format(info_str))
        
        emissions_df.to_csv(f_out, sep=',', header=True, index=False)
        logger.info('Finished calculating total emissions for {}'.format(species))
        
    # End species loop
    logger.info('Leaving validate::calc_emissions()\n')
    
    
    
def main():
    logger = setup_logger()
    logger.info('In validate::main()')
    """
    Tasks to run calc_emissions() for frozen emission factor files
    """
    logger.info('Initializing data directory paths')
    
    #'base_dir_act' : r"C:\Users\nich980\data\CEDS_CMIP6_Release_Archive\intermediate-output",
    
    dirs = {
            'base_dir_ef': r"C:\Users\nich980\data\e-freeze\dat_out\ef_files",
            'base_dir_act' : r"C:\Users\nich980\data\CEDS\CEDS\intermediate-output",
            'out_path_ems' : r"C:\Users\nich980\data\e-freeze\dat_out\frozen_emissions"
            }
    
    for key, val in dirs.items():
        logger.info('{}: {}'.format(key, val))
        
    diff_activity_files(dirs['base_dir_act'])
        
        
        
        
        
        
    
    
if __name__ == '__main__':
    main()            
            
            
            
            
            
            
            
