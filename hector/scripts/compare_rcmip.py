"""
Compare Hector RCP45 output using RCMIP emissions with Hector v2.3.0 RCP45 output using
default emissions

Matt Nicholson
26 Feb 2020
"""
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd

def subset_years(df, years):
    ret_df = df.loc[(df['year'] >= years[0]) & (df['year'] <= years[1])]
    return ret_df

def trim_axs(axs, N):
    """little helper to massage the axs list to have correct length..."""
    axs = axs.flat
    for ax in axs[N:]:
        ax.remove()
    return axs[:N]

def plot_variables(default_df, rcmip_df, vars, years=(1750, 2100), scenario='RCP45'):
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
    figsize = (10, 8)
    cols = 4
    rows = 4
    fig, axs = plt.subplots(rows, cols, figsize=figsize, dpi=150, constrained_layout=True)
    fig.suptitle('Hector Output - RCMIP Emissions vs. Default Emissions', fontsize=16)
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
        ax.set_xlim(1750, 2300)
     # End vars loop
    handles, labels = ax.get_legend_handles_labels()
    leg = fig.legend(handles, labels, loc=4, bbox_to_anchor=(0.98,0.17), prop={'size': 8}, 
                     ncol=2, title='Hector Input Emissions')
    for legobj in leg.legendHandles:
        legobj.set_linewidth(3.0)
    f_name = 'emission-comparison-{}.pdf'.format(scenario)
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()

# ------------------------------------------------------------------------------
outpath_default = r"C:\Users\nich980\data\hector\version-comparison\v2_3_0\output_rcp45_v2.3.0.csv"
outpath_rcmip   = r"C:\Users\nich980\data\hector\version-comparison\rcp45-default-rcmip.csv"

# Read both output files and extract a list of variables in each
df_default = pd.read_csv(outpath_default, sep=',', header=0)
df_rcmip   = pd.read_csv(outpath_rcmip, sep=',', header=0)

default_vars = df_default['variable'].unique().tolist()
rcmip_vars   = df_rcmip['variable'].unique().tolist()

vars = [x for x in rcmip_vars if x in default_vars]

plot_variables(df_default, df_rcmip, vars)