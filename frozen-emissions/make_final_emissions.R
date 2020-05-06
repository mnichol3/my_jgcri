# This script calculates the final emissions for each of the emission species
# defined in 'em_list' using the CEDS S1.1.write_summary_data.R file
#
# Author: Matt Nicholson
# 12 Dec 19

em_list <- c( "BC", "CH4", "CO", "CO2", "NH3", "NMVOC", "NOx", "OC", "SO2" )
# em_list <- c( "NMVOC" )

# Set the working directory to the main CEDS directory to make life easier
setwd("C:/Users/nich980/code/CEDS")

# Path of the CEDS script we're going to call, relative to the main CEDS directory
F_PATH <- "code/module-S/S1.1.write_summary_data.R"

# Path to the CEDS intermediate output directory
INTER_DIR <- "intermediate-output"

for (em in em_list) {
  # Name of the emission file we want
  em_fname <- paste0(em, "_total_CEDS_emissions.csv")

  system(paste("Rscript", F_PATH, em, "--nosave --no-restore", sep=" "))
}


