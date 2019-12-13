# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 08:19:44 2019

@author: nich980
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

from os.path import join



def get_model_df(abs_path, model='all'):
    """
    Read global AR6 dataset into a Pandas DataFrame
    
    Parameters
    -----------
    abs_path : str
        Absolute path of the data file to read
    model : str, optional
        Model data to return. Ex: if model = 'GCAM', only GCAM model
        data will be returned in the DataFrame. Default is 'all'.
        
    Return
    -------
    model_df : Pandas DataFrame
    """
    em_species = []
    em_subspecies = []
    
    model_df = pd.read_csv(abs_path, sep=',', header=0)
    
    # Remove "Emissions|" substring from every string in the Variable column
    model_df['Variable'] = model_df['Variable'].map(lambda x: x.replace("Emissions|", ""))
    
    if (model != 'all'):
        # Filter out unwanted models
        model_df = model_df[model_df['Model'] == model]
        
        # Reset the index column to accurately represent each row's index
        model_df = model_df.reset_index(drop=True)
    
    # Create lists for two new emission species columns
    for x in model_df['Variable'].tolist():
        species_split = x.split('|')
        em_species.append(species_split[0])
        try:
            em_subspecies.append(species_split[1])
        except IndexError:
            em_subspecies.append(species_split[0])
            
    # Create new DataFrame columns
    model_df['EM_Species'] = pd.Series(em_species).values
    model_df['EM_SubSpecies'] = pd.Series(em_subspecies).values
    
    # Re-order the DataFrame columns
    cols = model_df.columns.tolist()
    cols_new = cols[:-2]
    cols_new.insert(4, 'EM_Species')
    cols_new.insert(5, 'EM_SubSpecies')
    model_df = model_df[cols_new]
    
    model_df = model_df.drop("Variable", axis=1)
    
    return model_df



def get_scenarios(model_df, model=None):
    """
    Get the scenarios
    """
    if (model):
        scenarios = model_df[model_df['Model'] == model]['Scenario'].unique()
    else:
        scenarios = model_df['Scenario'].unique()
    return scenarios
    


def trim_axs(axs, N):
    """little helper to massage the axs list to have correct length..."""
    axs = axs.flat
    for ax in axs[N:]:
        ax.remove()
    return axs[:N]
    


def plot_model_facet(model_df, model):
    """
    Plot a facet of GCAM result graphs, by emission species, for all of the given
    GCAM scenarios in the data set
    
    Parameters
    -----------
    model_df : Pandas DataFrame
        DataFrame containing model data to plot
    model : str
        Model whose data is represented in the model_df DataFrame
        
    Return
    -------
    None
    """
    out_path = r"C:\Users\nich980\data\global_ar6"
    
    plt.style.use('ggplot')
    
    scenarios = get_scenarios(model_df)
    
    figsize = (10, 8)
    cols = 4
    rows = 4
    
#    fig, axs = plt.subplots(rows, cols, figsize=figsize, constrained_layout=True)
    
    for scenario in scenarios:
            
        scenario_df = model_df[model_df['Scenario'] == scenario]
        
        em_species = scenario_df['EM_Species'].unique()
        
        figsize = (10, 8)
        cols = 4
        rows = 4
        
        fig, axs = plt.subplots(rows, cols, figsize=figsize, constrained_layout=True)
        fig.suptitle('{} Scenario {}'.format(model, scenario), fontsize=16)
        
        axs = trim_axs(axs, len(em_species))
        
        for ax, species in zip(axs, em_species):
            ax.set_title('species = {}'.format(species))
            
            data_df = scenario_df[scenario_df['EM_Species'] == species]
            units = data_df['Unit'].tolist()
            
            if (not isinstance(units, str)):
                units = units[0]
            
            units = '{}/yr'.format(units[:2])
            
            x = [int(col) for col in data_df.columns.tolist() if col.isdigit()]
            
            # If sub-species exist, sum their values
            y = data_df.iloc[:,7:].sum().values
            
            ax.plot(x, y, color='blue', marker='o', ls='-', ms=4, label=species)
            ax.set_ylabel('{}'.format(units))
            ax.set_xticks([2025, 2050, 2075, 2100])
            ax.set_xlim(2015, 2100)
            
            ax.legend()
            
        # End species loop
        
        f_name = '{}-{}-facet.png'.format(model, scenario)
        out_path = join(out_path, f_name)
        print(f_name)
        
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        
        plt.show()
        
    # End scenario loop
    
    
    
