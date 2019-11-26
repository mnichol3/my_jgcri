# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 08:43:19 2019

@author: nich980
"""

import pandas as pd
import numpy as np

from os.path import join
from scipy import stats



def get_outliers_zscore(ef_df, sector, fuel, thresh=3):
    """
    Identify outliers using their Z-Scores
    
    Parameters
    ----------
    ef_df : Pandas DataFrame
        DataFrame containing an emission factors file
    sector : str
        CEDS emisions sector to subset
    fuel : str
        CEDS fuel to subset
        
    Returns
    -------
    outliers : list of tuple - (str, float, float)
        ISOs and their respective EFs & z-scores that have been identified as outliers
    """
    
    # Get a subset of the sector & fuel we're interested in
    ef_df = ef_df[ef_df['sector'] == sector]
    ef_df = ef_df[ef_df['fuel'] == fuel]
    
    isos = ef_df['iso'].tolist()
    ef_list = ef_df['X1970'].tolist()
    outliers = []
    
    print("Z-score thresh: {}".format(thresh))
    
    score = np.abs(stats.zscore(ef_list))
    
    bad_z = np.where(score > thresh)[0]
    
    for z_idx in bad_z:
        outliers.append((isos[z_idx], ef_list[z_idx], z_idx))
    
    return outliers



def get_outliers_std(ef_df, sector, fuel):
    """
    Identify outliers using the Standard Deviation Method
    
    All values that fall outside of 3 standard deviations of the mean data value
    will be flagged as outliers
    
    Parameters
    ----------
    ef_df : Pandas DataFrame
        DataFrame containing an emission factors file
    sector : str
        CEDS emisions sector to subset
    fuel : str
        CEDS fuel to subset
        
    Returns
    -------
    outliers : list of tuple - (str, float)
        ISOs and their respective EFs that have been identified as outliers
    """
    outliers = []
    
    # Get a subset of the sector & fuel we're interested in
    ef_df = ef_df[ef_df['sector'] == sector]
    ef_df = ef_df[ef_df['fuel'] == fuel]
    
    isos = ef_df['iso'].tolist()
    ef_list = ef_df['X1970'].tolist()
    outliers = []
    
    ef_std = np.std(ef_list)
    ef_mean = np.mean(ef_list)
    cutoff = ef_std * 3
    
    limit_lower = ef_mean - cutoff
    limit_upper = ef_mean + cutoff
    
    for idx, ef in enumerate(ef_list):
        if ((ef > limit_upper) or (ef < limit_lower)):
            outliers.append((isos[idx], ef))
    
    return outliers



def plot_df(ef_df, sector, fuel, year, species, plt_opts):
    """
    Make a scatter plot of an EF dataframe
    
    Parameters
    -----------
    ef_df : Pandas DataFrame
        DataFrame containing an emission factors file
    sector : str
        CEDS emisions sector to subset
    fuel : str
        CEDS fuel to subset
    year : int
        The year who's EFs we wish to subset
    species : str
        Emissions species who's EF data is represented in the EF DataFrame
    plt_opts : dict
        Plotting options 
    """
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    ef_df = ef_df[ef_df['sector'] == sector]
    ef_df = ef_df[ef_df['fuel'] == fuel]
    
    isos = ef_df['iso'].tolist()
    ef_list = ef_df['X{}'.format(year)].tolist()
    
    x = [i for i in range(len(isos))]
    y = ef_list
    
    ax.scatter(x, y, s=8)
    
    if (plt_opts['plot_outliers'] == True):
        outliers = get_outliers_zscore(ef_df, sector, fuel, thresh=plt_opts['z_thresh'])
        
        x_out = [i[2] for i in outliers]
        y_out = [j[1] for j in outliers]
        
        ax.scatter(x_out, y_out, marker="x", color="r", s=16)
    
    font_size = 10
    
    plt.title("Emission Factor for {} - {}".format(year, species), loc='left', fontsize=font_size)
    plt.title("Sector: {}, Fuel: {}".format(sector, fuel), loc='right', fontsize=font_size)
    
    plt.axis([0, len(isos), 0, 2])
    
    plt.xlabel("ISO")
    plt.ylabel("Emission Factor")
    plt.tight_layout()

    if (plt_opts['show'] == True):
        plt.show()
        
    if (plt_opts['save']):
        f_name = "{}.{}.{}.png".format(species, sector, fuel)
        f_path = join(plt_opts['out_path_abs'], f_name)
        plt.savefig(f_path, dpi=300)
    
    plt.close()
    
    

def main():
    
#    out_path_base = r"C:\Users\nich980\data\e-freeze\dat_out\imgs"
    out_path_base = r"C:\Users\nich980\data\e-freeze\dat_out\imgs\outliers-markup"
    f_path = r"C:\Users\nich980\data\CEDS_CMIP6_Release_Archive\intermediate-output"
    f_name = r"H.CO_total_EFs_extended.csv"
    
    year = 1970
    species = 'CO'
    
#    sector = '1A2b_Ind-Comb-Non-ferrous-metals'
#    fuel = 'hard_coal'
    sector = '1A3eii_Other-transp'
    fuel = 'hard_coal'
    
    plt_opts = {
                'show': False,
                'save': True,
                'out_path_base': '',
                'out_path_abs' : out_path_base,
                'plot_outliers' : True
               }
    
    f_path_abs = join(f_path, f_name)
    
    ef_df = pd.read_csv(f_path_abs, sep=",", header=0)
    
    thresh = 1
    
    plt_opts['z_thresh'] = thresh
    
    outliers = get_outliers_zscore(ef_df, sector, fuel, thresh=thresh)
#    outliers = get_outliers_std(ef_df, sector, fuel)
    
    for x in outliers:
        print(x)
    
    plot_df(ef_df, sector, fuel, year, species, plt_opts)
    
    
    
if __name__ == '__main__':
    main()