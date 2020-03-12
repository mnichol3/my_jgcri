"""
Plot a couple RCMIP scenario input emissions for fun and for profit

Matt Nicholson
11 Mar 2020
"""
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd


# === Helper funcs =============================================================
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
    scenario_df = rcmip_df.loc[(rcmip_df['Scenario'] == scenario) &
                               (rcmip_df['Region'] == 'World')].copy()
    return scenario_df
    
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
                                 (emission_df[col_name] <= years[1])].copy()
    return ret_df
    
    
# === Plotting func ============================================================

def plot_rcmip_ems(rcmip_ems, years=(1765, 2100)):
    """
    Plot RCMIP input emissions for some SSPs & RCPs. Currently only plotting
    N2O emissions
    
    Scenarios:
        RCP45, RCP60, SSP119, SSP370
    
    Params
    -------
    rcmip_ems : Pandas DataFrame
        RCMIP emissions data
    years : tuple of (int, int)
        Years that define variable timeseries
    """
    rcmip_ems = wide_to_long(rcmip_ems)
    scenarios = ['rcp60', 'rcp45', 'ssp119', 'ssp370']
    plt.style.use('ggplot')
    figsize = (10, 8)
    fig, ax = plt.subplots()
    plt.title('RCMIP N2O Emissions', fontsize=16)
    x = np.asarray([x for x in range(years[0], years[1] + 1)])
    # --- Subset the rcmip emissions df for scenario & years ---
    em_rcp45  = subset_rcmip_scenario(rcmip_ems, 'rcp45')
    em_rcp45  = subset_em_years(em_rcp45, years, 'rcmip')
    em_rcp60  = subset_rcmip_scenario(rcmip_ems, 'rcp60')
    em_rcp60  = subset_em_years(em_rcp60, years, 'rcmip')
    em_ssp119 = subset_rcmip_scenario(rcmip_ems, 'ssp119')
    em_ssp119 = subset_em_years(em_ssp119, years, 'rcmip')
    em_ssp370 = subset_rcmip_scenario(rcmip_ems, 'ssp370')
    em_ssp370 = subset_em_years(em_ssp370, years, 'rcmip')
    # --- Plot rcp45 -------------------------------------------
    var_df = em_rcp45.loc[em_rcp45['Variable'] == 'Emissions|N2O']
    em_vals = var_df['Value'].to_numpy()
    ax.plot(x, em_vals, c='r', ls='-', lw=1, label='RCP45')
    # --- Plot rcp60 -------------------------------------------
    var_df = em_rcp60.loc[em_rcp60['Variable'] == 'Emissions|N2O']
    em_vals = var_df['Value'].to_numpy()
    ax.plot(x, em_vals, c='g', ls='--', lw=1, label='RCP60')
    # --- Plot ssp119 ------------------------------------------
    var_df = em_ssp119.loc[em_ssp119['Variable'] == 'Emissions|N2O']
    em_vals = var_df['Value'].to_numpy()
    ax.plot(x, em_vals, c='b', ls='-', lw=1, label='SSP119')
    # --- Plot ssp370 ------------------------------------------
    var_df = em_ssp370.loc[em_ssp370['Variable'] == 'Emissions|N2O']
    em_vals = var_df['Value'].to_numpy()
    ax.plot(x, em_vals, c='m', ls='--', lw=1, label='SSP370')
    unit = var_df['Unit'].iloc[0]
    ax.set_ylabel('N2O Emissions ({})'.format(unit))
    ax.set_xlabel('Year')
    # --- Axis ticks & labels ----------------------------------
    # ax.set_xticks([1750, 1850, 1950, 2050, 2150, 2250])
    ax.set_xticks([1800, 1825, 1850, 1875, 1900, 1925, 1950])
    ax.set_xlim(years[0], years[1])
    handles, labels = ax.get_legend_handles_labels()
    leg = fig.legend(handles, labels, loc=4, bbox_to_anchor=(0.9,0.17), prop={'size': 8}, 
                     ncol=2, title='RCMIP Input Emissions')
    for legobj in leg.legendHandles:
        legobj.set_linewidth(3.0)
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()
    
# ------------------------------------------------------------------------------
    
if __name__ == '__main__':
    path_rcmip   = r"C:\Users\nich980\code\hector-rcmip\data-raw\rcmip-emissions-annual-means-v3-1-0.csv"
    df_rcmip = pd.read_csv(path_rcmip, sep=',', header=0)
    
    years = (1850, 1950)
    plot_rcmip_ems(df_rcmip, years=years)
    