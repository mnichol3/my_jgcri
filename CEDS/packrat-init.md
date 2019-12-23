# Using Packrat to Manage CEDS Dependencies

[CEDS](https://github.com/JGCRI/CEDS) uses numerous R packages in order to function. However, it needs very specific versions of these packages that, in most cases, are older than the current version. In order to install older versions of these packages without interfering with your global system R installation, an R package environment isolation package is utilized.

[Packrat](https://rstudio.github.io/packrat/) allows users to store project-specific R dependency packages inside their specific project directory, isolating them from other projects and the global R installation. This allows users to install an older verion of a package in the CEDS directory.

## Installing & Initializing Packrat
To install the Packrat package, pen an R prompt and execute the command 
```
> install.packages("packrat")
```
This will add the Packrat package to your R library.

Next, navigate to the directory that will hold your local CEDS repository. For example, if you've already cloned the CEDS repo from GitHub, navigate to that directory
```
> cd ../CEDS
```

**Make sure you are in your CEDS directory**. Packrat needs to initialize a local library in your project's main directory. 

Open a command prompt and start a new R session. To initialize a new local library for your CEDS repository, enter the following command
```
> library(packrat)
> packrat::init(infer.dependencies=F)
```
By default, Packrat will analyze the code already present in the current directory and try to infer the packages it needs to download. This can take a large amount of time, so ensure to include `infer.dependencies=F` as an argument to `packrat::init()`.

If Packrat initialized properly, you should see output similar to the following
```
Adding these packages to packrat:
            _         
    packrat   0.2.0.128

Fetching sources for packrat (0.2.0.128) ... OK (GitHub)
Snapshot written to '/Users/nich980/code/CEDS/packrat/packrat.lock'
Installing packrat (0.2.0.128) ... OK (built source)
init complete!
Packrat mode on. Using library in directory:
- "~code/CEDS/packrat/lib" 
```

## Installing CEDS Dependencies
After ensuring a successful Packrat installation, its time to install the packages we need to run CEDS. Copy the script `ceds_dep_download.R` into your main CEDS directory and run it. It will look for the specific versions of R packages that CEDS needs to run properly and download them if they aren't found. It will also download the packages' dependencies. 

## Known issues
* The `XML` R library sometimes fails to install due to how it be like that sometimes
* You cannot simply copy & paste a Packrat directory into a new CEDS directory. You have to initialize a new Packrat library in the new directory and re-download the CEDS dependency packages
