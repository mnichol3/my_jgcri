Hector Dev Notes
=================
This document holds tips, tricks, and other various snippets that I find extremely helpful when contributing to the development of [The Hector Simple Climate Model ](https://github.com/JGCRI/hector) 


## Structure
Hector currently consists of two main parts: a front-end, written in R; and a C++ back-end. The Hector R package provides a simple, user-friendly interface and utilizes the `Rcpp` package to flawlessly interface with the C++ backend, which does all the heavy lifting. Using a compiled back-end allows thousands of Hector runs to be executed in a matter of minutes. 

### R Interface



## Functionality



## Package Data
The Hector package comes with its own package data, located in `R/sysdata.rda`. In order for modifications to the data files in `data-raw/` to take effect, you re-build `sysdata.rda`. Not re-building the package data after implementing changes to R API function or variable names is a common cause of integration test failures on Github.

### Re-build sysdata in Rstudio
To re-build the package data after making changes, navigate to the `data-raw` directory and open the data file you modified. Source the file, then click `Install and Restart`. This will add the new data to `sysdata.rda`

**Example**

For example, development of the `fetchvars_all` function required a data file containing names of Hector variables to be added to the package data. A tab-delimited text file was placed in `data-raw/`, and a function that opened the file and read the data was added to `data-raw/units-data.R`. 

In order to make the data from the text file available to the R functions, `sysdata.rda` needs to be updated. 

1. Open & source `units-data.R`
  Since the function that reads the data from the text file is located in `data-raw/units-data.R`, sourcing the file will make Rstudio read the data file. 
  You can either use the command `source('...hector/data-raw/units-data.R')` or open the `data-raw/units-data.R` file and click the **Source** button located in the top right corner of the editor pane.

    A message will be displayed on the console that looks something like this:
    ```
    > source('C:/Users/nich980/code/hector/data-raw/units-data.R')
    ✔ Setting active project to 'C:/Users/nich980/code/hector'
    ✔ Saving 'unitstable' to 'R/sysdata.rda'
    ```

2. Re-build the package by clicking the **Install and Restart** button under the **Build** tab of the environment pane

Thats it! Your `sysdata.rda` file is now updated.



## Input files
Hector relies on input files located in `input/` in order to run. The The primary input file that drives Hector 
is an [INI-style](https://en.wikipedia.org/wiki/INI_file) text file. 

### .ini files
**Problem**: Hector is looking for halocarbon species that the emissions dataset does not have data for
**Solution**: Use species data in RCP45 emissions file that comes with Hector

**Details**
After creating `.ini` files for new scenarios, Hector raised the following error:
```
Error in newcore_impl(inifile, loglevel, suppresslogging, name) : 
  During hector core setup: msg:  	Assertion failed: tau has bad value
func: 	prepareToRun
file: 	halocarbon_component.cpp
ffile:	halocarbon_component.cpp

line: 	132
```
After inspecting the new scenario emission file (`/input/emissions/gas_paris_med.csv`) and logs, it was determined that
there were numerous halocarbon species that Hector expected but were not included in the input file. Since no input data
was being passed to the halocarbon component constructor, the component was being initialized with an invalid `tau` value. 


An attempt to remedy this issue was made by simply commenting-out the sections of missing halocarbon components in the
`.ini` file. **This did not work.**

The recommended solution is to utilize the `enabled` flag in the component's section of the `.ini` file. If `enabled=0`,
the component will be disabled. For example, below is the now-defunct `onelineocean` component section from `hector_rcp45.ini`:
```
;------------------------------------------------------------------------
[onelineocean]
enabled=0			; 'enabled=0' will disable any component
;output=0			; 'output=0' will disable any component's output
ocean_c=38000		; Pg C
```
By setting `enabled=0`, Hector will ignore this component.

The final solution, completeness in mind, was to source emission data not included in `gas_paris_med.csv` from 
`hector_rcp45.csv`.



## Rstudio Shortcuts
Below are some helpful Rstudio keyboard shortcuts that I can't seem to memorize no matter how many times I use them. This is not meant to be an exhaustive list. See the [Rstudio docs](https://support.rstudio.com/hc/en-us/articles/200711853-Keyboard-Shortcuts) for a complete list of default keyboard shortcuts.

Note: The shortcuts listed below are the Windows/Linux versions. Mac is for nerds. 

### Source Editor
* Comment/uncomment lines : `Crtl + Shift + C`
* Open document: `Crtl + O`
* Save active document: `Ctrl + S`
* Close active document: `Ctrl + W`
* Close all open documents: `Crtl + Shift + W`

* Run current line/selection: `Ctrl + Enter`
* Source a file: `Ctrl + Shift + O`

* Go to line: `Shift + Alt + G`
* Jump to: `Shift + Alt + J`
* Previous tab: `Ctrl + F11`
* Next tab: `Ctrl + F12`
* First tab: `Ctrl + Shift + F11` 
* Last tab: `Ctrl + Shift + F12`
* Find and Replace: `Ctrl + F`

### Build
* Build and Reload: `Ctrl + Shift + B`
* Load All (devtools): `Ctrl + Shift + L`
* Test Package: `Ctrl + Shift + T`
* Check Package: `Ctrl + Shift + E`
* Document Package: `Crtl + Shift + D`

### Git
* Diff active source document: `Ctrl + Alt + D`
* Commit changes: `Ctrl + Alt + M`
* Scroll diff view: `Ctrl + Up/Down`
* Stage/Unstage: `Spacebar`
* Stage/Unstage and move to next: `Enter`

### Session
* Quit Session: `Ctrl + Q`
* Restart R Session: `Ctrl + Shift + F10`
