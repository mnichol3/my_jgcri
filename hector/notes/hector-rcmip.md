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
