#!/bin/bash
# Wrapper for script : iterate_python_scripts.py

thisdir=$(cd $(dirname $0); pwd)
dir=$(dirname $thisdir)
export PYTHONPATH=$dir:$PYTHONPATH

# Testing a series of examples
################################

cd $dir/examples

# List of scripts that can be tested anywhere (based on data installed with the package)
scripts="clean_cache.py data_generic.py plotmap.py basic_oce.py latlonbox.py ann_cycle.py derived.py \
         export.py increm.py regrid.py latlonbox.py"

# Add some scripts, depending on the data available at each site
if [[ $(uname -n) == lx* || $(uname -n) == sx* ]]; then 
    # CNRM
    scripts=$scripts" data_cmip5drs.py "
    # Add scripts depending on user-configured data
    [ $(whoami) = senesi ] && scripts=$scripts" data_em.py"
elif [[ $(uname -n) == ciclad* ]]; then 
    # Ciclad
    scripts=$scripts" data_cmip5drs.py "
fi

# Cleaning script
scripts=$scripts" clean_cache.py"

echo "tested example scripts : "$scripts 
export CLIMAF_LOG_LEVEL=critical
python $thisdir/iterate_python_scripts.py -V -f $scripts
