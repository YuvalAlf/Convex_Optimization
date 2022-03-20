#!/bin/bash

#SBATCH --job-name=yuval_sos_poly
#SBATCH --mail-user=yuvalalfassi@gmail.com
#SBATCH --array=0-9

module load Python/3.7.4-GCCcore-8.3.0
module load CMake/3.20.1-GCCcore-10.3.0

python3 -m venv ../venv
source ../venv/bin/activate
pip3 install --upgrade pip
pip3 install cmake
pip3 install cvxpy

python3 ../gen_poly_basis.py $(($i)) ../results < input_worst_approximation.txt
