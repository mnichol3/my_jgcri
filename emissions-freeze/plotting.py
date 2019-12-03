# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 13:01:30 2019

@author: nich980
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

from os.path import join, isdir
from os import makedirs

import validate
import ceds_io

from quick_stats import get_outliers_zscore, get_outliers_iqr

from sys import exit

plt.ioff()



def plot_ef(ef_df, fuels, plt_opts):
    """
    Plot the EF for a given sector, fuel, and species. 
    
    Params
    -------
    ef_df : Pandas DataFrame
        DataFrame containing Emission Factor data
    fuels : list of str
        List of CEDS fuels
    plt_opts : dict
        Plotting options
    """
    
    print('\nSubsetting DataFrame for years {}-{}\n'.format(1950, 1990))
    ef_df = ceds_io.subset_yr_span(ef_df, 1970, yr_rng=20)
    
    isos = ceds_io.get_isos(ef_df)
    sectors = ceds_io.get_sectors(ef_df)
    species = ceds_io.get_species_from_fname(plt_opts['f_in'])
#        isos = validate.get_isos(ef_df)
    
    if (species == -1):
        raise ValueError("Illegal species value encountered for {}".format(plt_opts['f_in']))
    
        for group in validate.chunker(isos, 10):
            iso_f = group[0]
            iso_l = group[-1]
            iso_path = "{}-{}".format(iso_f, iso_l)
        
#            out_path = join(plt_opts['out_path'], species)
            out_path = join(plt_opts['out_path'], "1950-1990", species, iso_path)
            
            plt_opts['out_path'] = out_path
            plt_opts['iso_path'] = iso_path
            plt_opts['iso_list'] = group
            
            # Make the species subdirectory in the parent out_path dir if it doesn't 
            # already exist
            if (not isdir(out_path)):
                makedirs(out_path)
            
            for sector in sectors:
                for fuel in fuels:
                    print("Plotting -- {} -- {} -- {} --".format(species, sector, fuel))
                    _plot_ef(ef_df, sector, fuel, species, plt_opts)

    
    
