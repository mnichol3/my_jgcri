import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
from cfunits import Units

default_df = r"C:\Users\nich980\data\hector\version-comparison\emissions\RCP60_emissions_default.csv"
rcmip_df   = r"C:\Users\nich980\data\hector\version-comparison\emissions\RCP60_emissions_rcmip.csv"

years = [x for x in range(1765, 2101)]

default_df = pd.read_csv(default_df, sep=',', header=0, skiprows=3)
default_df = default_df.loc[(default_df['Date'] >= 1765) & (default_df['Date'] <= 2100)]
default_em = default_df['N2O_emissions'].to_numpy()

rcmip_df = pd.read_csv(rcmip_df, sep=',', header=0, skiprows=3)
rcmip_df = rcmip_df.loc[(rcmip_df['Date'] >= 1765) & (rcmip_df['Date'] <= 2100)]
rcmip_em = rcmip_df['N2O_emissions'].to_numpy()

default_unit = 'Mt N'
rcmip_unit = 'Tg N'

# --- Top Axis: Tg --> Mt ------------------------------------------------------
plt.style.use('ggplot')
figsize = (10, 8)
fig, axs = plt.subplots(2, 1)
axs[0].set_title('N2O Emissions - RCP60')

rcmip_em2 = Units.conform(rcmip_em, Units('Tg'), Units('Mt'))

axs[0].plot(years, default_em, c='r', ls='-', lw=1, label='Default N2O Emissions (Mt N2O-N/yr)')
axs[0].plot(years, rcmip_em2, c='g', ls='-', lw=1, label='RCMIP N2O Emissions (Tg N/yr)')

axs[0].set_ylabel('Mt')
axs[0].set_xlabel('Year')
axs[0].set_xlim(1765, 2100)
axs[0].set_xticks([1750, 1850, 1950, 2050, 2150, 2250])
axs[0].legend(loc='right')

# --- Bottom Axis: Mt --> Tg ---------------------------------------------------

# Convert the rcmip units to Mt
default_em2 = Units.conform(default_em, Units('Mt'), Units('Tg'))

axs[1].plot(years, default_em2, c='r', ls='-', lw=1, label='Default N2O Emissions')
axs[1].plot(years, rcmip_em, c='g', ls='-', lw=1, label='RCMIP N2O Emissions')

axs[1].set_title('Input N2O Emissions - RCP60')
axs[1].set_ylabel('Tg')
axs[1].set_xlabel('Year')
axs[1].set_xlim(1765, 2100)
axs[1].set_xticks([1750, 1850, 1950, 2050, 2150, 2250])
axs[1].legend(loc='right')

plt.show()