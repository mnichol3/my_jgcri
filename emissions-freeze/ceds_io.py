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
from os import listdir, getcwd

import create_comb_sector_df


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
            
    logger = logging.getLogger('main')
    
    f_name = bases[f_type].format(species)
    f_abs = join(dir_path, f_name)
    
    logger.debug("Searching for file '{}'".format(f_name))
    
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
    logger = logging.getLogger('main')
    logger.info("In ceds_io::get_sectors")
    
    if (comb_filter):
        logger.debug("Calling filter_data_sector")
        df = filter_data_sector(df)
    
    sectors = df['sector'].unique().tolist()
    fuels = df['fuel'].unique().tolist()
    
    logger.debug("len(sectors) = {}".format(len(sectors)))
    logger.debug("len(fuels) = {}".format(len(fuels)))
    
    return (sectors, fuels)
    
    
    
def get_isf(df, iso):
    sectors = list(df[df['iso'] == iso]['sectors'])
    fuels = list(df[df['iso'] == iso]['fuel'])
    return zip(sectors, fuels)



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
        
    Combustion sectors (defined by Master_Fuel_Sector_List.xlsx)
    -------------------
    1A1a_Electricity-public
    1A1a_Electricity-autoproducer
    1A1a_Heat-production
    1A2a_Ind-Comb-Iron-steel
    1A2b_Ind-Comb-Non-ferrous-metals
    1A2c_Ind-Comb-Chemicals
    1A2d_Ind-Comb-Pulp-paper
    1A2e_Ind-Comb-Food-tobacco
    1A2f_Ind-Comb-Non-metalic-minerals
    1A2g_Ind-Comb-Construction
    1A2g_Ind-Comb-transpequip
    1A2g_Ind-Comb-machinery
    1A2g_Ind-Comb-mining-quarying
    1A2g_Ind-Comb-wood-products
    1A2g_Ind-Comb-textile-leather
    1A2g_Ind-Comb-other
    1A3ai_International-aviation
    1A3aii_Domestic-aviation
    1A3b_Road
    1A3c_Rail
    1A3di_International-shipping
    1A3dii_Domestic-navigation
    1A3eii_Other-transp
    1A4a_Commercial-institutional
    1A4b_Residential
    1A4c_Agriculture-forestry-fishing
    1A5_Other-unspecified
    """
    if (not isfile('combustion_sectors.csv')):
        print( ("Warning: Combustion sector csv not found in current directory. "
                "Calling create_comb_sector_df.py to create the file.\n"
                "Please ensure the variable 'ceds_dir' in create_comb_sector_df.py "
                "contains the correct path to your local CEDS directory") )
                
        dir_dict = create_comb_sector_df.parse_dir_dict()
        dir_dict['out_dir'] = getcwd()
        
        _, comb_df = create_comb_sector_df.create_csv(dir_dict)
    else:
        comb_df = pd.read_csv('combustion_sectors.csv', sep=',', header=0)
    
    # Construct a list of combustion sectors from the DataFrame
    comb_sectors = comb_df['sector'].values.tolist()
    
    # Create a new DataFrame containing only combustion sectors from the input dataframe
    df_filtered = df.loc[df['sector'].isin(comb_sectors)]
    
    return df_filtered



def reconstruct_ef_df(ef_df_actual, efsubset_obj, year_strs):
    logger = logging.getLogger('main')
    logger.info("Constructing final EF DataFrame")
    
    sector = efsubset_obj.sector
    fuel   = efsubset_obj.fuel
    
    logger.debug("Sector = {}; Fuel = {}".format(sector, fuel))
    
    # for year_str in year_strs:
        # for idx, iso in enumerate(efsubset_obj.isos):
            #df.loc[df[<some_column_name>] == <condition>, [<another_column_name>]] = <value_to_add>
            # logger.debug("iso = {}; EF = {}; year = {}".format(iso, efsubset_obj.ef_data[idx], year_str[1:]))
            
            # Locate the row of the CMIP6 EF DataFrame with the corresponding 
            # iso, sector, & fuel values and overwrite its EF values
            # ef_df_actual.loc[(ef_df_actual['iso'] == iso) & (ef_df_actual['sector'] == sector) &
                             # (ef_df_actual['fuel'] == fuel), [year_str]] = efsubset_obj.ef_data[idx]
                             
    for idx, iso in enumerate(efsubset_obj.isos):
        # df.loc[df[<some_column_name>] == <condition>, [<another_column_name>]] = <value_to_add>
        
        # For the CMIP6 EF DataFrame row corresponding to the given iso, sector,
        # and fuel, overwrite the values for years >= 1970 with the frozen EF 
        ef_df_actual.loc[(ef_df_actual['iso'] == iso) &
                         (ef_df_actual['sector'] == sector) &
                         (ef_df_actual['fuel'] == fuel),
                         year_strs] = efsubset_obj.ef_data[idx]
        
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
    
    
