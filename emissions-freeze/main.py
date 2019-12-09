# -*- coding: utf-8 -*-
"""
Author: Matt Nicholson

"""
import copy
from os.path import join, isdir
from os import makedirs

import validate
import ceds_io
import plotting
import quick_stats
import efsubset

from sys import exit



def main():
    out_path_base = r"C:\Users\nich980\data\e-freeze\dat_out\imgs"
    
    data_path = r"C:\Users\nich980\data\CEDS_CMIP6_Release_Archive\intermediate-output"
#    f_name = "H.SO2_total_EFs_extended.csv"
    f_name = "H.NOx_total_EFs_extended.csv"
    
    fuels = ['biomass', 'brown_coal', 'coal_coke', 'diesel_oil',
             'hard_coal', 'heavy_oil', 'light_oil', 'natural_gas']
    
    plt_opts = {
                'show'          : False,
                'save'          : True,
                'out_path_base' : '',
                'out_path_abs'  : out_path_base,
                'plot_outliers' : False,
                'z_thresh'      : 3
               }
    
#    ef_files = ceds_io.fetch_ef_files(data_path)
    
    ef_df = ceds_io.read_ef_file(join(data_path, f_name))
    
    # Filter out all non-combustion sectors
#    ef_df = ceds_io.filter_data_sector(ef_df)      # get_sectors() already does this
    
#    sectors = ceds_io.get_sectors(ef_df)
    sector = '1A2g_Ind-Comb-textile-leather'
    fuel = 'diesel_oil'
    species = ceds_io.get_species_from_fname(f_name)
    year = 1970
    
    # Read the EF data into an EFSubset object
    ef_obj = efsubset.EFSubset(ef_df, sector, fuel, species, year)
    
    # Calculate the median of the EF values
    ef_median = quick_stats.get_ef_median(ef_obj)
    
    for i in range(2):
    
        ef_median = quick_stats.get_ef_median(ef_obj)
        
        # Compute a box cox transform for the EF data
        boxcox, lam = quick_stats.get_boxcox(ef_obj)
        ef_obj_boxcox = copy.deepcopy(ef_obj)
        ef_obj_boxcox.ef_data = boxcox
        
        # Identify outliers based on the box cox transform EF data
        outliers = quick_stats.get_outliers_zscore(ef_obj_boxcox)
        
        # Set the EF value of each idenfitied outlier to the median of the EF values
        for olr in outliers:
            ef_obj.ef_data[olr[2]] = ef_median
    
    quick_stats.plot_df(ef_obj, plt_opts)
    
    
    
    
#    import pandas as pd
#    p = r"C:\Users\nich980\data\e-freeze\dat_out\ef_stats\BC.comb_ef_stats.csv"
#    df = pd.read_csv(p, sep=',')
#    ceds_io.print_full_df(df)
    
if __name__ == '__main__':
    main()
            
            
            
            
            
            
            
            
            
            
