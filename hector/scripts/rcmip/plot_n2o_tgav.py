"""
Plot the global temperatures for two Hector runs: one using default RCP60
emissions, the other using converted RCMIP RCP60 emissions.

Matt Nicholson
25 Mar 2020
"""
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
from cfunits import Units

# --- Top Axis: Global temp ----------------------------------------------------
default_df = r"C:\Users\nich980\data\hector\output\hector-cold\default_rcp60.csv"
rcmip_df   = r"C:\Users\nich980\data\hector\output\hector-cold\rcmip_rcp60.csv"
rcmip_2_df = r"C:\Users\nich980\data\hector\output\hector-cold\rcmip_rcp60_2x.csv"

default_df = pd.read_csv(default_df, sep=',', header=0)
rcmip_df   = pd.read_csv(rcmip_df, sep=',', header=0)
rcmip_2_df = pd.read_csv(rcmip_2_df, sep=',', header=0)

default_temp = default_df.loc[default_df['variable'] == 'Tgav']
rcmip_temp   = rcmip_df.loc[rcmip_df['variable'] == 'Tgav']
rcmip_temp_2x = rcmip_2_df.loc[rcmip_2_df['variable'] == 'Tgav']

years = default_temp['year'].unique().tolist()

plt.style.use('ggplot')
figsize = (10, 8)
fig, axs = plt.subplots(2, 1)
axs[0].set_title('Hector Global Average Temperature - RCP60')

temp = default_temp['value'].to_numpy()
unit = default_temp['units'].tolist()[0]
axs[0].plot(years, temp, c='r', ls='--', lw=1, label='Default N2O Emissions (Mt N2O-N/yr)')

temp = rcmip_temp['value'].to_numpy()
unit = rcmip_temp['units'].tolist()[0]
axs[0].plot(years, temp, c='g', ls=':', lw=1, label='RCMIP N2O Emissions (Tg N/yr)')

temp = rcmip_temp_2x['value'].to_numpy()
unit = rcmip_temp_2x['units'].tolist()[0]
# axs[0].plot(years, temp, c='b', ls='-.', lw=1, label='RCMIP N2O Emissions x2 (Tg N/yr)')
axs[0].plot(years, temp, c='b', ls='-.', lw=1, label='Corrected RCMIP N2O Emissions (Tg N/yr)')

axs[0].set_ylabel(unit)
axs[0].set_xlabel('Year')
axs[0].set_xlim(1750, 2300)
axs[0].set_xticks([1750, 1850, 1950, 2050, 2150, 2250])
axs[0].legend(loc='right')

# --- Bottom Axis: N2O emissions -----------------------------------------------
default_df = r"C:\Users\nich980\data\hector\version-comparison\emissions\RCP60_emissions_default.csv"
rcmip_df   = r"C:\Users\nich980\data\hector\version-comparison\emissions\RCP60_emissions_rcmip.csv"
rcmip_df_2 = r"C:\Users\nich980\data\hector\version-comparison\emissions\RCP60_emissions_corrected.csv"

years = [x for x in range(1765, 2101)]

default_df = pd.read_csv(default_df, sep=',', header=0, skiprows=3)
default_df = default_df.loc[(default_df['Date'] >= 1765) & (default_df['Date'] <= 2100)]
default_em = default_df['N2O_emissions'].to_numpy()

rcmip_df = pd.read_csv(rcmip_df, sep=',', header=0, skiprows=3)
rcmip_df = rcmip_df.loc[(rcmip_df['Date'] >= 1765) & (rcmip_df['Date'] <= 2100)]
rcmip_em = rcmip_df['N2O_emissions'].to_numpy()
# rcmip_em_2 = np.multiply(rcmip_em, 2)

rcmip_df_2 = pd.read_csv(rcmip_df_2, sep=',', header=0, skiprows=3)
rcmip_df_2 = rcmip_df_2.loc[(rcmip_df_2['Date'] >= 1765) & (rcmip_df_2['Date'] <= 2100)]
rcmip_em_2 = rcmip_df_2['N2O_emissions'].to_numpy()

default_unit = 'Mt N'
rcmip_unit = 'Tg N'

# Convert the rcmip units to Mt
rcmip_em = Units.conform(rcmip_em, Units('Tg'), Units('Mt'))

axs[1].plot(years, default_em, c='r', ls='--', lw=1, label='Default N2O Emissions')
axs[1].plot(years, rcmip_em, c='g', ls=':', lw=1, label='RCMIP N2O Emissions')
axs[1].plot(years, rcmip_em_2, c='b', ls='-.', lw=1, label='Corrected RCMIP N2O Emissions')

axs[1].set_title('Input N2O Emissions - RCP60')
axs[1].set_ylabel('Mt N')
axs[1].set_xlabel('Year')
axs[1].set_xlim(1750, 2300)
axs[1].set_xticks([1750, 1850, 1950, 2050, 2150, 2250])
axs[1].legend(loc='right')

# --- Bottom Axis: N2O forcing -------------------------------------------------
# var = 'FN2O'
# default_f = default_df.loc[default_df['variable'] == var]
# rcmip_f   = rcmip_df.loc[rcmip_df['variable'] == var]
# rcmip_f_2x = rcmip_2_df.loc[rcmip_2_df['variable'] == var]

# forcing = default_f['value'].to_numpy()
# axs[1].plot(years, forcing, c='r', ls='--', lw=1, label='Default')

# forcing = rcmip_f['value'].to_numpy()
# axs[1].plot(years, forcing, c='g', ls=':', lw=1, label='RCMIP')

# forcing = rcmip_f_2x['value'].to_numpy()
# axs[1].plot(years, forcing, c='b', ls='-.', lw=1, label='RCMIP x2')

# axs[1].set_title('N2O Radiative Forcing - RCP60')
# axs[1].set_ylabel('W m-2')
# axs[1].set_xlabel('Year')
# axs[1].set_xlim(1750, 2300)
# axs[1].set_xticks([1750, 1850, 1950, 2050, 2150, 2250])
# axs[1].legend(loc='right')
# ------------------------------------------------------------------------------
plt.show()