# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 13:54:20 2019

@author: nich980

This file holds I/O functions for CEDS/EMIPS data files
"""

import re
import logging
import pandas as pd
from os.path import isfile, join
from os import listdir


def read_ef_file(abs_path):
    """
    Read the Emission Factor csv into a Pandas DataFrame
    
    Parameters
    -----------
    abs_path : str
        Absolute path of the Emission Factors file
    
    Returns
    -------
    ef_df : Pandas DataFrame
        DataFrame containing the emission factor data.
        
        Column headers: ['iso', 'sector', 'fuel', 'units', 'X1750', 'X1751',
                         ...,   'X2013', 'X2014']
    """
    ef_df = pd.read_csv(abs_path, sep=',', header=0)
    
    return ef_df



def fetch_ef_files(dir_path):
    """
    Get the names of all emission factor files in a given directory
    
    Parameters
    ----------
    dir_path : str
        Absolute path of the directory to search within
        
    Returns
    -------
    f_names : list of str
        Names of the emission factor files found within the specified directory
    """
    
    patterns = {
            "base" : r'(^H\.\w{1,7}_total_EFs_extended.csv$)'
            }
                    
    re_pat = patterns["base"]
    
    f_names = [f for f in listdir(dir_path) if (isfile(join(dir_path, f)) and re.match(re_pat, f))]
    
    return f_names



def fetch_activity_files(dir_path):
    """
    Get the names of all activity files in a given directory
    
    Parameters
    ----------
    dir_path : str
        Absolute path of the directory to search within
        
    Returns
    -------
    f_names : list of str
        Names of the activity files found within the specified directory
    """
    
    patterns = {
            "base" : r'(^H\.\w{1,7}_total_activity_extended.csv$)'
            }
                    
    re_pat = patterns["base"]
    
    f_names = [f for f in listdir(dir_path) if (isfile(join(dir_path, f)) and re.match(re_pat, f))]
    
    return f_names



def get_file_for_species(dir_path, species, f_type):
    """
    Get an output file (i.e., EF, total activity, etc.) for a given species
    of emission
    
    Parameters
    ----------
    dir_path : str
        Absolute path of the directory to search within
    species : str
        Emissions species
    f_type : str
        Type of file (EF, total activity, etc.)
        
    Returns
    -------
    f_name : str
        Name of the file found in the directory
    """
    bases = {
            "ef" : "H.{}_total_EFs_extended.csv",
            "activity": "H.{}_total_activity_extended.csv"
            }
    
    f_name = bases[f_type].format(species)
    f_abs = join(dir_path, f_name)
    
    if (not isfile(f_abs)):
        raise FileNotFoundError("No such file or directory: {}".format(f_abs))
    else:
        return f_name
    


def get_avail_species(dir_path):
    """
    Get the emission species available in a given directory
    
    Parameters
    ----------
    dir_path : str
        Absolute path of the directory to search within
        
    Returns
    -------
    species : list of str
        List containing the emission species found in the directory
    """
    pattern = r'^H\.(\w{1,7})_total_EFs_extended.csv$'
    
    species = [re.match(pattern, f).group(1) for f in listdir(dir_path) if (re.match(pattern, f))]
    return species



def get_species_from_fname(f_name):
    pattern = r'^H\.(\w{1,7})_'
    
    match = re.search(pattern, f_name)
    if (match):
        return match.group(1)
    else:
        return -1



def get_species(dir_path):
    species = []
    pattern = r'^H\.(\w{1,7})_total_EFs_extended.csv$'
    
    for f in listdir(dir_path):
        match = re.match(pattern, f)
        if (match):
            species.append(match.group(1))
    
    # Remove duplicate species
    species_set = set(species)
    species = list(species_set)
    
    return species



def chunker(iso_list, size):
    return (iso_list[pos:pos + size] for pos in range(0, len(iso_list), size))
    
        
        
def get_isos(df):
    """
    Get an array of ISOs (countries) in the DataFrame
    
    Parameters
    ----------
    df : Pandas DataFrame
        DataFrame containing emission data
        
    Returns
    -------
    isos = numpy array of str
        Array containing the ISOs present in the emissions DataFrame
    """
    isos = list(df['iso'].unique())
    return isos



def get_sectors(df, comb_filter=True):
    """
    Get an array of sectors in the DataFrame
    
    Parameters
    ----------
    df : Pandas DataFrame
        DataFrame containing emission data
    comb_filter : bool, optional
        If True, non-combustion related sectors will be removed. Default is True
        
    Returns
    -------
    sectors = numpy array of str
        Array containing the sectors present in the emissions DataFrame
    """
    if (comb_filter):
        df = filter_data_sector(df)
    
    sectors = df['sector'].unique()
    return sectors



def subset_iso(df, iso):
    """
    Return a subset of an emissions DataFrame where the value in the 'iso'
    column is equal to that of the 'iso' param
    
    Parameters
    ----------
    df : Pandas DataFrame
        DataFrame containing emission data
    iso : str or list
        iso(s) used for subsetting
        
    Returns
    -------
    subs_df : Pandas DataFrame
        DataFrame containing only emissions data for the specified iso
    """
    if (isinstance(iso, str)):
        iso = [iso]
        
    subs_df = df.loc[df['iso'].isin(iso)]
    return subs_df



def subset_sector(df, sector):
    """
    Return a subset of an emissions DataFrame where the value in the 'sector'
    column is equal to that of the 'sector' param
    
    Parameters
    ----------
    df : Pandas DataFrame
        DataFrame containing emission data
    sector : str
        sector used for subsetting
        
    Returns
    -------
    subs_df : Pandas DataFrame
        DataFrame containing only emissions data for the specified sector
    """
    subs_df = df.loc[df['sector'] == sector]
    return subs_df



def subset_fuel(df, fuel):
    """
    Return a subset of an emissions DataFrame where the value in the 'fuel'
    column is equal to that of the 'fuel' param
    
    Parameters
    ----------
    df : Pandas DataFrame
        DataFrame containing emission data
    sector : str
        sector used for subsetting
        
    Returns
    -------
    subs_df : Pandas DataFrame
        DataFrame containing only emissions data for the specified fuel
    """
    subs_df = df.loc[df['fuel'] == fuel]
    return subs_df



def subset_yr(df, yr):
    """
    Get a single year column from a DataFrame
    
    Parameters
    ----------
    df : Pandas DataFrame
        DataFrame containing emission data
    yr : int
        EF year of interest
        
     Returns
    -------
    sub_df : Pandas DataFrame
        DataFrame containing data for the specified year
    """
    yr_str = 'X{}'.format(yr)
    
    col_names = ['iso', 'sector', 'fuel', 'units']
    
    iso = df['iso']
    sector = df['sector']
    fuel = df['fuel']
    units = df['units']
    
    sub_df = df.loc[:, [yr_str]]
    
    # Re-introduce the iso, sector, fuel, & units columns to the beginning 
    # of the dataframe
    for idx, col in enumerate([iso, sector, fuel, units]):
        sub_df.insert(idx, col_names[idx], col)
    
    return sub_df
    


def subset_yr_span(df, yr, yr_rng=5):
    """
    Subset the DataFrame using a range of years
    
    Parameters
    ----------
    df : Pandas DataFrame
        DataFrame containing emission data
    yr : int
        EF year of interest
    yr_rng : int, optional
        Defines the range of years to subset
        Default is 5
        
    Returns
    -------
    sub_df : Pandas DataFrame
        DataFrame containing data within the range defined by yr +/ yr_rng
    """
    col_names = ['iso', 'sector', 'fuel', 'units']
    
    iso = df['iso']
    sector = df['sector']
    fuel = df['fuel']
    units = df['units']
    
    min_yr = yr - yr_rng
    max_yr = yr + yr_rng
    
    min_yr_str = "X{}".format(min_yr)
    max_yr_str = "X{}".format(max_yr)
    
    # Extract the columns from min_yr_str:max_yr_str
    sub_df = df.loc[:, min_yr_str:max_yr_str]
    
    # Re-introduce the iso, sector, fuel, & units columns to the beginning 
    # of the dataframe
    for idx, col in enumerate([iso, sector, fuel, units]):
        sub_df.insert(idx, col_names[idx], col)
    
    return sub_df



def filter_data_sector(df):
    """
    Filter the CEDS Emissions DataFrame to remove all emissions not related 
    to combustion
    
    Apply a regular expression to the 'sector' field in each DataFrame row to
    obtain a DataFrame containing only emission factor data pertaining to combustion
    sectors
    
    Parameters
    ----------
    df : Pandas DataFrame
        DataFrame containing CEDS CMIP6 emission data to be filteres
   
    Returns
    -------
    df_filtered : Pandas DataFrame
        DataFrame containing data only for the specified sector
        
    CEDS Working Sectors (as defined by Hoesly et al. 2018)
    -----
    * Combustion:       1A1 - 1A5
    * Non-combustion:   1A1bc, 1B1 - 1B7
    """
    sec_pattern = r'^1A[1-5]'
    sec_exclude = '1A1bc'
    
    # Remove sectors that don't begin with the '1A_' combustion prefix
    # OR begin with the '1A1bc' prefix, which is extremely similar to the 
    # combustion prefix but is a non-combustion sector
    df_filtered = df[(df['sector'].str.contains(sec_pattern)) & (df['sector'].str[:5] != sec_exclude)]
    
    return df_filtered



def reconstruct_ef_df(ef_df_actual, efsubset_obj, year_strs):
    logger = logging.getLogger('main')
    logger.info("Overwriting EF DataFrame values for year = 1970")
    
    sector = efsubset_obj.sector
    fuel   = efsubset_obj.fuel
    
    year_str_0 = year_strs[0]
    
    for idx, iso in enumerate(efsubset_obj.isos):
        # df.loc[df[<some_column_name>] == <condition>, [<another_column_name>]] = <value_to_add>
        ef_df_actual.loc[(ef_df_actual['iso'] == iso) & (ef_df_actual['sector'] == sector) &
                         (ef_df_actual['fuel'] == fuel), [year_str_0]] = efsubset_obj.ef_data[idx]
        
    return ef_df_actual
    
    
    
def reconstruct_ef_df_final(ef_df_actual, efsubset_obj, year_strs):
    logger = logging.getLogger('main')
    logger.info("Overwriting EF DataFrame values for years >= 1970\n")
    
    # X1970
    year_str_0 = year_strs[0]
    
    # Copy the 1970 column to the columns of years > 1970
    # MASSIVELY faster than repeating the above loop for every year
    for yr in year_strs[1:]:
        ef_df_actual[yr] = ef_df_actual[year_str_0]
        
    return ef_df_actual
    
    
    
def arr_to_csv(arr, out_path):
    import csv
    
    print('Writing {}...'.format(arr))
    
    with open(out_path, "wb") as fh:
        writer = csv.writer(fh)
        writer.writerows(arr)
    
    print("Done!")
    
    
    
def print_full_df(df):
    pd.set_option('display.max_rows', len(df))
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.float_format', '{:20,.4f}'.format)
    pd.set_option('display.max_colwidth', -1)
    print(df)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.float_format')
    pd.reset_option('display.max_colwidth')
    
    
    
    
def main():
    data_path = r"C:\Users\nich980\data\CEDS_CMIP6_Release_Archive\intermediate-output"
    
    gas = get_avail_species(data_path)
    gs = get_species(data_path)
    
    print(gas)
    print(gs)
    
    
#    print(get_file_for_species(data_path, "BC", "activity"))
#    print(get_file_for_species(data_path, "BC", "ef"))
#    print(get_file_for_species(data_path, "NH3", "activity"))
#    print(get_file_for_species(data_path, "NH3", "ef"))
#    print(get_file_for_species(data_path, "NMVOC", "activity"))
#    print(get_file_for_species(data_path, "NMVOC", "ef"))
    
    
    
    
    
    
    
if __name__ == '__main__':
    main()
    
    
