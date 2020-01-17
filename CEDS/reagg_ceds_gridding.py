"""
Reaggrigate CEDS historical openburning gridded data from 25 km (0.25 deg) res
to 50 km (0.5 deg) res. 

However, the re-gridded files contain longitude values [0, 359.5] instead of
[-179.75, 179.75], so we must overwrite the re-gridded netCDF longitude variable
in order to properly plot the gridded data

cdo CLI command to regrid a 0.5 x 0.5 deg grid as 0.25 x 0.25:
$ cdo remapnn,r1440x720 in.nc out.nc
(https://stackoverflow.com/questions/21152308/how-to-change-the-resolution-or-regrid-data-in-r)

Author: Matt Nicholson
3 Jan 2020
"""
import logging
import numpy as np
from os.path import join, isdir, isfile
from os import listdir, makedirs, getcwd, remove
from netCDF4 import Dataset

################################################################################
################ Remove previous log files and create a new one ################
################################################################################
def nuke_logs(log_file):
    
    if (isfile(log_file)):
        print('--- Removing {} ---'.format(log_file))
        remove(log_file)
   
        
        
def init_logger():
    log_name = 'reagg_ceds_gridding.log'
    
    log_format = logging.Formatter("%(asctime)s %(levelname)6s: %(message)s", "%Y-%m-%d %H:%M:%S")
    
    cwd = getcwd()
    
    # Directory that holds the log files
    logs_dir = join(cwd, 'logs')
    
    # Absolute path of the log file
    log_file = join(logs_dir, log_name)
    
    # Delete old log file
    nuke_logs(log_file)
    
    if (not isdir(logs_dir)):
        print('Creating directory {}'.format(logs_dir))
        makedirs(logs_dir)
        
    handler = logging.FileHandler(log_file)
    handler.setFormatter(log_format)
        
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
    logger.info("Log created!\n")
    
    return logger
    
################################################################################
################################################################################
################################################################################


logger = init_logger()
    
# Path of the parent directory
dir_path = r"C:\Users\nich980\code\temp"

# Path of the directory holding the files we need to modify
dir_in = join(dir_path, "re-grid")

# Log some stuff
logger.info('Current directory {}'.format(getcwd()))
logger.debug('Gridding netCDF parent directory {}'.format(dir_path))
logger.debug('Gridding netCDF input directory {}'.format(dir_in))

### Construct the correct 0.5 degree grid longitude values
min_lon = -179.75
max_lon = 179.75
d_lon = 0.5

logger.debug('Corrected longitude min {}'.format(min_lon))
logger.debug('Corrected longitude max {}'.format(max_lon))
logger.debug('Corrected longitude delta_lon {}'.format(d_lon))


# Add 0.5 to max_lon due to how arange handles upper bounds
correct_lons = np.arange(min_lon, max_lon + 0.5, d_lon)

logger.debug('Corrected longitude shape {}'.format(correct_lons.shape))

# Sanity checks
assert correct_lons.shape == (720,), "Invalide new longitude variable shape"
assert min(correct_lons) == -179.75, "Invalid new longitude variable minimum"
assert max(correct_lons) == 179.75, "Invalid new longitude variable maximum"
logger.debug('correct_lons assertions passed')

nc_ref_f = 'BC-em-anthro_input4MIPs_emissions_CMIP_CEDS-2017-05-18_gn_185101-189912.nc'
nc_ref = join(dir_path, nc_ref_f)

# logger.debug('Opening netCDF ref file {}'.format(nc_ref_f))

# nc_ref = Dataset(nc_ref, 'r')

# ref_keys = nc_ref.variables.keys()

logger.debug('Sanity checking nc_ref variable keys')
assert 'lon_bnds' in ref_keys, "'lon_bnds' not found in nc_ref variable keys"
assert 'lat_bnds' in ref_keys, "'lat_bnds' not found in nc_ref variable keys"
logger.debug("'lon_bnds' & 'lat_bnds' located in nc_ref variable keys")

### Loop over all the files in the input directory
for f_in in listdir(dir_in):
    info_str = '--- Processing {} ---'.format(f_in)
    print(info_str)
    logger.info(info_str)
    
    f_path = join(dir_in, f_in)
    
    # Read the netcdf file
    nc = Dataset(f_path, 'r+')
    
    # Initial sanity checks
    assert nc['lon'][:].shape == (720,), "Invalide longitude variable in {}".format(f_in)
    assert min(nc['lon'][:]) == 0, "Invalid longitude variable minimum in {}".format(f_in)
    assert max(nc['lon'][:]) == 359.5, "Invalid new longitude variable maximum in {}".format(f_in)
    logger.debug('Pre assertions passed')
    
    # Overwrite the longitude values with the correct ones
    logger.info('Overwriting netCDF longitude values')
    nc['lon'][:] = correct_lons[:]
    
    # Final sanity checks
    assert nc['lon'][:].shape == (720,), "Invalide longitude variable in {}".format(f_in)
    assert min(nc['lon'][:]) == -179.75, "Invalid longitude variable minimum in {}".format(f_in)
    assert max(nc['lon'][:]) == 179.75, "Invalid new longitude variable maximum in {}".format(f_in)
    logger.debug('Post assertions passed')
    
    ### Add lat_bnds & lon_bnds variables to re-gridded netCDF
    
    ## Create new 'bound' dimension for 'lat_bnds' & 'lon_bnds' to use
    # logger.debug("Copying nc_ref 'bound' dimension")
    # bound_dim = nc_ref.dimensions['bound']
    # nc.createDimension('bound',
                      # (len(bound_dim) if not bound_dim.isunlimited() else None))
    
    # for new_var in ['lat_bnds', 'lon_bnds']:
        # logger.debug("Adding nc_ref '{}' variable to current netCDF file object".format(new_var))
    
        ## Create the new variable in the re-gridded netCDF
        # nc.createVariable(new_var, nc_ref[new_var].datatype, nc_ref[new_var].dimensions)
        # nc[new_var].setncatts(nc_ref[new_var].__dict__)
        # nc[new_var][:] = nc_ref[new_var][:]
    
    logger.info('Finished overwriting longitude values; closing file')
    
    nc.close()
    nc = None

## Close the reference netCDF file
# logger.debug('Closing nc_ref')
# nc_ref.close()
# nc_ref = None

logger.info('--- Finished processing all files ---')

# Final sanity checks cuz something aint right
for f_in in listdir(dir_in):
    info_str = '--- Final sanity check for {} ---'.format(f_in)
    logger.debug(info_str)
    
    f_path = join(dir_in, f_in)
    
    # Read the netcdf file
    nc = Dataset(f_path, 'r+')
    
    logger.debug('longitude min {}'.format(min(nc['lon'][:])))
    logger.debug('longitude max {}'.format(max(nc['lon'][:])))
    logger.debug('longitude shape {}'.format(nc['lon'][:].shape))

    # Initial sanity checks
    assert nc['lon'][:].shape == (720,), "Invalide longitude variable in {}".format(f_in)
    assert min(nc['lon'][:]) == -179.75, "Invalid longitude variable minimum in {}".format(f_in)
    assert max(nc['lon'][:]) == 179.75, "Invalid new longitude variable maximum in {}".format(f_in)
    
    assert nc['lon'][:][0] == -179.75, "Invalid new longitude [0] value in {}".format(f_in)
    assert nc['lon'][:][-1] == 179.75, "Invalid new longitude [0] value in {}".format(f_in)
    logger.debug('Final assertions passed')
    
    nc.close()
    nc = None

logger.info('--- Final assertions passed for all files ---')

