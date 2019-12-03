# -*- coding: utf-8 -*-
"""
Author: Matt Nicholson

"""
from os.path import join, isdir
from os import makedirs

import validate
import ceds_io
import plotting

from sys import exit



def main():
#    out_path_base = r"C:\Users\nich980\data\e-freeze\dat_out\imgs\1950-1990"
    
#    data_path = r"C:\Users\nich980\data\CEDS_CMIP6_Release_Archive\intermediate-output"
#    f_name = "H.SO2_total_EFs_extended.csv"
#    
#    ef_files = ceds_io.fetch_ef_files(data_path)
#    
#    ef_df = ceds_io.read_ef_file(join(data_path, f_name))
#    
#    # Filter out all non-combustion sectors
#    ef_df = ceds_io.filter_data_sector(ef_df)
        
#    sub_df = validate.subset_yr(ef_df, 1970)
#    
#    print(sub_df)
   
    
#    ef_path = join(data_path, f_name)
#    
#    ef_df = ceds_io.read_ef_file(ef_path)
#    
#    isos = validate.get_isos(ef_df)
#    
#    for group in validate.chunker(isos, 8):
#        sub_df = validate.subset_iso(ef_df, group)
#        print(sub_df)
#        break
    
    
    import pandas as pd
    p = r"C:\Users\nich980\data\e-freeze\dat_out\ef_stats\BC.comb_ef_stats.csv"
    df = pd.read_csv(p, sep=',')
    ceds_io.print_full_df(df)
    
if __name__ == '__main__':
    main()
            
            
            
            
            
            
            
            
            
            
