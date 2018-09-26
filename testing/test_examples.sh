#!/bin/bash
# Wrapper for script : iterate_python_scripts.py

thisdir=$(cd $(dirname $0); pwd)
dir=$(dirname $thisdir)
export PYTHONPATH=$dir:$PYTHONPATH

# Testing a series of examples
################################

#cd $dir/examples

# List of scripts that can be tested anywhere (based on data installed with the package, or a test is done)
scripts="index_html.py data_generic.py plotmap.py basic_oce.py latlonbox.py \
         ann_cycle.py derived.py export.py increm.py regrid.py  macro.py \
         plot_timeseries.py plot_xsection.py figarray.py data_file.py gplot.py hovm.py"

# Add some scripts, depending on the data available at each site
if [[ $(uname -n) == lx* || $(uname -n) == sx* ]]; then 
    # CNRM
    scripts=$scripts" data_cmip5drs.py data_cmip6drs.py ensemble.py data_obs.py cdftools.py cdftools_multivar.py cdftransport.py"
    # Add scripts depending on user-configured data
    #[ $(whoami) = senesi ] && scripts=$scripts" data_em.py seaice.py"
elif [[ $(uname -n) == ciclad* ]]; then 
    # Ciclad
    scripts=$scripts" data_cmip5drs.py ensemble.py"
fi

# Cleaning script
scripts="clean_cache.py  "$scripts" clean_cache.py"

echo "tested example scripts : "$scripts 
export CLIMAF_LOG_LEVEL=critical
#export CLIMAF_LOG_LEVEL=debug

scripts2=""
for i in $scripts
do 
    scripts2=$scripts2"$dir/examples/$i " 
done

python $thisdir/iterate_python_scripts.py -V -f $scripts2
#for s in $scripts ; do cdat $s ; done

