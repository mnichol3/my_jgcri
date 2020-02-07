"""
Matt Nicholson
7 Feb 2020

This script contains functions to compare output from various versions of 
PNNL-JGCRI's Hector Simple Climate Model

"""
import pandas as pd
import matplotlib.pyplot as plt
from os.path import join, exists
from sys import platform

# ========================= Define HectorOutput Class ==========================

def Class HectorOutput
    """
    A simple class to represent a Hector output file
    
    Class Methods
    --------------
    __init__(abs_path, scenario, version, years=None, vars=None)
        Constructor
    _parse_output(self, vars=None, years=None)
        Determines which output file parsing method to call based on the Hector
        version that produced the output file.
    _parse_outputstream(self, vars=None, years=None)
        Reads a Hector output file produced by Hector's C++ outputstream functions
    _parse_fetchvars(self, vars=None, years=None)
        Reads a Hector output file produced by R Hector's fetchvars() function
    """
    
    def __init__(self, abs_path, scenario, version, years=None, vars=None):
        """
        Constructor for the HectorOutput class
        
        Params
        ------
        abs_path : str
            Absolute path of the output file.
        scenario : str
            Hector RCP scenario. Format: 'rcp_XX'
        version : str
            Hector version that produced the output file.
        years : tuple, optional
            If given, the output held in the DataFrame will be limited to the 
            range defined by (year_min, year_max). Default is to include all
            non-spin-up years.
        vars : list of str, optional
            List of Hector output variables to filter. If given, only output 
            from these variables will be held in the DataFrame. Default is 
            to include all variables.
            
        Instance Attributes
        --------------------
        * path : str
            Absolute path of the output file
        * version : str
            Hector version that produced the output
        * scenario : str
            Hector RCP scenario
        * output : Pandas DataFrame
            The Hector output
        * year_first : str
            First output year
        * year_last
            Last output year
        * output_vars : list of str
            Variables for which there is output
            
        Example usage
        --------------
        HectorOutput(<path>, "rcp45", "2.3.0", years=(1900, 2300), vars=['Ca', 'Tgav']
        """
        if (!exists(abs_path)):
            raise FileNotFoundError('Could not locate {}'.format(abs_path))
            
        self.path = abs_path
        self.scenario = scenario
        self.version = version
        self.year_first = None
        self.year_last = None
        self.output_vars = None
        self.output = _parse_output(path, vars=None, years=None)
        
    def _parse_output(self, vars=None, years=None):
        """
        Read the Hector output file into a Pandas DataFrame
        """
        # Hector outputstream csv files have a version string in row 0 that we
        # need to discard
        if (self.version != '2.3.0'):
            return self._parse_outputstream(vars=vars, years=years)
        else:
            return self._parse_fetchvars(vars=vars, years=years)        

    def _parse_outputstream(self, vars=None, years=None):
        """
        Read a Hector output CSV file from a pre-v2.3.0 version of Hector.
        This file is written by Hector's C++ outputstream functions.
        
        Params
        ------
        vars : list of str, optional
            Output variables to filter. If given, variables not included in this
            list will be removed from the DataFrame. Default is to include all
            output variables present in the file.
        years : tuple of int or tuple of str, optional
            Years to filter output by.
            Example: If years == (1900, 2100), only output from years [1900, 2100]
                     will be included in the final DataFrame
        
        Return
        ------
        Pandas DataFrame
        
        Notes
        ------
        This output file differs from the output file written from the R Hector
        'fetchvars' function in a few ways:
          * Includes a 'spinup' column (1 = in spinup, 0 = not in spinup)
          * Includes the output from while Hector is in spinup. 
            The corresponding year is the spinup year & ['spinup'] == 1.
          * Includes a version string in row 0
          * The scenario column (named run_name) format is 'rcpXX', instead of 
            'rcp_XX'
        """
        skipr = 0
        headr = 1
        
        df_out = pd.read_csv(path, sep=',', skiprows=skipr, header=headr)
        
        # Extract only non-spinup output
        df_out = df_out.loc[df_out['spinup'] != 1]
        
        # Drop the 'spinup' & 'component' columns
        df_out = df_out.drop(['spinup', 'component'], axis=1)
        
        # Rename the 'run_name' column as 'scenario' to match R Hector output
        df_out = df_out.rename(columns={'run_name': 'scenario'})
        
        # Re-format the 'scenario' column to match current Hector versions
        # Ex: 'rcp45' --> 'rcp_45'
        df_out['scenario'] = df_out['scenario'].apply(lambda x: x[:3] + '_' + x[3:])
        
        # Subset the desired output variables, if applicable
        if (vars):
            if (not isinstance(vars, list)):  # Cast as list, if needed
                vars = [vars]
            df_out = df_out.loc[df_out['variable'].isin(vars)]
        
        # Extract a tim subset, if applicable
        if (years):
            yr_min = int(years[0])
            yr_max = int(years[1])
            df_out = df_out.loc[(df_out['year'] >= yr_min) & (df_out['year'] <= yr_max)]
        
        return df_out
        
    def _parse_fetchvars(self, vars=None, years=None):
        """
        Read Hector output from a CSV file containing output from the R Hector
        API 'fetchvars' function. Only valid for Hector versions >= v2.2.2
         
        Params
        ------
        vars : list of str, optional
            Output variables to filter. If given, variables not included in this
            list will be removed from the DataFrame. Default is to include all
            output variables present in the file.
        years : tuple of int or tuple of str, optional
            Years to filter output by.
            Example: If years == (1900, 2100), only output from years [1900, 2100]
                     will be included in the final DataFrame
        
        Return
        ------
        Pandas DataFrame
        
        Notes
        ------
        Typical column names: ['scenario', 'year', 'variable', 'value', 'units']
        """
        skipr = None
        headr = 0
        
        df_out = pd.read_csv(path, sep=',', skiprows=skipr, header=headr)
        
        # Subset the desired output variables, if applicable
        if (vars):
            if (not isinstance(vars, list)):  # Cast as list, if needed
                vars = [vars]
            df_out = df_out.loc[df_out['variable'].isin(vars)]
        
        # Extract a tim subset, if applicable
        if (years):
            yr_min = int(years[0])
            yr_max = int(years[1])
            df_out = df_out.loc[(df_out['year'] >= yr_min) & (df_out['year'] <= yr_max)]
        
        return df_out
        
