"""
Author: Matt Nicholson
17 Jan 2020

Plotting functions to compare the radiative forcings calculated in update_ch4_rf.py
to radiative forcings from a nominal hector run
"""
import pandas as pd
import matplotlib.pyplot as plt

path_nominal_rf = r'C:\Users\nich980\data\hector\output\nominal_run.csv'
path_updated_rf = 'output/updated_rf.csv'

#----------------------- Read the updated hector output -----------------------#

updated_df = pd.read_csv(path_updated_rf, sep=',', header=0)

rf_new_ch4 = updated_df['rf_ch4'].tolist()
rf_new_co2 = updated_df['rf_co2'].tolist()
rf_new_n2o = updated_df['rf_n2o'].tolist()

years = updated_df['year'].unique().tolist()

del updated_df

#----------------------- Read the nominal hector output -----------------------#

nominal_df = pd.read_csv(path_nominal_rf, sep=',', header=0)

# Select only rad forcing values for years calculcated by the script
rf_nom_ch4 = nominal_df.loc[(nominal_df['variable'] == 'FCH4') & (nominal_df['year'].isin(years))].value.tolist()
rf_nom_co2 = nominal_df.loc[(nominal_df['variable'] == 'FCO2') & (nominal_df['year'].isin(years))].value.tolist()
rf_nom_n2o = nominal_df.loc[(nominal_df['variable'] == 'FN2O') & (nominal_df['year'].isin(years))].value.tolist()

del nominal_df

#--------------------- Plot the Radiative Forcing Values ----------------------#

dummy_data = [0] * len(rf_nom_n2o)

fig, axs = plt.subplots(2, 2)

fig.suptitle('Current & Updated Hector Radiative Forcing Equations')

axs[0, 0].plot(years, rf_nom_ch4, 'tab:red', label='Joos et al., 2001 (current)')
axs[0, 0].plot(years, rf_new_ch4, 'tab:green', label='Etminan et al., 2016 (updated)')
axs[0, 0].set_title('CH4')

axs[0, 1].plot(years, rf_nom_co2, 'tab:red', label='Joos et al., 2001 (current)')
axs[0, 1].plot(years, rf_new_co2, 'tab:green', label='Etminan et al., 2016 (updated)')
axs[0, 1].set_title('CO2')

axs[1, 0].plot(years, rf_nom_n2o, 'tab:red', label='Joos et al., 2001 (current)')
axs[1, 0].plot(years, rf_new_n2o, 'tab:green', label='Etminan et al., 2016 (updated)')
axs[1, 0].set_title('N2O')

# dummy data for the bottom right plot
axs[1, 1].plot(years, dummy_data, 'tab:red', label='dummy')    
axs[1, 1].plot(years, dummy_data, 'tab:green', label='dummy, but green')  
axs[1, 1].set_title('Dummy')

for ax in axs.flat:
    ax.set(xlabel='Year', ylabel='W m^-2')
    ax.legend(loc='lower right')

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()

plt.show()