def _plot_ef(ef_df, sector, fuel, species, plt_opts):
    """
    
    Params
    ------
    ef_df : Pandas DataFrame
        DataFrame of emission factor data
    sec_args : list of str, optional
        [']
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    scatter = []
    iso_list = plt_opts['iso_list']
    
    ef_df = ceds_io.subset_sector(ef_df, sector)
    ef_df = ceds_io.subset_fuel(ef_df, fuel)
    ef_df = ceds_io.subset_iso(ef_df, iso_list)
    
    ef_df = ef_df.drop(['iso', 'sector', 'fuel', 'units'], axis=1)
    
    if (plt_opts['yr_rng'] is not None):
        yr_min, yr_max = plt_opts['yr_rng']
        yr_max += 1
    else:
        yr_min = 1750
        yr_max = 2015
    
    x = [yr for yr in range(yr_min, yr_max)]
    
    for idx, row in ef_df.iterrows():
        y = row.values
        curr_scat = ax.scatter(x, y, s=2)
        scatter.append(curr_scat)
    
    font_size = 10
    
    plt.title("Emission Factor for {}".format(species), loc='left', fontsize=font_size)
    plt.title("Sector: {}, Fuel: {}".format(sector, fuel), loc='right', fontsize=font_size)
    
    plt.axis([yr_min, yr_max, 0, 1.0])
    
    plt.xlabel("Year")
    plt.ylabel("Emission Factor")
    
    if (plt_opts['iso_path'] is not None):
#        isof, iso_l = plt_opts['iso_path'].split('-')
        lgd = plt.legend(iso_list, loc='center left', bbox_to_anchor=(1, 0.5))
        
        for handle in lgd.legendHandles:
            handle._sizes = [30]
        bbox_ea = (lgd,)
    else:
        bbox_ea = None
    
    if (plt_opts['show'] == True):
        plt.show()
        
    if (plt_opts['save']):
        f_name = "{}.{}.{}.png".format(species, sector, fuel)
        f_path = join(plt_opts['out_path'], f_name)
        plt.savefig(f_path, dpi=300, bbox_extra_artists=bbox_ea, bbox_inches='tight')
    
    plt.close()
    
    
    
def plot_ef_distro(ef_df, year, fuels, plt_opts):
    
    # Get a dataframe where the only year data column is 'year'
    ef_df = ceds_io.subset_yr(ef_df, year)
    
    sectors = ceds_io.get_sectors(ef_df)
    species = ceds_io.get_species_from_fname(plt_opts['f_in'])
    
    if (species == -1):
            raise ValueError("Illegal species value encountered for {}".format(plt_opts['f_in']))
    
    if (plt_opts['mark_outliers']):
        dir_name = "distro-marked"
    else:
        dir_name = "distro"
        
    out_path = join(plt_opts['out_path_base'], dir_name, '{}-iqr_2.0'.format(str(year)), species)
    plt_opts['out_path_abs'] = out_path
    
    if (not isdir(out_path)):
            makedirs(out_path)
            
    for sector in sectors:
            for fuel in fuels:
                print("Plotting distro -- {} -- {} -- {} -- {} --".format(year, species, sector, fuel))
                _plot_ef_distro(ef_df, year, sector, fuel, species, plt_opts)
               
                

def _plot_ef_distro(ef_df, year, sector, fuel, species, plt_opts):
    """
    Helper function called by plot_ef_distro. Handles the actual plotting
    
    Parameters
    ----------
    ef_df   : Pandas DataFrame
        EF DataFrame
    sector  : str
    fuel    : str
    species : str
    plt_opts : dict
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    
    ef_df = ceds_io.subset_sector(ef_df, sector)
    ef_df = ceds_io.subset_fuel(ef_df, fuel)
    
    isos = list(ef_df['iso'])
    
    # Write the ISO strings and their representative ints to text file
#    with open(r"C:\Users\nich980\data\e-freeze\dat_out\iso_list.txt", "w") as fh:
#        for idx, iso in enumerate(isos):
#            str_idx = str(idx)
#            fh.write("{} {}\n".format(str_idx.ljust(3, ' '), iso))
#    
#    exit(0)
    
    
    x = [i for i in range(len(isos))]
    
    y = list(ef_df['X{}'.format(year)])
    
    ax.scatter(x, y, s=8, zorder=1)
    
    if (plt_opts['mark_outliers']):
#        outliers = get_outliers_zscore(ef_df, sector, fuel, thresh=plt_opts['z_thresh'])
        outliers = get_outliers_iqr(ef_df, sector, fuel, outlier_const=2)
        
        x_out = [i[2] for i in outliers]
        y_out = [j[1] for j in outliers]
        
        ax.scatter(x_out, y_out, marker="x", color="r", s=16, zorder=2)
    
    font_size = 10
    
    plt.title("Emission Factors for {} - {}".format(year, species), loc='left', fontsize=font_size)
    plt.title("Sector: {}, Fuel: {}".format(sector, fuel), loc='right', fontsize=font_size)
    
    max_ef= max(y)
    x_max = max_ef + (max_ef * 0.1)
    
    plt.axis([0, len(isos), 0, x_max])
    
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
    
    
    
def plot_histo(ef_df, year, fuels, plt_opts):
    
#    ef_df = ceds_io.subset_yr(ef_df, year)
    
    try:
        num_bins = plt_opts['num_bins']
    except:
        print('num_bins not set. Defaulting to 20')
        num_bins = 20
    
    sectors = ceds_io.get_sectors(ef_df)
    species = ceds_io.get_species_from_fname(plt_opts['f_in'])
    
    if (species == -1):
            raise ValueError("Illegal species value encountered for {}".format(plt_opts['f_in']))
            
    out_path = join(plt_opts['out_path_base'], "histo", str(year), species)
    plt_opts['out_path_abs'] = out_path
    
    if (not isdir(out_path)):
            makedirs(out_path)
            
    for sector in sectors:
            for fuel in fuels:
                print("Plotting histogram -- {} -- {} -- {} -- {} --".format(year, species, sector, fuel))
                _plot_histo(ef_df, year, sector, fuel, species, num_bins, plt_opts)



