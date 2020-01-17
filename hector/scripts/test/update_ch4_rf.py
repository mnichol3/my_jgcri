"""
Author: Matt Nicholson
17 Jan 2020

This script contains equations for calculating co2, ch4, & n2o radiative forcing
obtained from Etminan et al., 2016

Full citation:
Etminan, M., Myhre, G., Highwood, E. J., and Shine, K. P. ( 2016),
Radiative forcing of carbon dioxide, methane, and nitrous oxide:
A significant revision of the methane radiative forcing,
Geophys. Res. Lett., 43, 12,614– 12,623, doi:10.1002/2016GL071930.
"""
import logging
import numpy as np
import pandas as pd

from os.path import join, isdir, isfile
from os import mkdir, getcwd, listdir, remove

#--------------------------- Constant Definitions -----------------------------#

# Path of the output from the nominal Hector run
nominal_output = r'C:\Users\nich980\data\hector\output\nominal_run.csv'

# Name of the log file
log_name = 'update_rf.log'

# Name of the calculated radiative forcing output file
df_outpath = 'updated_rf.csv'

year_start = 1745
year_end = 2300
rf_baseyear = 1750  # When to start reporting; by definition, all F=0 in this year

#------------------------ Radiative Forcing Equations -------------------------#

def calc_rf_ch4(m_0, m_curr, m_bar, n_bar):
    """
    Calculate the radiative forcing for CH4 (methane)
    
    Parameters
    ----------
    m_0 : float
        Initial ch4 concentration, in ppb
    m_curr : float
        Current ch4 concentration, in ppb
    m_bar : float
        Averaged ch4 concentration, in W m^-2 ppb^-1
    n_bar : float
        Averaged n2o concentration, in W m^-2 ppb^-1
        
    Return
    -------
    rf_ch4 : float
        Radiative forcing of ch4, in W m^-2
    """
    a = -1.3e-6     # W m^-2 ppb^-1
    b = -8.2e-6     # W m^-2 ppb^-1
    
    rf_ch4 = ( (a * m_bar) + (b * n_bar) + 0.043) * ( np.sqrt(m_curr) - np.sqrt(m_0) )
    return rf_ch4
    
    
def calc_rf_n2o(n_0, n_curr, c_bar, n_bar, m_bar):
    """
    Calculate the radiative forcing for N2O
    
    Parameters
    ----------
    n_0 : float
        Initial n2o concentration, in ppb
    n_curr : float
        Current n2o concentration, in ppb
    m_bar : float
        Averaged ch4 concentration, in W m^-2 ppb^-1
    n_bar : float
        Averaged n2o concentration, in W m^-2 ppb^-1
    c_bar : float
        Averaged co2 concentration, in W m^-2 ppm^-1
        
    Return
    -------
    rf_n2o : float
        Radiative forcing of n2o, in W m^-2
    """
    a = -8.0e-6     # W m^-2 ppm^-1
    b = 4.2e-6      # W m^-2 ppb^-1
    c = -4.9e-6     # W m^-2 ppb^-1
    
    rf_n20 = ( (a * c_bar) + (b * n_bar) + (c * m_bar) + 0.117) * ( np.sqrt(n_curr) - np.sqrt(n_0) )
    return rf_n20


def calc_rf_co2(c_0, c_curr, n_bar):
    """
    Calculate the radiative forcing for CO2
    
    Parameters
    ----------
    c_0 : float
        Initial co2 concentration, in ppm
    c_curr : float
        Current co2 concentration, in ppm
    n_bar : float
        Averaged n2o concentration, in W m^-2 ppb^-1
    
    Return
    -------
    rf_co2 : float
        Radiative forcing of co2, in W m^-2
    """
    a = -2.4e-7     # W m^-2 ppm^-1
    b = 7.2e-4      # W m^-2 ppm^-1
    c = -2.1e-4     # W m^-2 ppb^-1
    
    rf_co2 = ( (a * (c_curr - c_0)**2 ) + ( b * np.fabs(c_curr - c_0) ) + (c * n_bar) + 5.36 ) * ( np.log(c_curr / c_0) )
    return rf_co2


#----------------------------- Helper Functions -------------------------------#

