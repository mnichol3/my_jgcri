"""
Create plots that compare input emissions between RCMIP & default Hector

Matt Nicholson
11 Mar 2020
"""
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
from cfunits import Units

from compare_rcmip import subset_years, trim_axs

# === Helper Functions =========================================================
def convert_units(input_vals, input_unit, output_unit):
    """
    Convert the units of an array of values
    
    Params
    -------
    input_vals : Numpy array
        Values to convert
    input_unit : str
        Unit corresponding to the input values
    output_unit : str
        Desired unit to covert the values to
    
    Return
    -------
    Numpy array
    """
    conv_vals = Units.conform(input_vals, Units(input_unit), Units(output_unit))
    return conv_vals
    
    
def subset_rcmip_scenario(rcmip_df, scenario):
    """
    Get a subset of the master RCMIP input emissions dataframe for a specific
    scenario
    
    Params
    -------
    rcmip_df : Pandas DataFrame
        RCMIP master input emissions dataframe
    scenario : str
        Name of the scenario to subset
        
    Return
    -------
    Pandas Dataframe
    """
    scenario_df = rcmip_df.loc[rcmip_df['Scenario'] == scenario].copy()
    return scenario_df
    

def rcmip_2_hector_var(rcmip_2_hector_lut, var_name):
    """
    Get the Hector variable name corresponding to a RCMIP variable name
    
    Params
    -------
    rcmip_2_hector_lut : Pandas DataFrame
        RCMIP to Hector variable look up table
    var_name : str
        Name of the RCMIP variable
        
    Return
    -------
    Pandas Series representing RCMIP --> Hector variable conversion information
        Attributes: hector_component, hector_variable, hector_unit, hector_udunits,
                    rcmip_variable, rcmip_units, rcmip_udunits
    """
    # Get a Pandas series for the lut row. Use iloc[0] to handle case where a hector
    # variable has multiple rows (ffi, luc)
    if (var_name == 'ffi_emissions'):
        rcmip_var = 'Emissions|CO2|MAGICC Fossil and Industrial'
        var_row = rcmip_2_hector_lut.loc[rcmip_2_hector_lut['rcmip_variable'] == rcmip_var].iloc[0]
    elif (var_name == 'luc_emissions'):
        rcmip_var = 'Emissions|CO2|MAGICC AFOLU'
        var_row = rcmip_2_hector_lut.loc[rcmip_2_hector_lut['rcmip_variable'] == rcmip_var].iloc[0]
    else:
        var_row = rcmip_2_hector_lut.loc[rcmip_2_hector_lut['hector_variable'] == var_name].iloc[0]
    return var_row
    
    
def wide_to_long(emissions_df):
    """
    Melt a dataframe from wide format to long format
    
    Params
    -------
    emissions_df : Pandas DataFrame
        Wide-format emissions dataframe to convert to long-format
        
    Return
    -------
    Pandas dataframe in long-format
    """
    id_vars = ["Model", "Scenario", "Region", "Variable", "Unit", "Activity_Id", "Mip_Era"]
    long_df = pd.melt(emissions_df, id_vars=id_vars, var_name="Year", value_name="Value")
    return long_df
    
    
def subset_em_years(emission_df, years, kywrd):
    """
    Subset an emissions dataframe for a given range of years
    
    Params
    -------
    emission_df : Pandas DataFrame
        Hector emissions data
    years : tuple of (int, int)
        Years that define variable timeseries
    kywrd : str
        Either 'hector' or 'rcmip'
        
    Return
    -------
    Pandas DataFrame
    """
    if (kywrd == 'hector'):
        col_name = 'Date'
    elif (kywrd == 'rcmip'):
        col_name = 'Year'
        emission_df[col_name] = pd.to_numeric(emission_df[col_name])
    else:
        raise ValueError('Invalid kywrd param; expected "hector" or "rcmip", got "{}"'.format(kywrd))
    ret_df = emission_df.loc[(emission_df[col_name] >= years[0]) &
                                 (emission_df[col_name] <= years[1])]
    return ret_df
    
