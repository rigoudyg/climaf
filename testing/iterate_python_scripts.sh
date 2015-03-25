#!/bin/bash
# Wrapper for script : iterate_python_scripts.p
thisdir=$(cd $(dirname $0); pwd)
dir=$(dirname $thisdir)
export PYTHONPATH=$dir:$PYTHONPATH
cd $dir/examples
python $thisdir/iterate_python_scripts.py $*
