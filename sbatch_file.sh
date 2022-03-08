#!/bin/bash

#SBATCH --job-name=yuval_sos_poly
#SBATCH --mail-user=yuvalalfassi@gmail.com
#SBATCH --mail-type=ALL
#SBATCH --cpus-per-task=20
#SBATCH --ntasks=1

module load Python/3.7.4-GCCcore-8.3.0

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

python gen_poly_basis.py < input.txt > output.txt