def _plot_histo(ef_df, year, sector, fuel, species, num_bins, plt_opts):
    fig, ax = plt.subplots(figsize=(8, 8))
    
    font_size = 10
    
    ef_df = ceds_io.subset_sector(ef_df, sector)
    ef_df = ceds_io.subset_fuel(ef_df, fuel)
    
    ef_data = ef_df['X{}'.format(year)]
    
    n, _, _ = plt.hist(ef_data, num_bins, facecolor='blue', edgecolor='black', alpha=0.5)
    
    plt.title("Emission Factors for {} - {}".format(year, species), loc='left', fontsize=font_size)
    plt.title("Sector: {}, Fuel: {}".format(sector, fuel), loc='right', fontsize=font_size)
    
#    plt.axis([0, max(n), 0, 1.0])
    
    plt.xlabel("Emission Factor")
    plt.ylabel("Frequency")
    plt.tight_layout()

    if (plt_opts['show'] == True):
        plt.show()
        
    if (plt_opts['save']):
        f_name = "{}.{}.{}.png".format(species, sector, fuel)
        f_path = join(plt_opts['out_path_abs'], f_name)
        plt.savefig(f_path, dpi=300)
    
    plt.close()
    
    
    
def plot_prob(ef_df, year, fuels, plt_opts):
    
    sectors = ceds_io.get_sectors(ef_df)
    species = ceds_io.get_species_from_fname(plt_opts['f_in'])
    
    try:
        num_bins = plt_opts['num_bins']
    except:
        print('num_bins not set. Defaulting to 20')
        num_bins = 20
    
    if (species == -1):
            raise ValueError("Illegal species value encountered for {}".format(plt_opts['f_in']))
            
    out_path = join(plt_opts['out_path_base'], 'prob', str(year), species)
    plt_opts['out_path_abs'] = out_path
    
    if (not isdir(out_path)):
            makedirs(out_path)
            
    for sector in sectors:
            for fuel in fuels:
                print("Plotting histogram -- {} -- {} -- {} -- {} --".format(year, species, sector, fuel))
                _plot_prob(ef_df, year, sector, fuel, species, num_bins, plt_opts)
                
                
                
def _plot_prob(ef_df, year, sector, fuel, species, num_bins, plt_opts):
    fig, ax = plt.subplots(figsize=(8, 8))
    
    font_size = 10
    
    ef_df = ceds_io.subset_sector(ef_df, sector)
    ef_df = ceds_io.subset_fuel(ef_df, fuel)
    
    ef_data = ef_df['X{}'.format(year)]
    
    counts, start, dx, _ = scipy.stats.cumfreq(ef_data, numbins=num_bins)

    x = np.arange(counts.size) * dx + start
    
    plt.plot(x, counts, 'ro')
    
    plt.title("Emission Factors for {} - {}".format(year, species), loc='left', fontsize=font_size)
    plt.title("Sector: {}, Fuel: {}".format(sector, fuel), loc='right', fontsize=font_size)
    
    plt.xlabel('Emission Factor')
    plt.ylabel('Cumulative Frequency')
    plt.tight_layout()

    if (plt_opts['show'] == True):
        plt.show()
        
    if (plt_opts['save']):
        f_name = "{}.{}.{}.png".format(species, sector, fuel)
        f_path = join(plt_opts['out_path_abs'], f_name)
        plt.savefig(f_path, dpi=300)
    
    plt.close()
    
    
    
