#!/bin/bash
#SBATCH -A ceds
#SBATCH -t 2:00:00
#SBATCH -N 1
#SBATCH -p shared
#SBATCH -n 1
#SBATCH --mail-user <matthew.nicholson@pnnl.gov>
#SBATCH --mail-type END

module purge
module load R/3.3.3
module load python/3.6.7

now=$(date)
echo "Current time : $now"

echo "Executing reorder_lons.py"

python reorder_lons.py

echo "Executing generate_all.R"
cd /pic/projects/GCAM/mnichol/ceds/CEDS_Data
Rscript generate_all.R

now=$(date)
echo "Current time : $now"