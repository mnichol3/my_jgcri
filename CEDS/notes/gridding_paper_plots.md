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

### 2.1 Check Grid Resolution

To quickly check the gridded data resolution, use your favorite programming language or netCDF4 utility program (such as [NASA's Panoply](https://www.giss.nasa.gov/tools/panoply/)) to view the file's `grid` global attribute. 

For example, using Python 3.6:
```python
> from netCDF4 import Dataset
> f_in = 'gridded-biomassburning_input4MIPs_file.nc'
> nc = Dataset(f_in, 'r')
>  nc.getncattr('grid')
'0.25x0.25 degree latitudexlongitude'
```

Or using R 3.6:
```r
> library(ncdf4)
> nc_in <- 'gridded-biomassburning_input4MIPs_file.nc'
> nc <- nc_open(nc_in)
> ncatt_get(nc, varid=0, attname='grid')$value
'0.25x0.25 degree latitudexlongitude'
```

In the above examples, the file's grid resolution is `0.25x0.25` degrees, so the gridded emissions **must** be re-aggreagated on to a 0.5 x 0.5 degree grid before the file can be passed to the plotting functions. However, if the file's `grid` resolution was `'0.5x0.5 degree latitudexlongitude'`, it could be passed to the plotting functions as-is (Sec 3).


### 2.2 Installing cdo on Windows 10

The easiest way to re-aggregate 0.25 deg gridded emissions data onto a 0.5 deg grid is by utilizing the [Climate Data Operators (cdo) toolset](https://code.mpimet.mpg.de/projects/cdo). Hopefully you're using a Unix-based or Windows 10 system. If not, good luck.

Although cdo can by installed on Windows 10 by utilizing cygwin, the most easiest method of installation is by utilizing Windows 10's [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10). 

After [enabling Windows Subsystem for Linux](https://www.onmsft.com/how-to/how-to-install-windows-10s-linux-subsystem-on-your-pc) and installing your distro of choice (I chose Ubuntu), [installing cdo is simple](https://code.mpimet.mpg.de/projects/cdo/wiki/Win32#Windows-10) Open your Linux distro app and enter the following command in to the Linux command prompt:
```
sudo apt-get install cdo
```

cdo netCDF & hdf5 support troubleshooting info can be found [here](https://github.com/koldunovn/nk_public_notebooks/blob/master/Install%20climate%20data%20operators%20(cdo)%20on%20Ubuntu%20with%20netCDF4%20and%20hdf5%20support.ipynb)

### 2.3 Create a cdo grid description file

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

### 2.4 Re-aggregate the gridded data
Once you have cdo installed & the grid description file configures, re-aggregating the gridded data is simple, especially since we're going from a smaller grid to a larger one. We'll use the first-order conservative remapping function [`remapconn`](https://code.mpimet.mpg.de/projects/cdo/embedded/index.html#x1-6290002.12.5)

In the Linux command prompt, enter the following command to re-aggregate the data from the file `biomassburning_input4MIPs.nc` and write it to a file of the same name:
```
cdo -f nc4 remapcon,cdo-grid-in.txt biomassburning_input4MIPs.nc biomassburning_input4MIPs.nc
```

Since the files are rather large, it takes ~55 minutes to re-grid a single file. Because of this, its advantageous to write a script to re-grid multiple files and let it run overnight. The following bash script, `re-grid.sh`, accomplishes this:

```bash
#!/bin/sh

DIR_INPUT=./openburning-gridded
DIR_OUTPUT=./re-grid-new

for f_in in ./openburning-gridded/*.nc; do
    filename="${f_in##*/}"
    f_out="${DIR_OUTPUT}/${filename}"
    
    echo "Processing $filename"
    cdo -f nc4 remapcon,cdo-grid-in.txt "$f_in" "$f_out"
done
```

The script iterates over every netCDF file found in the `./openburning-gridded` directory, passes it to the cdo `remapcon` function along with the `cdo-grid-in.txt` grid description file, the writes the resulting re-aggregated gridded data to the `./openburning-regridded` directory. It takes approximately 7 hours to process 8 gridded historical openburning emission files.

After re-aggregating the data on to the proper grid, copy & paste them into the proper `emission-archives/CEDS_grids/...` directory. For the historical openburning files metioned previously in this section, they belong in `emission-archives/CEDS_grids/historical-emissions`.

*Note: The cdo command does not compress the resulting netCDF4 files. The average size of one of these files is around 1.95 GB* 


## 3. Executing the Plotting Scripts

Once you have the `CEDS_Data` repo configured and the proper files in the proper folders, running the gridded emissions plotting scripts is simple.

The script `CEDS_Data/code/gridding-paper-figures/generate_all.R` handles all the operations necessary to produce all the gridded emissions plots. On pic, move the script to the main `CEDS_Data` directory and invoke it with a bash script:
```bash
#!/bin/bash
#######################################
### typical SBATCH variables & defs ### 
#######################################

module purge
module load R/3.3.3

cd /pic/projects/GCAM/path/to/CEDS_Data
Rscript generate_all.R
```

Alternatively, it can invoked in an interactive-job by the following:
```
module load R/3.3.3
cd /pic/projects/GCAM/path/to/CEDS_Data
Rscript generate_all.R
```

The output plots will be put in the directory defined by `OUT_DIR` in `gridding_paper_functions.R`. I created the directory `CEDS_Data/output/gridding-paper-figures` and had them placed there. 
