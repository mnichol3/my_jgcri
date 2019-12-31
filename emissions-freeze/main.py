# -*- coding: utf-8 -*-
"""
Author: Matt Nicholson

"""
#import copy
import logging
import numpy as np
from os.path import join, isdir, isfile
from os import mkdir, getcwd, listdir, remove
import pandas as pd

import ceds_io
import quick_stats
import efsubset

from sys import exit



def nuke_logs(target=None):
    cwd = getcwd()
    log_dir = join(cwd, "logs")
    
    if (target):
        log_name = "{}.log".format(target)
        log_files = [f for f in listdir(log_dir) if f == log_name]
        target_str = log_name
    else:
        log_files = [f for f in listdir(log_dir) if f.endswith(".log")]
        target_str = 'all logs'
    
    print('--- Removing {} from logs/ ---\n'.format(target_str))
   
    for f in log_files:
#        print("Deleting {}".format(f))
        remove(join(log_dir, f))



def setup_logger(log_name):
    nuke_logs(target=log_name)
    
    log_format = logging.Formatter("%(asctime)s %(levelname)6s: %(message)s", "%Y-%m-%d %H:%M:%S")
    
    cwd = getcwd()
    f_name = '{}.log'.format(log_name)
    
    f_dir = join(cwd, 'logs')
    local_dir = join('logs', f_name)
    
    if (not isdir(f_dir)):
        mkdir(f_dir)
        
    handler = logging.FileHandler(local_dir)
    handler.setFormatter(log_format)
        
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
    
#    logging.basicConfig(filename = local_dir, 
#                    format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s', 
#                    filemode = 'a',
#                    level=logging.INFO)
    
#    handler = logging.StreamHandler()
    logger.info("Log created!\n")
    
    return logger
    
    

def freeze_emissions(dirs, year, ef_files=None):
    data_path = dirs['dir_cmip6']
    out_path = dirs['dir_inter_out']
    
    main_log = logging.getLogger("main")
    main_log.info("In main::freeze_emissions()")
    main_log.info("data_path = {}".format(data_path))
    main_log.info("year = {}\n".format(year))
    
    # Get all Emission Factor filenames in the directory
    if (not ef_files):
        ef_files = ceds_io.fetch_ef_files(data_path)
        
    # Construct the column header strings for years >= 1970
    year_strs = ['X{}'.format(yr) for yr in range(1970, 2014 + 1)]
    
    # Begin for-loop over each species EF file
    for f_name in ef_files:
        
        species = ceds_io.get_species_from_fname(f_name)
        main_log.info("Processing species: {}".format(species))
        
        main_log.info("Loading EF DataFrame from {}".format(join(data_path, f_name)))
        ef_df = ceds_io.read_ef_file(join(data_path, f_name))
        
        # print(ef_df.shape)
        # exit(0)
        
        max_yr = ef_df.columns.values.tolist()[-1]
        
        # Get all non-combustion sectors
        sectors, fuels = ceds_io.get_sectors(ef_df)
        
        for sector in sectors:
            
            for fuel in fuels:
                
                main_log.info("--- Processing {}...{}...{}---".format(species, sector, fuel))
                
                print("Processing {}...{}...{}...".format(species, sector, fuel))
        
                # Read the EF data into an EFSubset object
                main_log.info("Subsetting EF DF for year {}".format(year))
                efsubset_obj = efsubset.EFSubset(ef_df, sector, fuel, species, year)
                
                if (efsubset_obj.ef_data.size != 0):
        
                    # Calculate the median of the EF values
                    ef_median = quick_stats.get_ef_median(efsubset_obj)
                    main_log.debug("EF data array median: {}".format(ef_median))
                    
                    # Use num_outlier_iters + 1 bc of how range() handles the upper bound
    #                for i in range(num_outlier_iters):
                    
    #                    ef_median = quick_stats.get_ef_median(ef_obj)
                        
                        # Compute a box cox transform for the EF data
    #                    boxcox, lam = quick_stats.get_boxcox(ef_obj)
    #                    ef_obj_boxcox = copy.deepcopy(ef_obj)
    #                    ef_obj_boxcox.ef_data = boxcox
                        
                        # Identify outliers based on the box cox transform EF data
                    main_log.info("Identifying outliers")
                    outliers = quick_stats.get_outliers_zscore(efsubset_obj)
                    
                    if (len(outliers) != 0):
                        main_log.info("Setting outlier values to median EF value")
                        
                        # Set the EF value of each idenfitied outlier to the median of the EF values
                        for olr in outliers:
                            efsubset_obj.ef_data[olr[2]] = ef_median
                    else:
                        main_log.info("No outliers were identified")
                    
                    # Overwrite the current EFs for years >= 1970
                    main_log.info("Overwriting original EF DataFrame with new EF values")
                    ef_df = ceds_io.reconstruct_ef_df(ef_df, efsubset_obj, year_strs)
                else:
                    main_log.warning("Subsetted EF dataframe is empty")
                
            # End fuel for-loop
        # End sector for-loop
        
        f_out = join(out_path, f_name)
        
        main_log.info("Writing resulting {} DataFrame to file".format(species))
        
        print('Writing final {} DataFrame to: {}\n'.format(species, f_out))
        ef_df.to_csv(f_out, sep=',', header=True, index=False)
        main_log.info("DataFrame written to {}\n".format(f_out))
        
    # End EF file for-loop
    main_log.info("Finished processing all species")
    main_log.info("Leaving main::freeze_emissions()\n")
    
    
    
