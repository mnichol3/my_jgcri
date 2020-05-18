# CEDS Developer's Notes
Last updated 15 May 2020

## Table of Contents
* [R Dependency Packages](#r-dependency-packages)
* [R Library Management with renv](#r-library-management-with-renv)
* [CEDS Gridding Module](#ceds-gridding-module)
* [CEDS_Data](#ceds-data)

# R Dependency Packages
## Version Validation
Currently, CEDS attempts to validate the R dependency package version the user has installed. If the version of an installed package is below the required version, the following error will be raised:
```
Package <pkg_name> version <pkg_version> or greater is required.
```

Similarly, if CEDS is unable to load a required R package, the following error will be raised:
```
Couldn't load <pkg_name>. Please install.
```

CEDS R package version definitions are located in `CEDS/code/parameters/global_settings.R`


## Troubleshooting
### R package `farver` fails to compile on pic HPC cluster
The installation of the `farcer` package may fail when attempting to compile, resulting in an error message that looks something like this:
  ```
  * installing *source* package 'farver' ...
  ** package 'farver' successfully unpacked and MD5 sums checked
  ** libs
  g++ -std=gnu++0x -I"/share/apps/R/3.5.1/lib64/R/include" -DNDEBUG   -I/usr/local/include   -fpic  -I/share/apps/R/3.5.1/include -c     ColorSpace.cpp -o ColorSpace.o
  In file included from ColorSpace.cpp:1:
  ColorSpace.h:19: error: ISO C++ forbids initialization of member 'valid'
  ColorSpace.h:19: error: making 'valid' static
  ColorSpace.h:19: error: ISO C++ forbids in-class initialization of non-const static member 'valid'
  make: *** [ColorSpace.o] Error 1
  ERROR: compilation failed for package 'farver'
  ```

This is due to the package's C++ backend using features that the default `gcc` complier on `pic` is unaware of due to it being an older version (`gcc 4.4.7` is still default as of 12 May 2020). 

### Solution
Load a newer version (6.1.0 works as of 13 May 2020) of the `gcc` compiler via `module load gcc/6.1.0`.
  
  ---
  
### R package `ncdf4` fails to compile on pic HPC cluster
CEDS only uses the `ncdf4` package within the gridding module to produce gridded emissions files. The package is not required to produce CEDS emissions CSV files.
  
`ncdf4` depends on an `nc-config` file that ships with the [Unidata NetCDF library](https://www.unidata.ucar.edu/software/netcdf/). **The Unidata NetCDF library is a [documented system requirement](https://cran.r-project.org/web/packages/ncdf4/index.html) for the R ncdf4 package.** The NetCDF C library is installed on pic, but is not loaded as a module at the beginning of a remote session. Attempting to install the R `ncdf4` package without the `netcdf` module loaded into your session can result in the following error:
  ```
  Installing ncdf4 [1.16] ...
          FAILED
  Error installing package 'ncdf4':
  =================================
  * installing *source* package 'ncdf4' ...
  ** package 'ncdf4' successfully unpacked and MD5 sums checked
  configure.ac: starting
  checking for nc-config... no
  -----------------------------------------------------------------------------------
  Error, nc-config not found or not executable.  This is a script that comes with the
  netcdf library, version 4.1-beta2 or later, and must be present for configuration
  to succeed.
  ```
  
### Solution
Load the `netcdf` library into your session via the command `module load netcdf`.

---

### Unable to Locate ICU4C library
[ICU](http://userguide.icu-project.org/intro) is a cross-platform Unicode based globalization library. It includes support for locale-sensitive string comparison, date/time/number/currency/message formatting, text boundary detection, character set conversion and so on. 
When attempting the install some R packages, such as `stringi v1.2.2`, the `ICU4C` library is unable to be located and the installation fails:
```
checking for pkg-config... /usr/bin/pkg-config
checking with pkg-config for the system ICU4C... no
*** pkg-config did not detect ICU4C-devel libraries installed
*** Trying with "standard" fallback flags
checking whether we may build an ICU4C-based project... no
*** The available ICU4C cannot be used
checking whether we may compile src/icu61/common/putil.cpp... no
checking whether we may compile src/icu61/common/putil.cpp with -D_XPG6... no
*** The ICU4C bundle could not be build. Upgrade your compiler flags.
ERROR: configuration failed for package 'stringi'
* removing '/pic/projects/GCAM/mnichol/ceds/CEDS-dev/renv/staging/1/stringi'
Error: install of package 'stringi' failed
```
### Solution 1
Load a newer compiler into your remote session: `module load gcc/7.3.0` (`gcc/7.3.0` works as of 15 May 2020).

### Solution 2
Use the `install.packages` function to modify the compiler flags used in the installation process:
```R
install.packages(c("stringi"),configure.args=c("--disable-cxx11"), lib=lib)
```
Use the `lib` argument to install the package into your project's `renv` library (can be found using `.libPaths()`). 

**NOTE** This solution is fine for only installing `stringi`, however it may not completely resolve the problem when `stringi` is being installed as a dependency for another R package through `renv`.

---

<br>


# R Library Management with renv
[`renv`](https://rstudio.github.io/renv/index.html) is an R package that allows users to create reproduceable, project-specific R libraries. This gives users the ability to create a CEDS-specific R library such that installing the older package versions CEDS requires will not affect their global R library.

## Set Up & Installation
**TODO**

## Troubleshooting
This section contains troubleshooting solutions related **only** to the installation of packages and management of libraries via `renv`. For general R package installation troubleshooting, see the troubleshooting sub-section in [R Dependency Packages](#r-dependency-packages)

### Package cache linking
`renv` has the ability to link packages from a user's global R library to their project-specific `renv` library, saving the time and space that re-downloading the same package and version a second time. However, once this cache link is established, removing the package from the global R library will break the link, causing errors in the `renv` library.

An example error message is below. This message resulted from the cache link between the CEDS `renv` library and global R library being broken for the `stringi` package when attempting to load the `stringr` package, which depends on `stringi`:
```
Error in dyn.load(file, DLLpath = DLLpath, ...) :
  unable to load shared object '/qfs/people/nich980/.local/share/renv/cache/v5/R-3.3/x86_64-pc-linux-gnu/stringi/1.2.2/e99d8d656980d2dd416a962ae55aec90/stringi/libs/stringi.so':
  /usr/lib64/libstdc++.so.6: version `CXXABI_1.3.8' not found (required by /qfs/people/nich980/.local/share/renv/cache/v5/R-3.3/x86_64-pc-linux-gnu/stringi/1.2.2/e99d8d656980d2dd416a962ae55aec90/stringi/libs/stringi.so)
Couldn't load 'stringr'. Please Install.
```
### Solution
Manually install the package dependency in question into the project `renv` library, using the [`library`](https://rstudio.github.io/renv/reference/install.html#arguments) and [`rebuild`](https://rstudio.github.io/renv/reference/install.html#arguments) arguments:
```R
> .libPaths()
[1] "/pic/projects/GCAM/mnichol/ceds/CEDS-dev/renv/library/R-3.3/x86_64-pc-linux-gnu"
[2] "/tmp/RtmpofmJy0/renv-system-library"
> lib <- .libPaths()[1]  # CEDS renv library
> renv::install("stringi@1.2.2", library=lib, rebuild=TRUE)
```
This forces `renv` to install the package in the local library, rather than attempting to create another cache link.


<br>


# CEDS Gridding Module
CEDS contains code to produce 0.5 degree x 0.5 degree gridded emissions, both annually as well as in multi-year chunks. The main gridding scripts are located in `code/module-G` while the core gridding and NetCDF I/O functions are located in `code/parameters/gridding_functions.R` and `code/parameters/nc_generation_functions.R`. 

## Execution
The gridding scripts can be called from the Makefile. However, it is important to note that the gridding targets in the Makefile call the `Module-H` functions before calling the actual gridding functions. 

If you wish to *only* execute the gridding scripts, you must call them via the command line. For example, to grid and chunk `BC` bulk and biofuel emissions with custom `Module-H` intermediate output files, the command would be:
```
# Grid & chunk bulk emissions
Rscript code/module-G/G1.1.grid_bulk_emissions.R BC --nosave --no-restore
Rscript code/module-G/G2.1.chunk_bulk_emissions.R BC --nosave --no-restore 

# Grid & chunk biofuel emissions
Rscript code/module-G/G1.4.grid_solidbiofuel_emissions.R BC --nosave --no-restore
Rscript code/module-G/G2.4.chunk_solidbiofuel_emissions.R BC --nosave --no-restore
```

## Gridding & Chunking
As previously mentioned, the gridding module produces annual emissions grids (written to `intermediate-output/gridded-emissions`) as well as files containing multi-year chunks of gridded emissions (written to `final-emissions/gridded-emissions`). 

### Gridding Start & End Years
The year at which gridding and chunking starts is set by the `start_year` parameter in `code/parameters/common_data.R`. However, this is a mutable global variable that doesn't always get sourced, depending on how you call the gridding and chunking functions. `start_year` can be hard-coded within the `Module-G` gridding scripts, in the `gridding_initialize()` function call.

For example, to ensure the gridding and chunking starts at 1950 and ends at 2014 (inclusive), within `code/module-G/G1.1.grid_bulk_emissions.R`, set the values of the `start_year` and `end_year` arguments in the `gridding_initialize()` function call:
```
gridding_initialize(grid_resolution = 0.5, 
                    start_year = 1950,
                    end_year = 2014,
                    ...
                    )
```

### Chunking Start & End Years
To hard-code the start and end years of grid chunking, as well as the chunking interval, navigate to the `chunk_emissions()` function in `code/parameters/nc_generation_functions.R` and modify the `start_year`, `end_year`, and `chunk_years`, respectively.

## Misc Notes
* Saving Execution Time
  * Only grid and chunk emissions for years you need. If you only want 1950-2014, don't waste time by starting the gridding & chunking all the way back at 1750.
  * Users can re-run chunking without re-running gridding, as long as the annual grids are present in `intermediate-output/gridded-  emissions` for the years specified in the chunking script. 


<br>


# CEDS_Data
## Version Comparison Scripts
The CEDS version comparison script, `CEDS_version_comparison.R`, is located in `CEDS_Data/code` or `CEDS_Data/code/version-comparison`.
### Set Up
* Your `CEDS` and `CEDS_Data` directories must be located within the same parent directory. You directory structure should look something like this:
  ```
  parent_dir/
      |
      |- CEDS/
      |
      | - CEDS_Data/
  ```
* Place the current CEDS version's emissions in `CEDS/final-emissions/current-versions`
* Place the previous CEDS version's emissions in `CEDS/final-emissions/previous-versions` or `CEDS_Data/emissions-archive`???

### Execution
* Due to how the relative paths within the script are constructed, the working directory must be the root `CEDS_Data` directory.

### Output
Ouput should be written to `.../CEDS/final-emissions/diagnostics/version-comparisons/` (line 1404), however in my experience it is instead written to `.../CEDS/final-emissions/diagnostics` for an unknown reason.

### Modification
* CEDS versions
  * Change previous CEDS version
    * Line 100 - `previous_CEDS_version`
  * Change current CEDS version
    * Line 108 - `current_CEDS_version`
* CEDS emissions species
  * Line 113 - `em_list <- c( "BC", "CH4", ...)`
* CEDS directory path (Ex: use `CEDS-dev` directory; replace `<CEDS-dir>` with your desired CEDS directory.)
  * Line 69   - `PARAM_DIR <- "../<CEDS_dir>/code/parameters/"`
  * Line 82   - `PARAM_DIR <- "../<CEDS_dir>/code/parameters/"`
  * Line 176  - `setwd( "../../<CEDS_dir>/input" )`
  * Line 1383 - `setwd( "../../<CEDS_dir>/input" )`
  * Line 1642 - `setwd( "../../../../CEDS/input" )`