def plot_all_facet(model_df):
    """
    Plot a facet of all model result graphs, by emission species, for all of the given
    scenarios in the data set
    
    Parameters
    -----------
    model_df : Pandas DataFrame
        DataFrame containing model data to plot
    model : str
        Model whose data is represented in the model_df DataFrame
        
    Return
    -------
    None
    """
    out_path = r"C:\Users\nich980\data\global_ar6"
    
    plt.style.use('ggplot')
    
    scenarios = get_scenarios(model_df, model='GCAM')
    
    models = model_df['Model'].unique()
    
    figsize = (10, 8)
    cols = 4
    rows = 4
    
#    fig, axs = plt.subplots(rows, cols, figsize=figsize, constrained_layout=True)
    
    for scenario in scenarios:
        
        scenario_df = model_df[model_df['Scenario'] == scenario]
        
        em_species = scenario_df['EM_Species'].unique()
        
        figsize = (10, 8)
        cols = 4
        rows = 4
        
        fig, axs = plt.subplots(rows, cols, figsize=figsize, constrained_layout=True)
        fig.suptitle('{} Scenario {}'.format('GCAM', scenario), fontsize=16)
        
        axs = trim_axs(axs, len(em_species))
        
        for ax, species in zip(axs, em_species):
            ax.set_title('species = {}'.format(species))
            
            data_df = scenario_df[scenario_df['EM_Species'] == species]
            units = data_df['Unit'].tolist()
            
            if (not isinstance(units, str)):
                units = units[0]
            
            units = '{}/yr'.format(units[:2])
            
            for model in models:
                
                if (model == 'GCAM'):
                    plt_color = 'blue'
                    z = 2
                else:
                    plt_color = (0.5, 0.5, 0.5)
                    z = 1
                    
                temp_df = data_df[data_df['Model'] == model]
                
                for i in range(len(temp_df.index)):
                    x = [int(col) for col in temp_df.columns.tolist() if col.isdigit()]
                    y = temp_df.iloc[:,7:].sum().values
                    ax.plot(x, y, color=plt_color, marker='o', ls='-', ms=4, zorder=z)
                    
            ax.set_ylabel('{}'.format(units))
            ax.set_xticks([2025, 2050, 2075, 2100])
            ax.set_xlim(2015, 2100)
        
        # End species loop
        f_name = '{}-{}-facet.png'.format('ALL', scenario)
        out_path = join(out_path, f_name)
        print(f_name)
        
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        
        plt.show()
        
    # End scenario loop
     



def plot_gcam_scanarios(model_df, model='GCAM'):
    """
    Plot all GCAM scenarios for each species (except HFC & PFC) on a facet plot
    """       
    out_path = r"C:\Users\nich980\data\global_ar6"
    
    plt.style.use('ggplot')
    
    scenarios = get_scenarios(model_df)
    
    colors = cm.tab20(np.linspace(0, 1, len(scenarios)))
    
    figsize = (10, 8)
    cols = 4
    rows = 4
    
#    fig, axs = plt.subplots(rows, cols, figsize=figsize, constrained_layout=True)
        
    em_species = model_df['EM_Species'].unique().tolist()
    em_species.remove('HFC')
    em_species.remove('PFC')
    
    
    figsize = (10, 8)
    cols = 4
    rows = 4
    
    fig, axs = plt.subplots(rows, cols, figsize=figsize, constrained_layout=True)
    fig.suptitle('{} Emission Species & Scenarios'.format(model), fontsize=16)
    
    axs = trim_axs(axs, len(em_species))
    
    for ax, species in zip(axs, em_species):
        
        data_df = model_df[model_df['EM_Species'] == species]
            
        units = data_df['Unit'].tolist()
        if (not isinstance(units, str)):
                units = units[0]
            
        units = '{}/yr'.format(units[:2])
        
        ax.set_title('species = {}'.format(species))
        
        for scenario_idx, scenario in enumerate(scenarios):
            scenario_df = data_df[data_df['Scenario'] == scenario]

            x = [int(col) for col in scenario_df.columns.tolist() if col.isdigit()]
            
            # If sub-species exist, sum their values
            y = scenario_df.iloc[:,7:].sum().values
            
            ax.plot(x, y, c=colors[scenario_idx], ls='-', lw=1, label=scenario)
            
        ax.set_ylabel('{}'.format(units))
        ax.set_xticks([2025, 2050, 2075, 2100])
        ax.set_xlim(2015, 2100)
        
    # End species loop
    
    handles, labels = ax.get_legend_handles_labels()
