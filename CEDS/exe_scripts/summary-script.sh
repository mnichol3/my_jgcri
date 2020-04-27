#!/bin/bash
#SBATCH -A ceds
#SBATCH -t 01:00:00
#SBATCH -N 1
#SBATCH -p shared
#SBATCH -n 1
#SBATCH --mail-user matthew.nicholson@pnnl.gov
#SBATCH --mail-type END

#Set up your environment you wish to run in with module commands.
module purge
module load R/3.5.1

now=$(date)
echo "Current time : $now"

cd /pic/projects/GCAM/mnichol/ceds/CEDS-dev 
Rscript code/module-S/S1.2.aggregate_summary_data.R

now=$(date)
echo "Current time : $now"

