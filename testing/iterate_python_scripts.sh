#!/bin/bash
# Wrapper for script : iterate_python_scripts.py
thisdir=$(cd $(dirname $0); pwd)
dir=$(dirname $thisdir)
export PYTHONPATH=$dir:$PYTHONPATH
cd $dir/examples
if [[ $(uname -n) == lx* || $(uname -n) == sx* ]]; then 
    scripts="plotmap.py basic_oce.py latlonbox.py ann_cycle.py derived.py \
         export.py increm.py regrid.py obscami.py cmip5drs.py obs4mips.py"
    scripts="plotmap.py              latlonbox.py ann_cycle.py derived.py \
         export.py increm.py regrid.py obscami.py cmip5drs.py obs4mips.py"
    scripts="                                                             \
                             regrid.py obscami.py cmip5drs.py obs4mips.py"
else
    scripts="plotmap.py basic_oce.py latlonbox.py ann_cycle.py derived.py \
         export.py increm.py regrid.py obscami.py cmip5drs.py ocmip_ciclad.py"
fi
python $thisdir/iterate_python_scripts.py -v -f $scripts
