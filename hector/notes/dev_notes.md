# Hector Dev Notes

## Components

## Functionality

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