#    fig.legend(handles, labels, loc='lower right', ncol=2)
    leg = fig.legend(handles, labels, loc=4, bbox_to_anchor=(0.97,0.23), ncol=2, title='GCAM Scenarios')
    
    for legobj in leg.legendHandles:
        legobj.set_linewidth(3.0)
    
    f_name = '{}-{}-facet.png'.format(model, scenario)
    out_path = join(out_path, f_name)
    print(f_name)
    
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    
    plt.show()
    
    
    
def plot_fluorocarbons(model_df, model='GCAM'):
    out_path = r"C:\Users\nich980\data\global_ar6"
    
    plt.style.use('ggplot')
    
    scenarios = get_scenarios(model_df)
    
    colors = cm.tab20(np.linspace(0, 1, len(scenarios)))
    
    figsize = (10, 8)
    cols = 4
    rows = 4
    
#    fig, axs = plt.subplots(rows, cols, figsize=figsize, constrained_layout=True)
        
    hfc = model_df[model_df['EM_Species'] == 'HFC']
    pfc = model_df[model_df['EM_Species'] == 'PFC']
    
    species_dict = {'HFC': hfc,
                    'PFC': pfc}
    
    figsize = (10, 8)
    cols = 3
    rows = 3
    
    for species in ['HFC']:
        fig, axs = plt.subplots(rows, cols, figsize=figsize, constrained_layout=True)
        fig.suptitle('{} Scenarios for {} Sub-species'.format(model, species), fontsize=16)
        
        # HFC or PFC DataFrame
        species_df = species_dict[species]
        
        sub_species = species_df['EM_SubSpecies'].unique().tolist()
        
        units = species_df['Unit'].tolist()[0]
        
#        if (not isinstance(units, str)):
#            units = units[0]
                
        units = '{}/yr'.format(units[:2])
        
        axs = trim_axs(axs, len(sub_species))
        
        for ax, sub_s in zip(axs, sub_species):
            
            # Sub-species DataFrame
            subs_df = species_df[species_df['EM_SubSpecies'] == sub_s]
#                
#            units = data_df['Unit'].tolist()
#            if (not isinstance(units, str)):
#                    units = units[0]
#                
#            units = '{}/yr'.format(units[:2])
            
            ax.set_title('{}'.format(sub_s))
            
            for scenario_idx, scenario in enumerate(scenarios):
                scenario_df = subs_df[subs_df['Scenario'] == scenario]
    
                x = [int(col) for col in scenario_df.columns.tolist() if col.isdigit()]
                
                # If sub-species exist, sum their values
                y = scenario_df.iloc[:,7:].sum().values
                
                ax.plot(x, y, c=colors[scenario_idx], ls='-', lw=1.5, label=scenario)
                
            ax.set_ylabel('{}'.format(units))
            ax.set_xticks([2025, 2050, 2075, 2100])
            ax.set_xlim(2015, 2100)
            
        # End species loop
        
        handles, labels = ax.get_legend_handles_labels()
    #    fig.legend(handles, labels, loc='lower right', ncol=2)
        leg = fig.legend(handles, labels, loc=4, bbox_to_anchor=(0.9,0.07), ncol=2, title='GCAM Scenarios')
        
        for legobj in leg.legendHandles:
            legobj.set_linewidth(3.0)
        
        f_name = '{}-{}-facet.png'.format(model, scenario)
        out_path = join(out_path, f_name)
        print(f_name)
        
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        
        plt.show()
        break
    


def melt_df(model_df):
    melted_df = model_df.melt(id_vars=['Model', 'Scenario', 'Region', 'EM_Species',
                                       'EM_SubSpecies', 'Unit', 'Ms'], 
                              var_name="Year", 
                              value_name="EM_Value")
    return melted_df
    


def pp_df(df):
    df = df[:20]
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df)

   
    
def main():
    f_path = r"C:\Users\nich980\data\global_ar6"
    f_name = "global_ar6_harmonized_emissions.csv"
    
    f_abs = join(f_path, f_name)
    
    # Get the GCAM data in a DataFrame
    em_df = get_model_df(f_abs, model="GCAM")
    plot_fluorocarbons(em_df)
    
#    print(em_df.columns.tolist())
#    plot_model_facet(em_df, 'GCAM')
#    plot_gcam_scanarios(em_df)
    
#    em_df = get_model_df(f_abs)
#    plot_all_facet(em_df)
    
    
   
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    