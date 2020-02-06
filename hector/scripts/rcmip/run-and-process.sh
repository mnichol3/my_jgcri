#!/bin/bash
#SBATCH -A "BR20_NICH980"
#SBATCH -t 2:00:00
#SBATCH -N 1
#SBATCH -p shared

#SBATCH --mail-user matthew.nicholson@pnnl.gov
#SBATCH --mail-type END

module purge
module load R

now=$(date)
echo "Current time: $now"

cd /pic/projects/GCAM/mnichol/hector/hector-rcmip/hector-rcmip

Rscript scripts/01-run-simulations.R --no-save --no-restore
Rscript scripts/02-process-outputs.R --no-save --no-restore

now=$(date)
echo "Current time: $now"
