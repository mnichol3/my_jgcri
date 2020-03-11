### Run all Hector RCP scenarios
#
# Usage
# -----
# From the root Hector directory:
# source("/mnt/c/Users/nich980/code/my_jgcri/hector/scripts/run_rcp_all.R")

library(hector)

parse_outpath <- function() {
  # Determine the path of the output dir based on the operating system
  if(.Platform$OS.type == "unix") {
    prefix <- "/mnt/c"
  } else {
    prefix <- "C:"
  }
  outpath <- file.path(prefix, "Users", "nich980", "code",
                       "hector-worktrees", "release_v2.3.0", "output")
}


run_scenario <- function(rcp, outpath) {
  f_in <- paste0("input/hector_rcp", rcp, ".ini")
  ini_file <- system.file("input/hector_rcp45.ini", package="hector")

  #core <- newcore(ini_file, loglevel=0, suppresslogging=FALSE)
  core <- newcore(ini_file, name=paste0("rcp_", rcp))
  run(core)

  vars <- c(ATMOSPHERIC_CH4(), ATMOSPHERIC_CO2(), ATMOSPHERIC_N2O(),
            DETRITUS_C(), VEG_C(), SOIL_C(), ATMOSPHERIC_C(),
            RF_TOTAL(), RF_CO2(), RF_N2O(), RF_BC(), RF_OC(), RF_SO2(), RF_CH4(),
            GLOBAL_TEMP()
            )

  rslt <- fetchvars(core, 1745:2400, vars)

  f_out <- paste0("output_rcp", rcp, "_v2.3.0.csv")
  outpath <- file.path(outpath, f_out)

  write.csv(rslt, outpath, row.names=FALSE)
  message( paste0( "Output written to ", outpath ) )
}

outpath <- parse_outpath()
rcps = c("26", "45", "60", "85")

lapply(rcps, run_scenario, outpath=outpath)
