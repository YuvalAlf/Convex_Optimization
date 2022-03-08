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

git clone https://github.com/DrTimothyAldenDavis/SuiteSparse.git
pushd SuiteSparse
git checkout v5.6.0
popd
export CVXOPT_SUITESPARSE_SRC_DIR=$(pwd)/SuiteSparse
git clone https://github.com/cvxopt/cvxopt.git
cd cvxopt
git checkout `git describe --abbrev=0 --tags`
export CVXOPT_BUILD_DSDP=1    # optional
export CVXOPT_BUILD_FFTW=1    # optional
export CVXOPT_BUILD_GLPK=1    # optional
export CVXOPT_BUILD_GSL=1     # optional
python setup.py install

pip install -r requirements.txt

python gen_poly_basis.py < input.txt > output.txt
