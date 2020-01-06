#### 6 Jan 2020
Matt Nicholson

# Creating CEDS Gridding Paper Plots

This document serves as a quick how-to for creating the CEDS gridded data plots used in *Gridded Emissions for CMIP6* by Feng et. al, 2020.

## 1. Set up the CEDS_Data Repository on pic
1. Download the `CEDS_Data` repository from Github into your working directory on pic. 
   * *Note: While the scripts will work on a Windows system, the available fonts are severely limited. For best results, use a Unix-based system*

2. Checkout the `gridfigs` branch. The scripts needed to create the plots are located in `code/gridding-paper-figures`.
3. Copy & paste the gridded emissions files into their respective directories
   * Paste historical gridded emission files into `emission-archives/CEDS_grids/historical-emissions`
   * Paste future/scenario gridded emission files into `emission-archives/CEDS_grids/gridded-emissions`
   * Ensure the directory variables in `gridding_paper_figures.R` point to the proper directories. Ex:
     ```
     BASE_DIR <- './code/gridding-paper-figures'
     GRIDDED_EMS_DIR <- './emission-archives/CEDS_grids/gridded-emissions'
     HISTORICAL_EMS_DIR <- './emission-archives/CEDS_grids/historical-emissions'
     OUT_DIR <- './output/gridding-paper-figures'
     ```
     
     
## 2. Re-aggregate the Gridded Data

The grid plotting scripts only accept grids with a nominal grid resolution of 0.5 degrees (50 km, 720 lons x 360 lats). However, gridded historical openburning emissions files produced by Vrije Universiteit Amsterdam and obtained from the [ESGF website](https://esgf-node.llnl.gov/search/input4mips) have a nominal resolution of 0.25 degrees (25 km; 1440 lons x 720 lats). The plotting are unable to handle these grids, so the data must be re-aggregated to a 0.5 deg grid.

The easiest way to re-aggregate 0.25 deg gridded emissions data onto a 0.5 deg grid is by utilizing the [Climate Data Operators (cdo) toolset](https://code.mpimet.mpg.de/projects/cdo). Hopefully you're using a Unix-based or Windows 10 system. If not, good luck.

### 2.1 Installing cdo on Windows 10

Although cdo can by installed on Windows 10 by utilizing cygwin, the most easiest method of installation is by utilizing Windows 10's [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10). 

After [enabling Windows Subsystem for Linux](https://www.onmsft.com/how-to/how-to-install-windows-10s-linux-subsystem-on-your-pc) and installing your distro of choice (I chose Ubuntu), installing cdo is simple. Open your Linux distro app and enter the following command in to the Linux command prompt:
```
sudo apt-get install cdo
```

### 2.2 Create a cdo grid description file

Cdo is able to take a grid description file as an argument. This file defines the grid that the data will be re-aggregated on. If no grid description is given, or if a simple `720x360` description is given, the data will be re-aggregated onto a grid with longitude values the span `[0, 359.5]`. Since the plotting scripts expect longitude values of `[-179.75, 179.75]`, the resulting plots will be incorrect.

The following grid description file (`cdo-grid-in.txt`) gets cdo to re-aggregate the data on to the correct 0.5 degree grid:
```
gridtype = lonlat
xsize = 720
ysize = 360
xfirst = -179.75
xinc = 0.5
yfirst = -89.75
yinc = 0.5
```

### 2.3 Re-aggregate the gridded data
Once you have cdo installed & the grid description file configures, re-aggregating the gridded data is simple, especially since we're going from a smaller grid to a larger one. We'll use the first-order conservative remapping function [`remapconn`](https://code.mpimet.mpg.de/projects/cdo/embedded/index.html#x1-6290002.12.5)

In the Linux command prompt, enter the following command to re-aggregate the data from the file `biomassburning_input4MIPs.nc` and write it to a file of the same name:
```
cdo -f nc4 remapcon,cdo-grid-in.txt biomassburning_input4MIPs.nc biomassburning_input4MIPs.nc
```
   
