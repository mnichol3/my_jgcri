#!/usr/bin/python2.7

"""
Author: Matt Nicholson
3 Jan 2020
"""
from os import getcwd, chdir, listdir
from os.path import join
import numpy as np
from netCDF4 import Dataset

orig_wd = getcwd()

ceds_dir = '/pic/projects/GCAM/mnichol/ceds/CEDS_Data'

print('Changing working directory to ' + ceds_dir)
chdir(ceds_dir)

gridded_ems_dir = join(".", "emission-archives", "CEDS_grids", "historical-emissions")

# Get the names of the openburning/biomass burning files
openburning_files = [f for f in listdir(gridded_ems_dir) if 'biomassburning' in f]

for obf in openburning_files:
    print('Reading ' + obf)
    
    f_path = join(gridded_ems_dir, obf)
    
    nc = Dataset(f_path, 'r+')
    
    species = nc.variable_id
    
    data = nc[species][:]
    
    west, east = np.split(data, 2, axis=2)
    
    new_data = np.concatenate((east, west), axis=2)
    
    nc[species][:] = new_data[:]
    
    nc.close()
    
print('Finished! Changing working directory back to ' + orig_wd)
chdir(orig_wd)