def calc_nbar(n_0, n_curr):
    """
    Calculate the n2o concentration average between the historical n2o and
    current n2o concentrations
    
    Parameters
    ----------
    n_0 : float
        Historical n2o concentration, in ppm
    n_curr : float
        Current n2o concentration, in ppm
        
    Return
    ------
    n_bar : float
        Averaged concentration, in W m^-2 ppb^-1
    """
    n_bar = 0.5 * (n_0 + n_curr)
    return n_bar
    
    
def calc_cbar(c_0, c_curr):
    """
    Calculate the co2 concentration average between the historical co2 and
    current co2 concentrations
    
    Parameters
    ----------
    c_0 : float
        Historical co2 concentration, in ppm
    c_curr : float
        Current co2 concentration, in ppm
        
    Return
    ------
    c_bar : float
        Averaged concentration, in W m^-2 ppm^-1
    """
    c_bar = 0.5 * (c_0 + c_curr)
    return c_bar
    
    
def calc_mbar(m_0, m_curr):
    """
    Calculate the ch4 concentration average between the historical ch4 and
    current ch4 concentrations
    
    Parameters
    ----------
    m_0 : float
        Historical ch4 concentration, in ppm
    m_curr : float
        Current ch4 concentration, in ppm
        
    Return
    ------
    m_bar : float
        Averaged concentration, in W m^-2 ppb^-1
    """
    m_bar = 0.5 * (m_0 + m_curr)
    return m_bar
    
    
def read_nominal_output(f_in):
    """
    Read a .csv file containing data from a nominal hector run to compare to the
    radiative forcing calculated in the above equations
    
    Parameters
    ----------
    f_in : str
        Absolute path of the .csv file containing the nominal hector output
        
    Return
    ------
    df : Pandas DataFrame
    """
    col_types = {'year': int, 'variable': str, 'value': float}
    df = pd.read_csv(f_in, sep=',', header=0, dtype=col_types)
    return df
    
    
def get_nominal_conc(df, species):
    """
    Get the nominal hector concentration for a given species
    
    Parameters
    ----------
    df : Pandas DataFrame
        DataFrame containing output from a nominal hector run
    species : str
        Species to retrieve output for
    
    Return
    ------
    species_df : Pandas DataFrame
        Pandas DataFrame containing hector concentration output for the given
        species
    """
    species = species.upper()   # Ensure string is all uppercase
    
    # ensure correct string for atmospheric co2 concentration
    if (species == 'CO2'):
        species = 'Ca'
        
    species_df = df.loc[df['variable'] == species]
    return species_df


def get_nominal_rf(df, species):
    """
    Get the nominal hector radiative forcing for a given species
    
    Parameters
    ----------
    df : Pandas DataFrame
        DataFrame containing output from a nominal hector run
    species : str
        Species to retrieve output for
    
    Return
    ------
    species_df : Pandas DataFrame
        Pandas DataFrame containing hector radiative forcing output for the given
        species
    """
    species = species.upper()   # Ensure string is all uppercase
    species = 'F{}'.format(species)
    species_df = df.loc[df['variable'] == species]
    return species_df
    
    
def nuke_logs(target=None):
    """
    Remove previous logs for the log directory
    """
    cwd = getcwd()
    log_dir = join(cwd, "logs")
    
    if (isdir(log_dir)):
        if (target):
            log_files = [f for f in listdir(log_dir) if f == log_name]
            target_str = log_name
        else:
            log_files = [f for f in listdir(log_dir) if f.endswith(".log")]
            target_str = 'all logs'
        
        print('--- Removing {} from logs/ ---\n'.format(target_str))
       
        for f in log_files:
            remove(join(log_dir, f))


def setup_logger(log_name):
    nuke_logs(target=log_name)
    
    log_format = logging.Formatter("%(asctime)s %(levelname)6s: %(message)s", "%Y-%m-%d %H:%M:%S")
    
    cwd = getcwd()
    
    f_dir = join(cwd, 'logs')
    local_dir = join('logs', log_name)
    
    if (not isdir(f_dir)):
        mkdir(f_dir)
        
    handler = logging.FileHandler(local_dir)
    handler.setFormatter(log_format)
        
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
    logger.info("Log created!\n")
    
    return logger
    
#=========================== End Helper Functions =============================#

