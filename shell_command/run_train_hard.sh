#!/bin/bash
#SBATCH --account=guest
#SBATCH --partition=guest-gpu
#SBATCH --qos=low-gpu
#SBATCH --time=24:00:00
#SBATCH --job-name=train-hard
#SBATCH --mail-user=zli@brandeis.edu
#SBATCH --output=shell_command/output/%j.txt
#SBATCH --nodes=1
#SBATCH --gres=gpu:TitanXP:3

python3 train_hard.py