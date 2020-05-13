# CEDS Developer's Notes
Last updated 13 May 2020

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
  

  
# R Dependency Packages
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

This is due to the package's C++ backend using features that the default `gcc` complier on `pic` is unaware of due to it being an older version. 

### Solution
Load a newer version (6.1.0 works as of 13 May 2020) of the `gcc` compiler via `module load gcc/6.1.0`.
  
  ---
  
### R package `ncdf4` fails to compile on pic HPC cluster
CEDS only uses the `ncdf4` package within the gridding module to produce gridded emissions files. The package is not required to produce CEDS emissions CSV files.
  
`ncdf4` depends on an `nc-config` file that ships with the NetCDF library. The NetCDF C library is installed on pic, but is not loaded as a module at the beginning of a remote session. Attempting to install the R `ncdf4` package without the `netcdf` module loaded into your session can result in the following error:
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
