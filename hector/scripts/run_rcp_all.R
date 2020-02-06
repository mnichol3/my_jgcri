### 

library(hector)

def parse_outpath <- function() {
  # Determine the path of the output dir based on the operating system
  if(.Platform$OS.type == "unix") {
    prefix <- "/mnt/c/"
  } else {
    prefix <- "C:"
  }
  outpath <- file.path(prefix, "Users", "nich980", "hector-worktrees", "release_v2.3.0", "output")
}


run_scenario <- function(rcp) {
  f_in <- paste0("input/hector_rcp", rcp, ".ini")
  ini_file <- system.file("input/hector_rcp45.ini", package = "hector")

  #core <- newcore(ini_file, loglevel = 0, suppresslogging = F)
  core <- newcore(ini_file)
  run(core)
  
  vars <- c(ATMOSPHERIC_CH4(), ATMOSPHERIC_CO2(), ATMOSPHERIC_N2O(),
            DETRITUS_C(), VEG_C(), SOIL_C(),
            RF_TOTAL(), RF_CO2(),
            GLOBAL_TEMP(), OCEAN_SURFACE_TEMP()
            )
            
  rslt <- fetchvars(core, 1745:2400, vars)
  
  f_out <- paste0("output_rcp", rcp, ".csv")
  outpath <- file.path(outpath, f_out)
  
  write.csv(rslts, outpath, row.names = FALSE)
  message( paste0( "Output written to ", outpath ) )
}

outpath <- parse_outpath()
rcps = c("26", "45", "60", "85")
lapply(rcps, run_scenario, arg1=outpath)