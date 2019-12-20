# Changes made to Hector

Document to track changes made to fork of JGCRI/hector

Last updated: 19 Dec 2019

## fetchvars_all

This branch was created to address [JGCRI #330](https://github.com/JGCRI/hector/issues/330) and introduces the function `fetchvars_all` and three helper functions: `cum_vars_input`, `cum_vars_params`, `cum_vars_output`. These functions are held in `./R/messages.R`.

#### Actions
  * Merged into `origin/master` on 19 Dec 19
  * Pull request to `JGCRI/master` made on 19 Dec 19

<br/>

## fix/ocean_component-timeSeries

This branch was created in order to address [JGCRI #328](https://github.com/JGCRI/hector/issues/328), and aims to add time series capability to atmopsphere & ocean components

#### Actions


#### Specifics

  * ocean_component.cpp
    * Modify the assertion at the beginning of `OceanComponent::getData` to check that the date parameter is appropriate for the given varNAme
    * Ocean Carbon (`D_OCEAN_C` & `D_Carbon_*`)
      * Return value is constructed by summing carbon values from time series objects for deep ocean, intermediate ocean, surface high latitude, & surface low latitude timeseries data structures
      * **TODO** get return val from oceanbox time vector, similar to `D_PH_*`
    * All other variables
      * Return value is obtained by retrieving the `oceanbox` corresponding to the `date` param from the corresponding `oceanbox timevector` and querying its attributes. This negates the need to add a separate, variable-specific time series data structure to the component
        
          Ex: 
          ```
          [in] varName = D_PH_LL  // pH for low-latitude surface ocean
        
          oceanbox temp_obox = surfaceLL_tv.get( date );
          returnval = temp_obox.mychemistry.pH;
          ```
          
