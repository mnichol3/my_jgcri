# -*- coding: utf-8 -*-
"""
Author: Matt Nicholson

"""
import pandas as pd
import numpy as np
import re

from os.path import isfile, join
from os import listdir

import ceds_io


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
    activity_files = []
    mismatch = []
    file_re= r'(H\.\w+_total_activity_extended.csv)'
    
    print("\nSearching in {}...".format(dir_path))
    
    # Iterate through files in dir_path and cumulate names of activity files
    for f in listdir(dir_path):
        if (isfile(join(dir_path, f))):
            match = re.match(file_re, f)
            if (match):
                activity_files.append(match.group(1))
    
    print("\nActivity files found: {}".format(len(activity_files)))
    print("-"*25)
    for f in activity_files:
        print(f)
    print("\n")
    
    for idx, act_file in enumerate(activity_files):
        path_f1 = join(dir_path, act_file)
        df1 = pd.read_csv(path_f1, sep=',', header=0)
        
        for j in range(len(activity_files) - idx):
            print("Comparing {} and {}...".format(act_file, activity_files[j]))
            path_f2 = join(dir_path, activity_files[j])
            df2 = pd.read_csv(path_f2, sep=',', header=0)
            
            if (not df1.equals(df2)):
                # If the two dataframes are not identical, add them to a list
                # to be printed at the end of function execution
                mismatch.append([act_file, activity_files[j]])
            
            del df2
        del df1
    
    if (len(mismatch) >0 ):
        print("\nThe following activity files did not match:")
        print("-"*(55-12))
        
        for pair in mismatch:
            print("--- {} and {} ---".format(pair[0], pair[1]))
    else:
        print("\n--- All activity files are identical ---")



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
        
        
     
def calc_emissions(species, ef_file, act_file, out_path):
    """
    Calculate the hypothetical emissions from the frozen emissions and the CMIP6
    activity files
    
    Emissions = EF x Activity
    
    Parameters
    -----------
    species : str
        Emissions species
    ef_file : str
        Absolute path of the frozen emission factor file for the given emissions species
    act_file : str
        Absolute path of the activity file for the given emissions species
    out_path : str
        Directory to write the resulting emissions file to
    """
    print('Calculating frozen total emissions for {}'.format(species))
    
    data_col_headers = ['X{}'.format(i) for i in range(1750, 2015)]
    
    ef_df = pd.read_csv(ef_file, sep=',', header=0)
    act_df = pd.read_csv(act_file, sep=',', header=0)
    
    # Get the 'iso', 'sector', 'fuel', & 'units' columns
    meta_cols = ef_df.iloc[:, 0:4]
    
    # Sanity check
    if (meta_cols.equals(act_df.iloc[:, 0:4])):
        raise ValueError('Emission Factor & Activity DataFrames have mis-matched meta columns')
    
    # Get a subset of the emission factor & activity files that contain numerical
    # data so we can compute emissions
    ef_subs = ef_df[data_col_headers]
    act_subs = act_df[data_col_headers]
    
    
    emissions_df = pd.DataFrame(ef_subs.values * act_subs.values,
                                columns=ef_subs.columns, index=ef_subs.index)
    
    f_name = '{}_total_frozen_emissions.csv'.format(species)
    
    f_out = join(out_path, f_name)
    
    print('     writing to file....')
    
    emissions_df.to_csv(f_out, sep=',', header=True, index=False)
    
    
    
def main():
    
    """
    Tasks to run calc_emissions() for frozen emission factor files
    """
    
    base_dir_ef = r"C:\Users\nich980\data\e-freeze\dat_out\ef_files"
    base_dir_act = r"C:\Users\nich980\data\CEDS_CMIP6_Release_Archive\intermediate-output"
    out_path_ems = r"C:\Users\nich980\data\e-freeze\dat_out\frozen_emissions"
#    out_path_act = r"C:\Users\nich980\data\e-freeze\dat_out\frozen_activity"
    
#    diff_activity_files(base_dir_act)
    
    # Emission species in the above directory
    em_species = ceds_io.get_avail_species(base_dir_ef)
    
    for species in em_species:
        
        # Get emission factor file for species
        frozen_ef_file = ceds_io.get_file_for_species(base_dir_ef, species, "ef")
        
        # Get activity file for species
        activity_file = ceds_io.get_file_for_species(base_dir_act, species, "activity")
        
        ef_path = join(base_dir_ef, frozen_ef_file)
        act_path = join(base_dir_act, activity_file)
        
        calc_emissions(species, ef_path, act_path, out_path_ems)
        
        
        
        
        
        
    
    
if __name__ == '__main__':
    main()            
            
            
            
            
            
            
            