# === Plotting funcs =========================================================== 
    
def plot_emissions(default_df, rcmip_df, var_lut, vars, years=(1765, 2100), scenario='RCP45'):
    """
    Plot RCMIP & default Hector input emissions
    
    Parameters
    -----------
    default_df : Pandas DataFrame
        Default Hector emissions data
    rcmip_df : Pandas DataFrame
        RCMIP Hector emissions data
    var_lut : Pandas DataFrame
        RCMIP to Hector variable look up table
    vars : list of str
        Variables to plot
    years : tuple of (int, int)
        Years that define variable timeseries
    scenario : str
        Emissions scenario
    """
    plt.style.use('ggplot')
    figsize = (10, 8)
    cols = 4
    rows = 3
    fig, axs = plt.subplots(rows, cols, figsize=figsize, dpi=150, constrained_layout=True)
    fig.suptitle('Hector Input Emissions - RCMIP vs. Default - {}'.format(scenario), fontsize=16)
    axs = trim_axs(axs, len(vars))
    x = np.asarray([x for x in range(years[0], years[1] + 1)])
    yr_str = [str(yr) for yr in x]
    default_df = subset_em_years(default_df, years, 'hector')
    rcmip_df   = subset_em_years(rcmip_df, years, 'rcmip')
    for ax, var in zip(axs, vars):
        ax.set_title(var)
        print('Plotting {}...'.format(var))
        # --- Get Hector <==> RCMIP variable conversion info ---
        var_conv = rcmip_2_hector_var(var_lut, var)
        # --- Plot default variable value ----------------------
        var_df = default_df[var]
        units  = var_conv.hector_unit
        y = var_df.values
        ax.plot(x, y, c='g', ls='-', lw=1, label='Default')
        ax.set_ylabel('{}'.format(units))
        # --- Convert & plot RCMIP variable value ------------------------
        var_df = rcmip_df.loc[rcmip_df['Variable'] == var_conv.rcmip_variable]
        rcmip_vals = var_df['Value'].to_numpy()
        y = convert_units(rcmip_vals, var_conv.rcmip_udunits, var_conv.hector_udunits)
        ax.plot(x, y, c='r', ls='-', lw=1, label='RCMIP')
        ax.set_xticks([1750, 1850, 1950, 2050, 2150, 2250])
        ax.set_xlim(years[0], years[1])
     # End vars loop
    handles, labels = ax.get_legend_handles_labels()
    leg = fig.legend(handles, labels, loc=4, bbox_to_anchor=(0.98,0.17), prop={'size': 8}, 
                     ncol=2, title='Hector Input Emissions')
    for legobj in leg.legendHandles:
        legobj.set_linewidth(3.0)
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()
# ------------------------------------------------------------------------------

if __name__ == '__main__':
    # !! Note filename is "RCP6", not "RCP60"
    path_default = r"C:\Users\nich980\code\hector\inst\input\emissions\RCP45_emissions.csv"
    path_rcmip   = r"C:\Users\nich980\code\hector-rcmip\data-raw\rcmip-emissions-annual-means-v3-1-0.csv"
    lut_path     = "variable-conversion.csv"
    
    # Default Hector emissions are already in long-format
    df_default = pd.read_csv(path_default, sep=',', skiprows=3, header=0)
    
    df_rcmip = pd.read_csv(path_rcmip, sep=',', header=0)
    df_rcmip = wide_to_long(df_rcmip)
    df_rcmip = subset_rcmip_scenario(df_rcmip, 'rcp45')
    
    rcmip_hector_lut = pd.read_csv(lut_path, sep=',', header=0, skipinitialspace=True)
    
    vars = ['BC_emissions', 'CH4_emissions', 'CO_emissions', 'ffi_emissions',
            'luc_emissions', 'N2O_emissions', 'NMVOC_emissions',
            'NOX_emissions', 'OC_emissions', 'SO2_emissions']

    plot_emissions(df_default, df_rcmip, rcmip_hector_lut, vars)
    