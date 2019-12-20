# Workflow to produce final emissions from frozen emission factor files
This document describes the workflow used to produce "frozen" emission factor files (where emission factors for years after 1970 are set to their 1970 value).

## 1. Producing Frozen Emission Factor Files
The directory `code/my_jgcri/emissions-freeze` holds numerous scripts written to produce frozen emission factor (EF) files from CEDS EF files. 

`validate.py` holds the function `diff_activity_files` that compares all of the emission species activity files found in a given directory, as they should all be the same. However, it appears that CH4 likes to by difficult as its activity file does not match any of the activity files for other species.

`main.py` contains a series of functions that handle the emission factor freezing and production of final emissions files. First, `freeze_emissions` retrieves all of the emission factor files in a given directory and freezes the emission factors for every combustion sector for all isos and fuels. It then writes the resulting EF DataFrames to a directory. In this case, that directory is `.../data/e-freeze/dat_out/ef_files/`. File names follow the CEDS naming conventions (e.g., `H.CH4_total_EFs_extended.csv`). 

Next, `calc_emissions` computes the total emissions for the given emissions species using the frozen emission factor files and the equation `Total Emissions = Emission Factor x Activity`. Again, these files follow the CEDS naming conventions (e.g., `NH3_total_CEDS_emissions.csv`) and are written to `.../data/e-freeze/dat_out/frozen_emissions/`

## 2. Producing Emission Summary Data
Tthe next step is to produce final emission files using the CEDS `S1.1.write_summary_data.R` script. 

The easiest way to do this is to copy and paste the frozen emission files from `/data/e-freeze/dat_out/frozen_emissions/` to `code/CEDS/intermediate-output`, then execute the script `/code/my_jgcri/emissions-freeze/make_final_emissions.R`. The resulting emission summary files will be placed in `/code/CEDS/final-emissions/current-versions`

## 3. Compare Frozen Emissions to Normal Emissions
The final step is to create plots comparing the frozen emissions to normal emissions using the `CEDS_version_comparison.R` script located in `/code/CEDS_Data/code`. 

First, ensure that the `CEDS` and `CEDS_Data` directories are in the same parent directory (`/code` in this case). Check that the CEDS version of the summary data files produced in step 2 match the `current_CEDS_version` variable defined in `CEDS_version_comparison.R` (line 66). Copy the normal CEDS emissions into the `CEDS/final-emissions/previous-versions` directory and ensure that their CEDS version matches the `previous_CEDS_version` in line 62 of `CEDS_version_comparison.R`. 

Within RStudio, set the current working directory to the `CEDS_Data` directory, and run the script. Assuming there are no errors (ahem, CH4), comparison `.pdf` graphs should be placed in `/CEDS/final-emissions/diagnostics`

## Summary
### Produce Frozen Emission Factor Files
  1. Run `code/my_jgcri/emissions-freeze/main.py` to produce frozen EF files and final emission files
### Produce Emission Summary Data
  1. Copy and paste the frozen emission files from `/data/e-freeze/dat_out/frozen_emissions/` to `code/CEDS/intermediate-output` 
  2. Run `/code/my_jgcri/emissions-freeze/make_final_emissions.R`
### Compare Frozen Emissions to Normal Emissions
  1. Configure the `current_CEDS_version` and `previous_CEDS_version` in `CEDS_version_comparison.R` to match the frozen emission & normal emission versions
  2. Run `CEDS_version_comparison.R`
  3. Comparison plots will be placed into `/CEDS/final-emissions/diagnostics`
