# -*- coding: utf-8 -*-
"""
Author: Matt Nicholson

"""
#import copy
import logging
import numpy as np
from os.path import join, isdir, isfile
from os import mkdir, getcwd, listdir, remove

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
    
    

def main():
    num_outlier_iters = 1
    year = 1970
        
#    out_path_base = r"C:\Users\nich980\data\e-freeze\dat_out\imgs"
    data_path = r"C:\Users\nich980\data\CEDS_CMIP6_Release_Archive\intermediate-output"
#    f_name = "H.SO2_total_EFs_extended.csv"
#    f_name = "H.NOx_total_EFs_extended.csv"
    
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
    
    # Delete any old log files
    nuke_logs()
    
    # Create new log for main
    main_log = setup_logger('main')
    main_log.info("data_path = {}".format(data_path))
    main_log.info("num_outliers = {}".format(num_outlier_iters))
    main_log.info("year = {}\n".format(year))
    
    # Get all Emission Factor filenames in the directory
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
            
            # End fuel for-loop
        # End sector for-loop
            
        f_out = r"C:\Users\nich980\data\e-freeze\dat_out\ef_files"
        f_out = join(f_out, f_name)
        
        main_log.info("Writing resulting {} DataFrame to file".format(species))
        
        print('Writing final {} DataFrame to: {}'.format(species, f_out))
        ef_df.to_csv(f_out, sep=',', header=True, index=False)
        main_log.info("DataFrame written to {}\n".format(f_out))
        
    # End EF file for-loop
    main_log.info("Finished processing all species")
    main_log.info("Goodbye")
    
    
    
#    import pandas as pd
#    p = r"C:\Users\nich980\data\e-freeze\dat_out\ef_stats\BC.comb_ef_stats.csv"
#    df = pd.read_csv(p, sep=',')
#    ceds_io.print_full_df(df)
    
if __name__ == '__main__':
    main()
            
            
            
            
            
            
            
            
            
            
