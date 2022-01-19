#!/bin/bash

# Run an ESMValTool python diagnostic script, after setting the relavant
# environment

# This script must be tuned both to the platform and to the ESMValTool install

# Here, platform is Ciclad and ESMValTool install is an intermediate one
# And we assume that command 'conda' is available

diag=${1/.py/}.py
settings=$2

module load modtools-python3

# Init conda
base=$(conda info | grep -i 'base environment' | awk '{print $4}')
source $base/etc/profile.d/conda.sh

# Init ESMValTool with conda just for the sake of initing some environment
# variables such as NCARG_ROOT for Ncl
CENV=/net/nfs/tools/Users/SU/jservon/mambaforge/envs/esmvaltool_2.4
conda activate $CENV

# Using python from ESMValTool env is necessary for accessing ESMValTool modules,
# and is not automatic after 'conda activate', when launched by a python's
# subprocess with shell=False
python=$CENV/bin/python3

$python $CENV/lib/python3.9/site-packages/Esmvaltool/diag_scripts/$diag $settings

