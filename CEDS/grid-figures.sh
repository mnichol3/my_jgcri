#!/bin/bash
#SBATCH -A ceds
#SBATCH -t 2:00:00
#SBATCH -N 1
#SBATCH -p shared
#SBATCH -n 1
#SBATCH --mail-user <matthew.nicholson@pnnl.gov>
#SBATCH --mail-type END

#Set up your environment you wish to run in with module commands.
module purge
module load R/3.3.3

#Actually codes starts here
now=$(date)
echo "Current time : $now"

cd /pic/projects/GCAM/mnichol/ceds/CEDS_Data
Rscript generate_all.R

now=$(date)
echo "Current time : $now"