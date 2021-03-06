"""
Matt Nicholson
7 Feb 2020

This script contains functions to compare output from various versions of 
PNNL-JGCRI's Hector Simple Climate Model
"""
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

from os.path import join, exists
from os import walk
from sys import platform

# ========================= Define HectorOutput Class ==========================

class HectorOutput:
    """
    A simple class to represent a Hector output file
    """
    
    def __init__(self, abs_path, years=None, vars=None):
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
        if (not exists(abs_path)):
            raise FileNotFoundError('Could not locate {}'.format(abs_path)) 
        self.path        = abs_path
        self.scenario    = self._parse_scenario(abs_path)
        self.version     = self._parse_version(abs_path)
        self.year_first  = None
        self.year_last   = None
        self.output_vars = vars
        self.output = self._parse_output(abs_path, vars=vars, years=years)
        self._parse_years(years)
        
    def _parse_scenario(self, path):
        pattern = re.compile(r'_(rcp\d{2})')
        match = re.search(pattern, path)
        scenario = match.groups()[0]
        return scenario
        
    def _parse_version(self, path):
        splits  = path.split('\\')
        if (len(splits) == 1):
            splits = path.split('/')  # Linux case
        version  = splits[-2].replace('v', '').replace('_', '.')
        return version
    
    def _parse_years(self, years):
        if (years):
            self.year_first, self.year_last = years
        else:
            self.year_first = None
            self.year_last  = None
        
    def _parse_output(self, path, vars=None, years=None):
        """
        Read the Hector output file into a Pandas DataFrame
        """
        # Hector outputstream csv files have a version string in row 0 that we
        # need to discard
        if (self.version != '2.3.0'):
            return self._parse_outputstream(path, vars=vars, years=years)
        else:
            return self._parse_fetchvars(path, vars=vars, years=years)        

    def _parse_outputstream(self, path, vars=None, years=None):
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
        
    def _parse_fetchvars(self, path, vars=None, years=None):
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
        
# =============================== Plotting Funcs ===============================
def trim_axs(axs, N):
    """little helper to massage the axs list to have correct length..."""
    axs = axs.flat
    for ax in axs[N:]:
        ax.remove()
    return axs[:N]

def plot_variables(hector_output, vars, years=(1750, 2300), scenario='RCP45'):
    """
    Plot output from HectorOutput objects
    
    Parameters
    -----------
    hector_output: dict
        Dictionary of {str: HectorOutput obj}
    vars : list of str
        Output variables to plot
    """
    versions = ['2.0.0', '2.0.1', '2.1.0', '2.3.0']
    plt.style.use('ggplot')
    colors = cm.tab20(np.linspace(0, 1, len(vars)))
    figsize = (10, 8)
    cols = 4
    rows = 4
    fig, axs = plt.subplots(rows, cols, figsize=figsize, dpi=150, constrained_layout=True)
    fig.suptitle('Hector Output by Version - {}'.format(scenario), fontsize=16)
    axs = trim_axs(axs, len(vars))
    x = np.asarray([x for x in range(years[0], years[1] + 1)])
    for ax, var in zip(axs, vars):
        ax.set_title(var)
        for version_idx, version in enumerate(versions):
            print(var, version)
            version_df = hector_output[version].output
            var_df = version_df.loc[version_df['variable'] == var]
            units  = var_df['units'].unique().tolist()[0]
            y = np.asarray(var_df['value'])
            ax.plot(x, y, c=colors[version_idx], ls='-', lw=1, label=version)
        ax.set_ylabel('{}'.format(units))
        ax.set_xticks([1750, 1850, 1950, 2050, 2150, 2250])
        ax.set_xlim(1750, 2300)
     # End vars loop
    handles, labels = ax.get_legend_handles_labels()
    leg = fig.legend(handles, labels, loc=4, bbox_to_anchor=(0.98,0.17), prop={'size': 8}, 
                     ncol=2, title='Hector Version')
    for legobj in leg.legendHandles:
        legobj.set_linewidth(3.0)
    f_name = 'version-comparison-{}.pdf'.format(scenario)
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()

def generate_obj(out_file):
    def _parse_key(f_path):
        pattern = re.compile(r'_(rcp\d{2})')
        match = re.search(pattern, f_path)
        scenario = match.groups()[0]
        splits  = f_path.split('\\')
        if (len(splits) == 1):
            splits = f_path.split('/')  # Linux case
        version  = splits[-2].replace('v', '').replace('_', '.')
        # k = '{}-{}'.format(version, scenario)
        k = version
        return k
    key = _parse_key(out_file)
    obj = HectorOutput(out_file, years=(1750, 2300), vars=vars)
    return (key, obj)

root_output = 'C:\\Users\\nich980\\data\\hector\\version-comparison'

### Hector variables that we're interested in
# Hector outputstream vars (Pre-v2.x.x)
# 'ocean_c' is unavail for the current Hector
# vars_old = ['Tgav', 'Ca', 'atmos_c', 'veg_c', 'detritus_c', 'soil_c', 'ocean_c',
            # 'FCO2', 'Ftot']

# Current Hector (>= v2.3.0) vars
# vars_curr = ['Tgav', 'Ca', 'atmos_c', 'veg_c', 'detritus_c', 'soil_c', 'FCO2', 'Ftot']
vars = ['Tgav', 'Ca', 'atmos_c', 'veg_c', 'detritus_c', 'soil_c', 'FCO2', 'Ftot'] 
 
output_dict = {
    'v2_0_0': 'outputstream_rcp45.csv',
    'v2_0_1': 'outputstream_rcp45.csv',
    'v2_1_0': 'outputstream_rcp45.csv',
    'v2_3_0': 'output_rcp45_v2.3.0.csv',
    }
# Construct absolute paths of all output files
out_files = [join(root_output, key, val) for (key, val) in output_dict.items()]

# Create a dictionary where the key is 'version-scenario' and the value is the
# corresponding HectorOutput object
# Ex: '2.0.0-rcp26':  <__main__.HectorOutput object at...
output = {key: val for (key, val) in [generate_obj(f) for f in out_files]}

plot_variables(output, vars, years=(1750, 2300), scenario='RCP45')




