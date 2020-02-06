# Hector RCMIP
## Brief
The [Reduced Complexity Model Intercomparison Project (RCMIP)](https://www.rcmip.org/) focuses on testing and comparing the abilities of reduced-complexity, simple climate models and emulators to emulate a range of [CMIP6](https://www.wcrp-climate.org/wgcm-cmip/wgcm-cmip6) coupled models. One of the reduced-complexity climate emulators participating in RCMIP is PNNL-Joint Global Change Research Institute's [Hector](https://github.com/JGCRI/hector).

The RCMIP provides a standard protocol for simple and reduced-complexity climate models to be compared to the latest [CMIP6](https://www.wcrp-climate.org/wgcm-cmip/wgcm-cmip6) results. The experiment protocol is broken into multiple phases, the first running until November 2019 and the second planned for 2020, with the ability to add more phases thereafter.  

### Scenarios
The RCMIP experimental protocol is broken up into three tiers, with Tier 1 being the highest priority. Tier 1 scenarios focus on concentration and emissions driven scenarios as well as basic benchmarking tests. Tier 2 and 3 scenarios focus on further examining the behavior of the models. This document discusses how to set up and run scripts to produce Hector variables for submission for RCMIP Tier 1 scenarios.

<br>

## Set-up and Installation
The [`hector-rcmip` repository](https://github.com/ashiklom/hector-rcmip) contains functions and scripts that produce RCMIP output from Hector for submission to RCMIP. Included in the repository is an [renv](https://cran.r-project.org/web/packages/renv/index.html) directory that contains a script to install the dependencies needed to run the Hector RCMIP Tier 1 scenarios. 

In order to take advantage of the `hector-rcmip` package's parallelization, its best to set it up to run on a HPC cluster. This section outlines how to go about installing the package and its dependencies on PNNL's HPC `pic`. 

### 1. Load required modules
It's easiest to load all the required modules we'll need to install the `hector-rcmip` on `pic` at the beginning. We'll need to load `git` to clone the repository, a compiler (`gcc`) to compile the installed R dependency packages, and a few other libraries. 

After starting a new remote session on `pic`, enter the following commands to load the required modules: 
```
module load git
module load R
module load gcc/6.1.0
```

**Notes**
* The default version of R on `pic` is v3.5.1 (as of 1-30-2020). Later on in the installation, `renv` may request R v3.6.2, but 3.5.1 will work fine.
* The default `gcc` compiler on `pic` is a bit outdated. In order to install some R dependency packages, you'll need to explicitly load `gcc/6.1.0` (see [Troubleshooting subsection](#r-package-farver-fails-to-compile-on-pic) for details)


### 2. Clone the `hector-rcmip` repository
The `hector-rcmip` repository can be cloned by entering the following command into the git command prompt:
```
git clone https://github.com/ashiklom/hector-rcmip.git
```

### 3. Install dependencies with `renv`
Once you have a local clone of the repo, `renv` will install all required dependencies. 
* To install the packages from Rstudio: `renv::restore()`
* To install the packages from the command line:
  *  Navigate to the `hector-rcmip` directory and enter the command: `Rscript -e 'renv::restore()`

The `renv` package *should* install itself if not already installed. If this fails, `renv` can be installed manually with `install.packages("renv")`

The following message indicates that `renv` has finished downloading and installing the required packages & dependencies:
```
* The library is already synchronized with the lockfile.
```

<br>

## Reproducing Tier 1 Analysis
The Hector RCMIP Tier 1 analysis can be produced via `hector-rcmipscripts/tier-1-scenarios.R`
* From Rstudio: `source("scripts/tier-1-scenarios.R")`
* From command line: `Rscript scripts/tier-1-scenarios.R`

<br>

## Troubleshooting

* ### Running in parallel on Windows
  The `hector-rcmip` scripts are designed to run in parallel. However, the package that implements parallelization relies on a forking mechanism that exists only on Unix-like systems (Linux, MAC, etc.). Thus, the scripts are unable to be run in parallel on Windows machines.


* ### R package `farver` fails to compile on `pic`
  The automated `renv` package installation script may fail when attempting to compile the `farver` package on `pic` with an error message that looks something like this:
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

  **Solution**: Load a newer version of the `gcc` compiler with `module load gcc/6.1.0` and execute the `renv` installation command again.


* ### R package `rzmq` fails to compile on `pic`
  The automated `renv` package installation script may fail when attempting to compile the `rzmq` package on `pic` with an error message   that looks something like this:
  ```
  Installing rzmq [0.9.6] ...
          FAILED
  Error installing package 'rzmq':
  ================================
  
  * installing *source* package 'rzmq' ...
  ** package 'rzmq' successfully unpacked and MD5 sums checked
  Package libzmq was not found in the pkg-config search path.
  Perhaps you should add the directory containing `libzmq.pc'
  to the PKG_CONFIG_PATH environment variable
  No package 'libzmq' found
  Using PKG_CFLAGS=
  Using PKG_LIBS=-lzmq
  ------------------------- ANTICONF ERROR ---------------------------
  Configuration failed because libzmq was not found. Try installing:
   * deb: libzmq3-dev (Debian, Ubuntu, etc)
   * rpm: zeromq-devel (Fedora, CentOS 7)
   * rpm: zeromq3-devel (RHEL 6, CentOS 6, from EPEL)
   * csw: libzmq1_dev (Solaris)
  If libzmq is already installed, check that 'pkg-config' is in your
  PATH and PKG_CONFIG_PATH contains a libzmq.pc file. If pkg-config
  is unavailable you can set INCLUDE_DIR and LIB_DIR manually via:
  R CMD INSTALL --configure-vars='INCLUDE_DIR=... LIB_DIR=...'
  ```
  
  The R package `rzmq` requires either the `libzmq` or `zeromq` library to be installed. The `zeromq` library is already installed on `pic` (as of 1-30-2020), however it is not properly configured as the error message suggests.
  
  **Solution**: Manually load the `zeromq` module and install the `rzmq` package with the following command:
  ```
  PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/share/apps/zeromq/4.1.4/lib/pkgconfig Rscript -e "install.packages('rzmq')"
  ```
  (Solution courtesy of [Alexey Shiklomanov](https://github.com/ashiklom))
  
  
* ### R package `udunits2` fails to install on `pic`
  The automated `renv` package installation script may fail when attempting to compile the `udunits2` package on `pic` with an error message that looks something like this:
  ```
  Installing udunits2 [0.13] ...
        FAILED
  Error installing package 'udunits2':
  .
  .
  .
  -----Error: udunits2.h not found-----
     If the udunits2 library is installed in a non-standard location,
     use --configure-args='--with-udunits2-lib=/usr/local/lib'
  ...
  ```
  The `udunits2` R package requires the `udunits2` library to already be installed. While it *is* installed on `pic` (`which udunits2` yield `/usr/bin/udunits2`), it appears that its `modulefile` is either misconfigured or absent entirely. Thus, `module load udunits2` will not solve the problem.
  
  **Solution**: Specify the location of `udunits2.h` and manually install the R package with the following command:
  ```
  Rscript -e "install.packages('udunits2',configure.args='--with-udunits2-include=/usr/include/udunits2')"
  ```
