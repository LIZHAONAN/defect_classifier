#!/bin/bash
#SBATCH --account=guest
#SBATCH --partition=guest-gpu
#SBATCH --qos=low-gpu
#SBATCH --time=00:10:00
#SBATCH --job-name=train-uniform
#SBATCH --mail-user=zli@brandeis.edu
#SBATCH --output=shell_command/output/%j.txt
#SBATCH --nodes=1
#SBATCH --gres=gpu:3

python3 train_uniform.py