#!/bin/bash
#SBATCH --account=guest
#SBATCH --partition=guest-gpu
#SBATCH --qos=low-gpu
#SBATCH --time=24:00:00
#SBATCH --job-name=train-FNN
#SBATCH --mail-user=zli@brandeis.edu
#SBATCH --output=shell_command/output/%j.txt
#SBATCH --nodes=1
#SBATCH --gres=gpu:TitanXP:3

export CUDA_VISIBLE_DEVICE=0
python3 train_FNN.py