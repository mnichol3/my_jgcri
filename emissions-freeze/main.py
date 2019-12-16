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
#import validate
#import plotting



def nuke_logs():
    cwd = getcwd()
    log_dir = join(cwd, "logs")
    
    log_files = [f for f in listdir(log_dir) if f.endswith(".log")]
   
    for f in log_files:
#        print("Deleting {}".format(f))
        remove(join(log_dir, f))



def setup_logger(species):
    
    log_format = logging.Formatter("%(asctime)s %(levelname)6s: %(message)s", "%Y-%m-%d %H:%M:%S")
    
    cwd = getcwd()
    f_name = '{}.log'.format(species)
    
    f_dir = join(cwd, 'logs')
    local_dir = join('logs', f_name)
    
    if (not isdir(f_dir)):
        mkdir(f_dir)
        
    handler = logging.FileHandler(local_dir)
    handler.setFormatter(log_format)
        
    logger = logging.getLogger(species)
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
    data_path = dirs['dir_ef_actual']
    out_path = dirs['dir_ef_freeze']
        

    fuels = ['biomass', 'brown_coal', 'coal_coke', 'diesel_oil',
             'hard_coal', 'heavy_oil', 'light_oil', 'natural_gas']
        
#    plt_opts = {
#                'show'          : False,
#                'save'          : True,
#                'out_path_base' : '',
#                'out_path_abs'  : out_path_base,
#                'plot_outliers' : False,
#                'z_thresh'      : 3
#               }
    
    logger = logging.getLogger("main")
    main_log.info("In main::freeze_emissions()")
    main_log.info("data_path = {}".format(data_path))
    main_log.info("num_outliers = {}".format(num_outlier_iters))
    main_log.info("year = {}\n".format(year))
    
    # Get all Emission Factor filenames in the directory
    if (not ef_files):
        ef_files = ceds_io.fetch_ef_files(data_path)
    
    # Begin for-loop over each species EF file
    for f_name in ef_files:
        
        species = ceds_io.get_species_from_fname(f_name)
        main_log.info("Processing species: {}".format(species))
        
        main_log.info("Loading EF DataFrame from {}".format(join(data_path, f_name)))
        ef_df = ceds_io.read_ef_file(join(data_path, f_name))
        
        max_yr = ef_df.columns.values.tolist()[-1]
        
        species_log = setup_logger(species)
        
        # Get all non-combustion sectors
        for sector in ceds_io.get_sectors(ef_df):
            
            for fuel in fuels:
                
                main_log.info("Processing {}...{}...{}".format(species, sector, fuel))
                species_log.info("Processing {}...{}".format(sector, fuel))
                
                print("\nProcessing {}...{}...{}...".format(species, sector, fuel))
        
                # Read the EF data into an EFSubset object
                main_log.info("Subsetting EF DF for year {}".format(year))
                species_log.info("Subsetting EF DF for year {}".format(year))
                efsubset_obj = efsubset.EFSubset(ef_df, sector, fuel, species, year)
                
                if (not efsubset_obj.ef_data.size == 0):
        
                    # Calculate the median of the EF values
                    ef_median = quick_stats.get_ef_median(efsubset_obj)
                    species_log.debug("EF data array median: {}".format(ef_median))
                    
                    # Use num_outlier_iters + 1 bc of how range() handles the upper bound
    #                for i in range(num_outlier_iters):
                    
    #                    ef_median = quick_stats.get_ef_median(ef_obj)
                        
                        # Compute a box cox transform for the EF data
    #                    boxcox, lam = quick_stats.get_boxcox(ef_obj)
    #                    ef_obj_boxcox = copy.deepcopy(ef_obj)
    #                    ef_obj_boxcox.ef_data = boxcox
                        
                        # Identify outliers based on the box cox transform EF data
                    species_log.info("Identifying outliers")
                    main_log.info("Identifying outliers")
                    outliers = quick_stats.get_outliers_zscore(efsubset_obj)
                    
                    species_log.info("Setting outlier values to median EF value")
                    main_log.info("Setting outlier values to median EF value")
                    
                    # Set the EF value of each idenfitied outlier to the median of the EF values
                    for olr in outliers:
                        efsubset_obj.ef_data[olr[2]] = ef_median
                    
                    #quick_stats.plot_df(ef_obj, plt_opts)
                    
                    # Construct the column header strings for years >= 1970
                    year_strs = ['X{}'.format(yr) for yr in range(1970, int(max_yr[1:]) + 1)]
                    
                    # Overwrite the current EFs for years >= 1970
                    species_log.info("Overwriting original EF DataFrame with new EF values")
                    main_log.info("Overwriting original EF DataFrame with new EF values\n")
                    ef_df = ceds_io.reconstruct_ef_df(ef_df, efsubset_obj, year_strs)
                else:
                    species_log.warning("Subsetted EF dataframe is empty")
                
            # End fuel for-loop
        # End sector for-loop
        ef_df = reconstruct_ef_df_final(ef_df, efsubset_obj, year_strs)
        
        # Copy the 1970 column values to every column >= 1970
        reconstruct_ef_df_final
        f_out = r"C:\Users\nich980\data\e-freeze\dat_out\ef_files"
        f_out = join(f_out, f_name)
        
        main_log.info("Writing resulting {} DataFrame to file".format(species))
        species_log.info("Writing resulting DataFrame to file")
        
        print('Writing final {} DataFrame to: {}'.format(species, f_out))
        ef_df.to_csv(f_out, sep=',', header=True, index=False)
        main_log.info("DataFrame written to {}\n".format(f_out))
        species_log.info("DataFrame written to {}\n".format(f_out))
        
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
        Keys: ['base_dir_ef', 'base_dir_act', 'out_path_ems']
        
    Return
    -------
    None, writes to file
    """
    logger = logging.getLogger("main")
    logger.info('In main::calc_emissions()')
    
    # Unpack for better readability
    base_dir_ef = dir_dict['dir_ef_freeze']
    base_dir_act = dir_dict['dir_ef_actual']
    out_path_ems = dir_dict['out_path_ems']
    
    logger.info('Searing for available species in {}'.format(base_dir_ef))
    
    if (not em_species):
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
       
        f_name = '{}_total_CEDS_emissions.csv'.format(species)
        
        f_out = join(out_path_ems, f_name)
        
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
    # nuke_logs()
    
    # Set up new main log
    main_log = setup_logger('main')
    ############################
    
    year = 1970
    ef_files = ["H.CO2_total_EFs_extended.csv", "H.CH4_total_EFs_extended.csv"]
    species = ["CO2", "CH4"]
    
    dir_dict = {
                'dir_ef_actual': r"C:\Users\nich980\data\CEDS\CEDS\intermediate-output",
                'dir_ef_freeze': r"C:\Users\nich980\data\e-freeze\dat_out\ef_files",
                'out_path_ems' : r"C:\Users\nich980\data\e-freeze\dat_out\frozen_emissions"
                }
    
    # freeze_emissions(dir_dict, year, ef_files=ef_files)
    
    calc_emissions(dir_dict, em_species=species)
    
    
    
if __name__ == '__main__':
    main()
            
            
            
            
            
            
            
            
            
            
