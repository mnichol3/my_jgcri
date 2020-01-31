### Basic Hector run, adapted from Alexy's vignette

library(hector)

# ini_file <- system.file("input/gas_paris_med.ini", package = "hector")
ini_file <- system.file("input/hector_rcp45.ini", package = "hector")

core <- newcore(ini_file, name="Billy", loglevel = 0, suppresslogging = F)
# core <- newcore(ini_file, name="Billy")

run(core)

vars <- c(ATMOSPHERIC_CH4(), ATMOSPHERIC_CO2(), ATMOSPHERIC_N2O())

# rslts <- fetchvars(core, 1745:2300, vars)
rslt <- fetchvars_all(core, 2100:2150)

# write.csv(rslts, outpath, row.names = FALSE)
# message( paste0( "Output written to ", outpath ) )
