# Hector RCMIP
## Brief
The [Reduced Complexity Model Intercomparison Project (RCMIP)](https://www.rcmip.org/) focuses on testing and comparing the abilities of reduced-complexity, simple climate models and emulators to emulate a range of [CMIP6](https://www.wcrp-climate.org/wgcm-cmip/wgcm-cmip6) coupled models. One of the reduced-complexity climate emulators participating in RCMIP is PNNL-Joint Global Change Research Institute's [Hector](https://github.com/JGCRI/hector).

The RCMIP provides a standard protocol for simple and reduced-complexity climate models to be compared to the latest [CMIP6](https://www.wcrp-climate.org/wgcm-cmip/wgcm-cmip6) results. The experiment protocol is broken into multiple phases, the first running until November 2019 and the second planned for 2020, with the ability to add more phases thereafter.  

### Scenarios
The RCMIP experimental protocol is broken up into three tiers, with Tier 1 being the highest priority. Tier 1 scenarios focus on concentration and emissions driven scenarios as well as basic benchmarking tests. Tier 2 and 3 scenarios focus on further examining the behavior of the models. This document discusses how to set up and run scripts to produce Hector variables for submission for RCMIP Tier 1 scenarios.

## Set-up and Installation
The [`hector-rcmip` repository](https://github.com/ashiklom/hector-rcmip) contains functions and scripts that produce RCMIP output from Hector for submission to RCMIP. Included in the repository is an [renv](https://cran.r-project.org/web/packages/renv/index.html) directory that contains a script to install the dependencies needed to run the Hector RCMIP Tier 1 scenarios. 

### 1. Clone the `hector-rcmip` repository
The `hector-rcmip` repository can be cloned by entering the following command into the git command prompt:
```
git clone https://github.com/ashiklom/hector-rcmip.git
```

### 2. Install dependencies with `renv`
Once you have a local clone of the repo, `renv` will install all required dependencies. 
* To install the packages from Rstudio: `renv::restore()`
* To install the packages from the command line:
  *  Navigate to the `hector-rcmip` directory and enter the command: `Rscript -e 'renv::restore()`

The `renv` package *should* install itself if not already installed. If this fails, `renv` can be installed manually with `install.packages("renv")`

### Notes
* The `hector-rcmip` scripts are designed to run in parallel. However, the package that implements parallelization relies on a forking mechanism that exists only on Unix-like systems. Thus, the scripts are unable to be run in parallel on Windows machines. 


## Reproducing Tier 1 Analysis
The Hector RCMIP Tier 1 analysis can be produced via `hector-rcmipscripts/tier-1-scenarios.R`
* From Rstudio: `source("scripts/tier-1-scenarios.R")`
* From command line: `Rscript scripts/tier-1-scenarios.R`


## Troubleshooting

### R package `farver` fails to compile on `pic`
The automated `renv` package installation script may fail when attempting to compile the `farver` package on `pic` with an error message that looks something like this:
```
* installing *source* package 'farver' ...
** package 'farver' successfully unpacked and MD5 sums checked
** libs
g++ -std=gnu++0x -I"/share/apps/R/3.5.1/lib64/R/include" -DNDEBUG   -I/usr/local/include   -fpic  -I/share/apps/R/3.5.1/include -c ColorSpace.cpp -o ColorSpace.o
In file included from ColorSpace.cpp:1:
ColorSpace.h:19: error: ISO C++ forbids initialization of member 'valid'
ColorSpace.h:19: error: making 'valid' static
ColorSpace.h:19: error: ISO C++ forbids in-class initialization of non-const static member 'valid'
make: *** [ColorSpace.o] Error 1
ERROR: compilation failed for package 'farver'
```

This is due to the package's C++ backend using features that the default `gcc` complier on `pic` is unaware of due to it being an older version. 

**Solution**: Load a newer version of the `gcc` compiler with `module load gcc/6.1.0` and execute the `renv` installation command again.
