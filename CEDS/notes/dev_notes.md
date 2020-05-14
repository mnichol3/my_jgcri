# CEDS Developer's Notes
Last updated 14 May 2020

## Table of Contents
* [R Dependency Packages](#r-dependency-packages)
* [R Library Management with `renv`](r-library-management-with-renv)
* [CEDS_Data](#CEDS_Data)

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
### Solution
Cry.

<br>


# R Library Management with `renv`
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
