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
    
    var_data = nc[species][:].data
    
    var_data[var_data == nc[species].missing_value] = 0.0
    
    nc[species][:].data = var_data[:]
    
    nc.close()
    
print('Finished! Changing working directory back to ' + orig_wd)
chdir(orig_wd)
    
    