"""
Author: Matt Nicholson
20 Jan 2020

This script aims to validate the simplified radiative forcing expressions
described by Etminan et al. 2016 by comparing the radiative forcing values
from table S1 to RF calculated by the expressions implemented in update_ch4_rf.py

References
-----------
Etminan, M., Myhre, G., Highwood, E. J., and Shine, K. P. ( 2016),
    Radiative forcing of carbon dioxide, methane, and nitrous oxide:
    A significant revision of the methane radiative forcing,
    Geophys. Res. Lett., 43, 12,614– 12,623, doi:10.1002/2016GL071930.
Etminan, M., Myhre, G., Highwood, E. J., and Shine, K. P. ( 2016),
    Supporting Information for: Radiative forcing of carbon dioxide, methane,
    and nitrous oxide: A significant revision of the methane radiative forcing,
    Geophys. Res. Lett., 43, 12,614– 12,623, doi:10.1002/2016GL071930.
    (https://agupubs.onlinelibrary.wiley.com/action/downloadSupplement?doi=10.
     1002%2F2016GL071930&file=grl55302-sup-0001-Supplementary.pdf)
"""
import sys
import pandas as pd
import matplotlib.pyplot as plt

import update_ch4_rf as updated_rf

# File containing the mixing ratios and calculated RF for co2, ch4, & n20 from
# Etminan et al. 2016's supplemental information table S1
rf_data = 'input/etminan_vars.csv'
rf_actual = pd.read_csv(rf_data, sep=',', header=0)

# co2 mixing ratio values as list
mixr_co2 = rf_actual.loc[(rf_actual['species'] == 'co2') &
                         (rf_actual['variable'] == 'mixing_ratio')].iloc[:,3:].values[0].tolist()

# ch4 mixing ratio values as list
mixr_ch4 = rf_actual.loc[(rf_actual['species'] == 'ch4') &
                         (rf_actual['variable'] == 'mixing_ratio')].iloc[:,3:].values[0].tolist()

# n2o mixing ratio values as list           
mixr_n2o = rf_actual.loc[(rf_actual['species'] == 'n2o') &
                         (rf_actual['variable'] == 'mixing_ratio')].iloc[:,3:].values[0].tolist()

c_0 = mixr_co2[0]                         
m_0 = mixr_ch4[0]
n_0 = mixr_n2o[0]

num_steps = len(rf_actual.columns.tolist()[3:])

rf_calc_co2 = [None] * num_steps
rf_calc_ch4 = [None] * num_steps
rf_calc_n2o = [None] * num_steps

#===============================================================================
# Calculate the radiative forcing of the GHG species using the supplemental
# mixing ratios and the new simplified expressions from Etminan et al. 2016
#===============================================================================
prog_count = 1
# Iterate over the timesteps, ignoring the first three columns ('species', 'variable', 'units')
for t_step in range(num_steps):
    
    if (t_step % 9 == 0):
        print('Processing{}'.format('.' * prog_count))
        prog_count += 1
    
    # Mixing ratios (read: concenctrations) for the current time step
    c_curr = mixr_co2[t_step]
    m_curr = mixr_ch4[t_step]
    n_curr = mixr_n2o[t_step]
    
    # Calculate the avaraged concentration for the current time step
    c_bar = updated_rf.calc_cbar(c_0, c_curr)
    m_bar = updated_rf.calc_mbar(m_0, m_curr)
    n_bar = updated_rf.calc_nbar(n_0, n_curr)
    
    # Calculate the radiative forcings for the current time step
    rf_c = updated_rf.calc_rf_co2(c_0, c_curr, n_bar)                  # co2 RF
    rf_m = updated_rf.calc_rf_ch4(m_0, m_curr, m_bar, n_bar)           # ch4 RF
    rf_n = updated_rf.calc_rf_n2o(n_0, n_curr, c_bar, n_bar, m_bar)    # n2o RF
    
    # Add the calculated radiative forcings to their respective arrays
    rf_calc_co2[t_step] = rf_c
    rf_calc_ch4[t_step] = rf_m
    rf_calc_n2o[t_step] = rf_n
    
# End for

# Round the calculated values to the nearest hundredth, since thats the precision
# given in table S1
rf_calc_co2 = [round(x, 2) for x in rf_calc_co2]
rf_calc_ch4 = [round(x, 2) for x in rf_calc_ch4]
rf_calc_n2o = [round(x, 2) for x in rf_calc_n2o]

#===============================================================================
# Get the calculated radiative forcing values from the supplemental text
# table S1 and compare them the to the RF values we just calculated using the 
# same equations
#===============================================================================

# Table S1 co2 RF values
rf_actual_co2 = rf_actual.loc[(rf_actual['species'] == 'co2') &
                              (rf_actual['variable'] == 'rf_new')].iloc[:,3:].values[0].tolist()
                              
# Table S1 ch4 RF values
rf_actual_ch4 = rf_actual.loc[(rf_actual['species'] == 'ch4') &
                              (rf_actual['variable'] == 'rf_new')].iloc[:,3:].values[0].tolist()
                              
# Table S1 n2o RF values
rf_actual_n2o = rf_actual.loc[(rf_actual['species'] == 'n2o') &
                              (rf_actual['variable'] == 'rf_new')].iloc[:,3:].values[0].tolist()

# Compare the given RF values to the ones we calculated
assert_str = 'Table S1 RF values & calculated RF values do not match for {}'

assert rf_actual_co2 == rf_calc_co2, assert_str.format('co2')
assert rf_actual_ch4 == rf_calc_ch4, assert_str.format('ch4')
assert rf_actual_n2o == rf_calc_n2o, assert_str.format('n2o')

print('\n--- All assertion checks passed! ---')
    