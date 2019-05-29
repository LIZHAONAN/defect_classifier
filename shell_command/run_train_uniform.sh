#!/bin/bash
#SBATCH --account=pengyu-lab
#SBATCH --partition=pengyu-gpu
#SBATCH --time=00:10:00
#SBATCH --job-name=train-uniform
#SBATCH --mail-user=zli@brandeis.edu
#SBATCH --output=shell_command/output/%j.txt
#SBATCH --node=2

python3 train_uniform.py