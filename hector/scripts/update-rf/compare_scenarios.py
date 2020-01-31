"""
Author: Matt Nicholson
23 Jan 2020

This script compares radiative forcings calculated using Hector RCMIP SSP emissions
to default Hector RFs
"""
import pandas as pd
import matplotlib.pyplot as plt

import update_ch4_rf as updated_rf


# ============================= Config variables ===============================
input_emissions = r'C:\Users\nich980\data\hector\output\nominal_run.csv'
rcmip_rfs = r'input/ERF_ssp245_1750-2500.csv'

year_start = 1750
year_end = 2300

# ============================== Calculate RFs =================================
# Read the emissions into a DataFrame
emission_df = pd.read_csv(input_emissions, sep=',', header=0)

# Call the RF calculation func
rf_new = updated_rf.calc_all_rf(emission_df, year_start, year_end)


# =============================== Compare RFs ==================================
# Read the RFs that we're going to compare the calculated RFs to
rf_rcmip = pd.read_csv(rcmip_rfs, sep=',', header=0)

# Plot the RFs
dummy_data = [0] * (year_end - year_start + 1)

years = [yr for yr in range(year_start, year_end + 1)]

fig, axs = plt.subplots(2, 2)

fig.suptitle('Current & Updated Hector Radiative Forcing Equations')

# ----- Plot CH4 -----
var_rcmip = rf_rcmip['ch4'].loc[(rf_rcmip['year'] >= year_start) & (rf_rcmip['year'] <= year_end)].tolist()
var_new = rf_new['rf_ch4'].loc[(rf_new['year'] >= year_start) & (rf_new['year'] <= year_end)].tolist()

axs[0, 0].plot(years, var_rcmip, 'tab:red', label='Hector RCMIP')
axs[0, 0].plot(years, var_new, 'tab:green', label='Etminan et al., 2016 (updated)')
axs[0, 0].set_title('CH4')

# ----- Plot CO2 -----
var_rcmip = rf_rcmip['co2'].loc[(rf_rcmip['year'] >= year_start) & (rf_rcmip['year'] <= year_end)].tolist()
var_new = rf_new['rf_co2'].loc[(rf_new['year'] >= year_start) & (rf_new['year'] <= year_end)].tolist()

axs[0, 1].plot(years, var_rcmip, 'tab:red', label='Hector RCMIP')
axs[0, 1].plot(years, var_new, 'tab:green', label='Etminan et al., 2016 (updated)')
axs[0, 1].set_title('CO2')

# ----- Plot N2O -----
var_rcmip = rf_rcmip['n2o'].loc[(rf_rcmip['year'] >= year_start) & (rf_rcmip['year'] <= year_end)].tolist()
var_new = rf_new['rf_n2o'].loc[(rf_new['year'] >= year_start) & (rf_new['year'] <= year_end)].tolist()

axs[1, 0].plot(years, var_rcmip, 'tab:red', label='Hector RCMIP')
axs[1, 0].plot(years, var_new, 'tab:green', label='Etminan et al., 2016 (updated)')
axs[1, 0].set_title('N2O')

# ----- dummy data for the bottom right plot -----
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