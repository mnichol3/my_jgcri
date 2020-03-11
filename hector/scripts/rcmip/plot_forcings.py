"""
Create plots that compare various forcing variables for RCMIP & Default hector
RCP 45 emissions

Matt Nicholson
11 Mar 2020
"""
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd

from compare_rcmip import subset_years, trim_axs

def plot_forcings(default_df, rcmip_df, vars, years=(1750, 2100), scenario='RCP45'):
    """
    Plot RCMIP & default Hector forcings
    
    Parameters
    -----------
    default_df : Pandas DataFrame
        Default Hector emissions data
    rcmip_df : Pandas DataFrame
        RCMIP Hector emissions data
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
    rows = 2
    fig, axs = plt.subplots(rows, cols, figsize=figsize, dpi=150, constrained_layout=True)
    fig.suptitle('Hector Output - RCMIP vs. Default Forcings', fontsize=16)
    axs = trim_axs(axs, len(vars))
    x = np.asarray([x for x in range(years[0], years[1] + 1)])
    default_df = subset_years(default_df, years)
    rcmip_df   = subset_years(rcmip_df, years)
    for ax, var in zip(axs, vars):
        ax.set_title(var)
        print('Plotting {}...'.format(var))
        # Plot default variable value
        var_df = default_df.loc[default_df['variable'] == var]
        units  = var_df['units'].unique().tolist()[0]
        y = np.asarray(var_df['value'])
        ax.plot(x, y, c='g', ls='-', lw=1, label='Default')
        ax.set_ylabel('{}'.format(units))
        # Plot RCMIP variable value
        var_df = rcmip_df.loc[rcmip_df['variable'] == var]
        units  = var_df['units'].unique().tolist()[0]
        y = np.asarray(var_df['value'])
        ax.plot(x, y, c='r', ls='-', lw=1, label='RCMIP')
        ax.set_xticks([1750, 1850, 1950, 2050, 2150, 2250])
        ax.set_xlim(1750, 2100)
     # End vars loop
    handles, labels = ax.get_legend_handles_labels()
    leg = fig.legend(handles, labels, loc=4, bbox_to_anchor=(0.98,0.17), prop={'size': 8}, 
                     ncol=2, title='Hector Forcings')
    for legobj in leg.legendHandles:
        legobj.set_linewidth(3.0)
    # f_name = 'emission-comparison-{}.pdf'.format(scenario)
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()
# ------------------------------------------------------------------------------

if __name__ == '__main__':  
    outpath_default = r"C:\Users\nich980\data\hector\version-comparison\v2_3_0\output_rcp45_v2.3.0.csv"
    outpath_rcmip   = r"C:\Users\nich980\data\hector\version-comparison\rcp45-default-rcmip.csv"

    # Read both output files and extract a list of variables in each
    df_default = pd.read_csv(outpath_default, sep=',', header=0)
    df_rcmip   = pd.read_csv(outpath_rcmip, sep=',', header=0)

    vars = ['Ftot', 'FCO2', 'FN2O', 'FBC', 'FOC', 'FSO2', 'FCH4']

    plot_forcings(df_default, df_rcmip, vars)
    