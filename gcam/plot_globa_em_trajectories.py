# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 08:19:44 2019

@author: nich980
"""

import pandas as pd
import matplotlib.pyplot as plt
from time import sleep

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



def get_scenarios(model_df):
    """
    Get the scenarios
    """
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
            
            for i in range(len(data_df.index)):
                x = [int(col) for col in data_df.columns.tolist() if col.isdigit()]
                y = data_df.iloc[i,7:]
                ax.plot(x, y, 'o', ls='-', ms=4, label=data_df['EM_SubSpecies'].iloc[i])
            ax.set_ylabel('{}'.format(units))
            ax.set_xticks([2025, 2050, 2075, 2100])
            ax.set_xlim(2015, 2100)
            
            if (species == 'HFC'):
                ax.legend(loc=1, ncol=2)
            else:
                ax.legend()
        # End species loop
        f_name = '{}-{}-facet.png'.format(model, scenario)
        out_path = join(out_path, f_name)
        print(f_name)
        
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        
        plt.show()
        
    # End scenario loop
            
    
    
    
    


def melt_df(model_df):
    melted_df = model_df.melt(id_vars=['Model', 'Scenario', 'Region', 'EM_Species',
                                       'EM_SubSpecies', 'Unit', 'Ms'], 
                              var_name="Year", 
                              value_name="EM_Value")
    return melted_df
    


def pp_df(df):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df)

   
    
def main():
    f_path = r"C:\Users\nich980\data\global_ar6"
    f_name = "global_ar6_harmonized_emissions.csv"
    
    f_abs = join(f_path, f_name)
    
    # Get the GCAM data in a DataFrame
    em_df = get_model_df(f_abs, model='GCAM')
    
#    em_df = em_df[em_df['Scenario'] == 'SSP1-19']
#    em_df = em_df[em_df['EM_Species'] == 'CO2']
#    em_df = melt_df(em_df)
   
#    pp_df(em_df[:10])
#    print(em_df.iloc[0])
    
    plot_model_facet(em_df, 'GCAM')
    
    
   
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    