def calc_emissions(dir_dict, em_species=None):
    """
    Calculate the hypothetical emissions from the frozen emissions and the CMIP6
    activity files
    
    Emissions = EF x Activity
    
    Parameters
    -----------
    dir_dict : dictionary of {str: str}
        Dictionary holding the paths to directories for the various files needed.
        Keys: ['dir_inter_out', 'base_dir_act', 'dir_inter_out']
        
    Return
    -------
    None, writes to file
    """
    logger = logging.getLogger("main")
    logger.info('In main::calc_emissions()')
    
    # Unpack for better readability
    dir_inter_out = dir_dict['dir_inter_out']
    base_dir_act = dir_dict['dir_cmip6']
    
    logger.info('Searing for available species in {}'.format(dir_inter_out))
    
    if (not em_species):
        em_species = ceds_io.get_avail_species(dir_inter_out)
    
    logger.info('Emission species found: {}\n{}'.format(len(em_species)))
    
    # Create list of strings representing year column headers
    data_col_headers = ['X{}'.format(i) for i in range(1750, 2015)]
    
    for species in em_species:
        info_str = 'Calculating frozen total emissions for {}\n{}'.format(species, "="*45)
        logger.info(info_str)
        print(info_str)
        
        # Get emission factor file for species
        logger.info('Fetching emission factor file from {}'.format(dir_inter_out))
        frozen_ef_file = ceds_io.get_file_for_species(dir_inter_out, species, "ef")
        
        # Get activity file for species
        logger.info('Fetching activity file from {}'.format(base_dir_act))
        try:
            activity_file = ceds_io.get_file_for_species(base_dir_act, species, "activity")
        except:
            err_msg = 'No activity file found for {}'.format(species)
            logger.error(err_msg)
            print(err_msg)
            continue
        
        ef_path = join(dir_inter_out, frozen_ef_file)
        act_path = join(base_dir_act, activity_file)
        
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
        
        if (ef_subs.shape != act_subs.shape):
            # Error is arising where ef_subs.shape = (55212, 265) &
            # act_subs.shape = (54772, 265).
            # ValueError will be raised by pandas
            logger.error('ValueError: ef_subs & act_subs could not be broadcast together')
            logger.debug('ef_subs.shape {}'.format(ef_subs.shape))
            logger.debug('act_subs.shape {}'.format(act_subs.shape))
        
        emissions_df = pd.DataFrame(ef_subs.values * act_subs.values,
                                    columns=ef_subs.columns, index=ef_subs.index)
        
        # Insert the meta ('iso', 'sector', 'fuel', 'units') columns at the 
        # beginning of the DataFrame
        logger.info('Concatinating meta_cols and emissions_df DataFrames along axis 1')
        emissions_df = pd.concat([meta_cols, emissions_df], axis=1)
       
        f_name = '{}_total_CEDS_emissions.csv'.format(species)
        
        f_out = join(dir_inter_out, f_name)
        
        info_str = 'Writing emissions DataFrame to {}'.format(f_out)
        logger.info(info_str)
        print('     {}\n'.format(info_str))
        
        emissions_df.to_csv(f_out, sep=',', header=True, index=False)
        logger.info('Finished calculating total emissions for {}'.format(species))
        
    # End species loop
    logger.info("Finished processing all species")
    logger.info('Leaving validate::calc_emissions()\n')
    
    
    
def main():
    ##### Log housekeeping #####
    # Delete any old log files
    # nuke_logs(tartet='main')
    
    # Set up new main log
    main_log = setup_logger('main')
    ############################
    
    year = 1970
    ef_files = ["H.SO2_total_EFs_extended.csv"]
    species = ["SO2"]
    
    """Dictionary holding the paths to the various dta directories
    
    Keys
    ----
    dir_inter_out : Path to the directory for the CEDS intermediate output 
                    files that this script produces.
                    Contains:
                       > *_total_CEDS_emissions.csv
                       > H.*_total_EFs_extended.csv
                       
    dir_cmip6 : Path to the directory that holds the original, unmodified 
                    CMIP6 emission factor (EF) files
                      
    """
    dir_dict = {
                'dir_cmip6': r"C:\Users\nich980\data\e-freeze\CMIP6-emissions\intermediate-output",
                'dir_inter_out': r"C:\Users\nich980\data\e-freeze\python-output\intermediate-output"
                }
    
    freeze_emissions(dir_dict, year) #, ef_files=ef_files)
    
    calc_emissions(dir_dict) #, em_species=species)
    
    
    
if __name__ == '__main__':
    main()
            
            
            
            
            
            
            
            
            
            
