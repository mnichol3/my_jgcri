#### 3 Jan 2020

# Re-Gridding CEDS Historical Openburning Data for Gridding

The grid plotting routines in `CEDS_Data` expect gridded emissions file grids to have 0.5 degree resolution (720 Lon x 360 Lat). However, input4MIPS gridded openburning files obtained from Vrije Universiteit Amsterdam (VUA) has 0.25 degree grid resolution (1440 Lon x 720 Lat). Simple work-arounds to try to force the plotting routines to accept 0.25 degree grids causes errors elsewhere in the preprocessing code. Hence, the most viable option is to re-aggregate the 0.25 degree gridded data on to a 0.5 degree grid.

## Regridding 