def plot_prob_histo(ef_df, year, fuels, plt_opts):
    try:
        num_bins = plt_opts['num_bins']
    except:
        print('num_bins not set. Defaulting to 20')
        num_bins = 20
    
    sectors = ceds_io.get_sectors(ef_df)
    species = ceds_io.get_species_from_fname(plt_opts['f_in'])
    
    if (species == -1):
            raise ValueError("Illegal species value encountered for {}".format(plt_opts['f_in']))
            
    out_path = join(plt_opts['out_path_base'], "prob-histo", str(year), species)
    plt_opts['out_path_abs'] = out_path
    
    if (not isdir(out_path)):
            makedirs(out_path)
            
    for sector in sectors:
            for fuel in fuels:
                print("Plotting histogram -- {} -- {} -- {} -- {} --".format(year, species, sector, fuel))
                _plot_prob_histo(ef_df, year, sector, fuel, species, num_bins, plt_opts)
                
                
                
def _plot_prob_histo(ef_df, year, sector, fuel, species, num_bins, plt_opts):
    fig, ax = plt.subplots(figsize=(8, 8))
    
    font_size = 10
    
    ef_df = ceds_io.subset_sector(ef_df, sector)
    ef_df = ceds_io.subset_fuel(ef_df, fuel)
    
    ef_data = ef_df['X{}'.format(year)]
    
    ef_data = ef_df['X{}'.format(year)]
    
    counts, start, dx, _ = scipy.stats.cumfreq(ef_data, numbins=num_bins)
    x = np.arange(counts.size) * dx + start
    
    n, _, _ = plt.hist(ef_data, num_bins, facecolor='blue', edgecolor='black', alpha=0.5)
    
    plt.plot(x, counts, '-ro')
    
    plt.title("Emission Factors for {} - {}".format(year, species), loc='left', fontsize=font_size)
    plt.title("Sector: {}, Fuel: {}".format(sector, fuel), loc='right', fontsize=font_size)
    
    plt.xlabel('Emission Factor')
    plt.ylabel('Cumulative Frequency')
#    plt.legend(loc='best')
    plt.tight_layout()

    if (plt_opts['show'] == True):
        plt.show()
        
    if (plt_opts['save']):
        f_name = "{}.{}.{}.png".format(species, sector, fuel)
        f_path = join(plt_opts['out_path_abs'], f_name)
        plt.savefig(f_path, dpi=300)
    
    plt.close()
  
    
    
def main():
    out_path_base = r"C:\Users\nich980\data\e-freeze\dat_out\imgs"
    
    data_path = r"C:\Users\nich980\data\CEDS_CMIP6_Release_Archive\intermediate-output"
#    f_name = "H.SO2_total_EFs_extended.csv"
    
    ef_files = ceds_io.fetch_ef_files(data_path)
    
#    ef_files= [x for x in ef_files if (".OC" in x or ".SO2" in x)]
    
    fuels = ['biomass', 'brown_coal', 'coal_coke', 'diesel_oil',
             'hard_coal', 'heavy_oil', 'light_oil', 'natural_gas']
    
    plt_opts = {
                'show': False,
                'save': True,
                'out_path_base': out_path_base,
                'yr_rng': (0,0),
                'mark_outliers': True,
                'z_thresh': 2,
                'f_in' : '',
                'num_bins': 50
               }
    
    for f in ef_files:
        
        plt_opts['f_in'] = f
        
        ef_path = join(data_path, f)
    
        ef_df = ceds_io.read_ef_file(ef_path)
        
        ef_df = ceds_io.filter_data_sector(ef_df)
        
        plot_ef_distro(ef_df, 1970, fuels, plt_opts)

        
#        plot_histo(ef_df, 1970, fuels, plt_opts)
        
#        plot_prob(ef_df, 1970, fuels, plt_opts)
        
#        plot_prob_histo(ef_df, 1970, fuels, plt_opts)
        
    
if __name__ == '__main__':
    main()
