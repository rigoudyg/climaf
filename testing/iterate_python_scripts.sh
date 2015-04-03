#!/bin/bash
# Wrapper for script : iterate_python_scripts.py

thisdir=$(cd $(dirname $0); pwd)
dir=$(dirname $thisdir)
export PYTHONPATH=$dir:$PYTHONPATH
cd $dir/examples

# List of scripts that can be tested anywhere (based on data installed with the package)
scripts="plotmap.py basic_oce.py latlonbox.py ann_cycle.py derived.py \
         export.py increm.py regrid.py cmip5drs.py"

# Add some scripts, depending on the data available at each site
if [[ $(uname -n) == lx* || $(uname -n) == sx* ]]; then 
    # CNRM
    scripts=$scripts" obscami.py obs4mips.py"
    # Add scripts depending on user-configured data
    [ $(whoami) = senesi ] && scripts=$scripts" em_data.py"
elif [[ $(uname -n) == ciclad* ]]; then 
    # Ciclad
    scripts=$scripts" ocmip_ciclad.py"
fi

# Cleaning script
scripts=$scripts" clean_cache.py"

echo "tested scripts : "$scripts
python $thisdir/iterate_python_scripts.py -v -f $scripts