def main():
    # Remove old logs & initialize a new one 
    nuke_logs()
    log = setup_logger(log_name)
    
    # Set RF reporting start year
    year_start = rf_baseyear
    
    yr_span = (year_end - year_start) + 1
    
    # initialize dict val lists to their final size 
    rf_dict = {'year': [None] * yr_span,
               'rf_co2': [None] * yr_span,
               'rf_ch4': [None] * yr_span,
               'rf_n2o': [None] * yr_span
               }
    
    nominal_df = read_nominal_output(nominal_output)
    log.debug('Finished reading nominal hector output. DataFrame shape: {}'.format(nominal_df.shape))
    
    nominal_c = get_nominal_conc(nominal_df, 'co2')     # co2 concentration
    nominal_m = get_nominal_conc(nominal_df, 'ch4')     # ch4 concentration
    nominal_n = get_nominal_conc(nominal_df, 'n2o')     # n2o concentration
    
    # Obtain the initial concentrations for t=0 timestep
    c_0 = nominal_c.loc[nominal_c['year'] == year_start].value.iloc[0]
    m_0 = nominal_m.loc[nominal_m['year'] == year_start].value.iloc[0]
    n_0 = nominal_n.loc[nominal_n['year'] == year_start].value.iloc[0]
    
     # Log constants and such
    log.debug('nominal hector output path: {}'.format(nominal_output))
    log.debug('c_0 = {}'.format(c_0))
    log.debug('m_0 = {}'.format(m_0))
    log.debug('n_0 = {}'.format(n_0))
    log.debug('year_start = {}'.format(year_start))
    log.debug('year_end = {}'.format(year_end))
    log.debug('Initialized rf_dict value lists to length {}'.format(len(rf_dict['year'])))
    
    idx = 0
    # Max year = year_end + 1 due to how range() handles upper bounds
    for year in range(year_start, year_end + 1):
        info_str = 'Year = {}'.format(year)
        log.info(info_str)
        print(info_str)
        
        # Get the nominal concentrations for the current year
        c_curr = nominal_c.loc[nominal_c['year'] == year].value.iloc[0]
        m_curr = nominal_m.loc[nominal_m['year'] == year].value.iloc[0]
        n_curr = nominal_n.loc[nominal_n['year'] == year].value.iloc[0]
        
        log.debug('Concentration co2 = {}'.format(c_curr))
        log.debug('Concentration ch4 = {}'.format(m_curr))
        log.debug('Concentration n2o = {}'.format(n_curr))
        
        # Calculate the averaged concentrations
        c_bar = calc_cbar(c_0, c_curr)
        m_bar = calc_mbar(m_0, m_curr)
        n_bar = calc_nbar(n_0, n_curr)
        
        log.debug('c_bar = {}'.format(c_bar))
        log.debug('m_bar = {}'.format(m_bar))
        log.debug('n_bar = {}'.format(n_bar))
        
        # Calculate the radiative forcings for the current year
        rf_c = calc_rf_co2(c_0, c_curr, n_bar)                  # co2 RF
        rf_m = calc_rf_ch4(m_0, m_curr, m_bar, n_bar)           # ch4 RF
        rf_n = calc_rf_n2o(n_0, n_curr, c_bar, n_bar, m_bar)    # n2o RF
        
        log.debug('RF co2 = {}'.format(rf_c))
        log.debug('RF ch4 = {}'.format(rf_m))
        log.debug('RF n2o = {}'.format(rf_n))
        
        log.debug('Adding RF vals to rf_dict')
        
        rf_dict['year'][idx] = year
        rf_dict['rf_co2'][idx] = rf_c     # co2 RF
        rf_dict['rf_ch4'][idx] = rf_m     # ch4 RF
        rf_dict['rf_n2o'][idx] = rf_n     # n2o RF
        
        idx += 1
        
        log.info('Finished calculating RF for year {}\n'.format(year))
        
    log.info('Finished calculating RF for all years\n')

    log.info('Constructing final DataFrame from rf_dict')
    rf_df = pd.DataFrame.from_dict(rf_dict, orient='columns')
    
    info_str = 'Writing final DataFrame to {}'.format(df_outpath)
    log.info(info_str)
    print(info_str)
    
    rf_df.to_csv(df_outpath, sep=',', header=True, index=False)
    
    log.info('Finished calculating & reporting radiative forcings. Goodbye!')
    
        

if __name__ == '__main__':
    main()