# ------------------------- End HectorOutput Class def -------------------------
        
        
    
### Get the appropriately-formatted path for whatever OS is running the script.
# Hard-coded but who cares nothing matters
if (platform.startswith('linux')):
    #root_wtree  = '/mnt/c/Users/nich980/code/hector-worktrees'
    root_output = '/mnt/c/Users/nich980/data/hector/version-comparison'
elif (platform.startswith('win')):
    #root_wtree  = 'C:\\Users\\nich980\\code\\hector-worktrees'
    root_output = 'C:\\Users\\nich980\\data\\hector\\version-comparison'
else:
    raise OSError("Only Windows and Unix/Linux systems are supported")

### Hector variables that we're interested in
# Hector outputstream vars (Pre-v2.x.x)
vars_old = ['Tgav', 'Ca', 'atmos_c', 'veg_c', 'detritus_c', 'soil_c', 'ocean_c',
            'FCO2', 'Ftot']

# Current Hector (>= v2.3.0) vars
vars_curr = ['Tgav', 'Ca', 'atmos_c', 'veg_c', 'detritus_c', 'soil_c',
             'FCO2', 'Ftot']
### Build a dictionary of the absolute paths of output files for the given Hector versions
v_out = {
    'v2_0_0': {
                'rcp26': join(root_output, 'v2_0_0', 'outputstream_rcp26.csv'),
                'rcp45': join(root_output, 'v2_0_0', 'outputstream_rcp45.csv'),
                'rcp60': join(root_output, 'v2_0_0', 'outputstream_rcp60.csv'),
                'rcp85': join(root_output, 'v2_0_0', 'outputstream_rcp85.csv'),
    },
    'v2_0_1': {
                'rcp26': join(root_output, 'v2_0_1', 'outputstream_rcp26.csv'),
                'rcp45': join(root_output, 'v2_0_1', 'outputstream_rcp45.csv'),
                'rcp60': join(root_output, 'v2_0_1', 'outputstream_rcp60.csv'),
                'rcp85': join(root_output, 'v2_0_1', 'outputstream_rcp85.csv'),
    },
    'v2_1_0': {
                'rcp26': join(root_output, 'v2_1_0', 'outputstream_rcp26.csv'),
                'rcp45': join(root_output, 'v2_1_0', 'outputstream_rcp45.csv'),
                'rcp60': join(root_output, 'v2_1_0', 'outputstream_rcp60.csv'),
                'rcp85': join(root_output, 'v2_1_0', 'outputstream_rcp85.csv'),
    },
    'v2_3_0': {
                'rcp26': join(root_output, 'v2_3_0', 'output_rcp26_v2.3.0.csv'),
                'rcp45': join(root_output, 'v2_3_0', 'output_rcp26_v2.3.0.csv'),
                'rcp60': join(root_output, 'v2_3_0', 'output_rcp26_v2.3.0.csv'),
                'rcp85': join(root_output, 'v2_3_0', 'output_rcp26_v2.3.0.csv'),
    },
}




