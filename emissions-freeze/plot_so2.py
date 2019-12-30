"""
Plot two SO2 emissions by country sector files
"""
import pandas as pd
import matplotlib.pyplot as plt

from os.path import join

def plot_emissions():
    plt.style.use('ggplot')

    path_cmip = r"C:\Users\nich980\data\CEDS_CMIP6_Release_Archive\final-emissions\current-versions"
    fname_cmip = "CEDS_SO2_emissions_by_country_sector_v_08_31_2018.csv"

    path_frozen = r"C:\Users\nich980\code\CEDS\final-emissions\previous-versions"
    fname_frozen = "CEDS_SO2_emissions_by_country_sector_v_frozen.csv"

    df_cmip = pd.read_csv(join(path_cmip, fname_cmip), sep=',', header=0)

    df_frozen = pd.read_csv(join(path_frozen, fname_frozen), sep=',', header=0)

    # Subset the Qatar iso & 1B_Fugitive sector
    df_cmip = df_cmip[df_cmip['iso'] == 'qat']
    df_cmip = df_cmip[df_cmip['sector'] == '1B_Fugitive']


    # Subset the Qatar iso & 1B_Fugitive sector
    df_frozen = df_frozen[df_frozen['iso'] == 'qat']
    df_frozen = df_frozen[df_frozen['sector'] == '1B_Fugitive']

    # Get x axis values
    x = range(1750, 2015)

    # ignore first 4 values as they're metadata
    vals_cmip = df_cmip.values[0].tolist()[4:]

    vals_frozen = df_frozen.values[0].tolist()[4:]

    # Create pyplot figure
    plt.figure(num=None, figsize=(8,6), facecolor='w', edgecolor='k')
    # plt.figure(num=None, dpi=1200, facecolor='w', edgecolor='k')

    plt.plot(x, vals_cmip, 'g-', label='CMIP6')
    plt.plot(x, vals_frozen, 'r-', label='Frozen')

    plt.xlabel('Year')
    plt.ylabel('Emission Factor')
    plt.title('SO2 Emissions by Country Sector - Qatar 1B_Fugitive')

    plt.grid(True)

    # Adjust left side of x axis limit
    plt.xlim(1950, 2015) 

    x_ticks = range(1950, 2015, 5)
    plt.xticks(x_ticks, x_ticks)

    plt.legend()

    # plt.show()
    out_path = r"C:\Users\nich980\data\e-freeze\debug"
    f_out = "SO2-Divergence-Qatar-1B_Fugitive.pdf"
    plt.savefig(join(out_path, f_out))
    
    
    
def plot_ef():
    plt.style.use('ggplot')
    
    f_path = r"C:\Users\nich980\data\e-freeze\debug"
    f_name = "so2-cmip-v-frozen.csv"
    
    f_abs = join(f_path, f_name)
    
    df = pd.read_csv(f_abs, sep=',', skiprows=4, header=0)
   
    x = df['Year'].tolist()
    cmip = df['CMIP6'].tolist()
    frozen = df['Frozen'].tolist()

    plt.figure(num=None, figsize=(8,6), facecolor='w', edgecolor='k')
    
    plt.plot(x, cmip, 'g-', label='CMIP6')
    plt.plot(x, frozen, 'r-', label='Frozen')

    plt.xlabel('Year')
    plt.ylabel('Emission Factor')
    plt.title('SO2 Emission Factors - Qatar 1B2_Fugitive-petr-and-gas')

    plt.grid(True)

    # Adjust left side of x axis limit
    plt.xlim(1950, 2015) 

    x_ticks = range(1950, 2015, 5)
    plt.xticks(x_ticks, x_ticks)

    plt.legend()

    # plt.show()
    f_out = "SO2-Divergence-Qatar-1B2_Fugitive-petr-and-gas.pdf"
    plt.savefig(join(f_path, f_out))


def main():
    plot_ef()
    


if __name__ == '__main__':
    main()
