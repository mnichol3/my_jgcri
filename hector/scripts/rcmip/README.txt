This directory holds scripts to reproduce the hector-rcmip Tier 1 analysis using the hector-rcmip package
* https://github.com/ashiklom/hector-rcmip
* https://github.com/mnichol3/hector-rcmip

- run-sims.sh
  * This script runs the Hector simulations for the various RCMIP scenarios ("scripts/01-run-simulations.R"). IT DOES NOT run the post-processing script. 

- run-and-process.sh
  * This script does two things: run the Hector simulations for the RCMIP scenarios ("scripts/01-run-simulations.R"), then runs the post-processing script ("scripts/02-process-outputs.R").

- post-process.sh
  * This script only executes the post-processing script, and will fail if the output produced by the "scripts/01-run-simulations.R" script is not in place. 