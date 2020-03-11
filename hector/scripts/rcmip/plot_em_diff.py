"""
Plot the difference between RCMIP emissions and default emissions for Hector

Matt Nicholson
10 Mar 2020
"""
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd

from compare_rcmip import subset_years, trim_axs

def plot_em_diff(default_df, rcmip_df, vars, years=(1750, 2100), scenario='RCP45'):
    """
    Plot the difference between RCMIP & default Hector emissions for various
    emissions species
    
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
    rows = 4
    fig, axs = plt.subplots(rows, cols, figsize=figsize, dpi=150, constrained_layout=True)
    fig.suptitle('Hector Output - RCMIP Minus Default Concentrations', fontsize=16)
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
        y_default = np.asarray(default_df.loc[default_df['variable'] == var]['value'])
        y_rcmip   = np.asarray(rcmip_df.loc[rcmip_df['variable'] == var]['value'])
        diff = np.subtract(y_rcmip, y_default)
        ax.plot(x, diff, c='r', ls='-', lw=1, label='Diff')
        ax.set_ylabel('{}'.format(units))
        ax.set_xticks([1750, 1850, 1950, 2050, 2150])
        ax.set_xlim(1750, 2100)
     # End vars loop
    f_name = 'emission-comparison-{}.pdf'.format(scenario)
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

    default_vars = df_default['variable'].unique().tolist()
    rcmip_vars   = df_rcmip['variable'].unique().tolist()

    vars = [x for x in rcmip_vars if x in default_vars]

    plot_em_diff(df_default, df_rcmip, vars)
    