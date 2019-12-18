### Basic Hector run, adapted from Alexy's vignette

library(hector)
# library(ggplot2)

ini_file <- system.file("input/gas_paris_med.ini", package = "hector")
# ini_file <- system.file("input/hector_rcp45.ini", package = "hector")

# core <- newcore(ini_file, loglevel=0, suppresslogging=F, name="Billy")
core <- newcore(ini_file, name="Billy")

run(core)

results <- fetchvars(core, 1745:2300, vars=hector::PH_HL())
