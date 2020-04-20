# Speciated-VOC Chunking

**Issue**: Speciated-VOC chunking function results in segmentation fault:
```
Mon Apr 20 11:26:47 2020 G2.2.chunk_subVOC_emissions.R [ 1 ] : -----
Mon Apr 20 11:26:47 2020 G2.2.chunk_subVOC_emissions.R [ 1 ] : Starting G2.2.chunk_subVOC_emissions.R
Mon Apr 20 11:26:47 2020 G2.2.chunk_subVOC_emissions.R [ 1 ] : Generates chunk NetCDF files for subVOC emissions
Mon Apr 20 11:26:47 2020 G2.2.chunk_subVOC_emissions.R [ 1 ] : Reading ../input/gridding/gridding_mappings/VOC_id_name_mapping.csv
Done:  23  rows,  3  cols
Mon Apr 20 11:26:48 2020 G2.2.chunk_subVOC_emissions.R [ 1 ] : Start NMVOC grids chunking from 1950 to 2014

*** caught segfault ***
address (nil), cause 'memory not mapped'

Traceback:
1: .C("R_nc4_put_att_text", as.integer(ncid), as.integer(varid),     as.character(attname), as.integer(typetocreate), as.integer(length(attval)),     attval, error = as.integer(rv$error), PACKAGE = "ncdf4",     NAOK = TRUE)
2: ncatt_put_inner(nc$id, -1, attname, attval, prec = prec, verbose = verbose,     definemode = definemode)
3: ncatt_put(nc_new, 0, "VOC_name", VOC_name)
4: singleVarChunkingFun(em, grid_resolution, chunk_start_years,     chunk_end_years, chunk_count_index, input_dir, output_dir,     ...)
5: chunk_emissions(singleVarChunking_subVOCemissions, em, VOC_names = VOC_names)
An irrecoverable exception occurred. R is aborting now ...
/tmp/slurmd/job13187507/slurm_script: line 45:  9886 Segmentation fault      Rscript code/module-G/G2.2.chunk_subVOC_emissions.R VOC01 --nosave --no-restore
Current time : Mon Apr 20 11:32:22 PDT 2020 
```
**Cause:** The variable `VOC_name` is an empy character array.

* The file produced by the chunking routine is also incorrect in many aspects:
  * Filename : `NMVOC--em-speciated-VOC-anthro_input4MIPs_emissions_CMIP_CEDS-2020-04-20-supplemental-data_gn_195001-199912.nc`
  * Global attributes
    * `title = "Annual Anthropogenic Emissions of NMVOC  prepared for input4MIPs"`
    * `variable_id = "NMVOC__em_speciated_VOC_anthro"`
  
* The line:
  ```
  title <- paste( 'Annual Anthropogenic Emissions of', VOC_em, VOC_name, 'prepared for input4MIPs' )
  ```
  produces `NMVOC__em_speciated_VOC_anthro`. The doulbe `_` indicates the value of `VOC_Name` is non-existent. 

* `print(VOC_name)` produces `character(0)`
* `print(typeof(VOC_name))` produces `[1] "character"`
