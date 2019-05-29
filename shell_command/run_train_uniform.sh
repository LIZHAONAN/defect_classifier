#!/bin/bash
#SBATCH --account=pengyu-lab
#SBATCH --partition=pengyu-gpu
#SBATCH --qos=medium
#SBATCH --time=00:10:00
#SBATCH --job-name=train-uniform
#SBATCH --mail-user=zli@brandeis.edu
#SBATCH --output=shell_command/output/%j.txt
#SBATCH --nodes=3

python3 train_uniform.py