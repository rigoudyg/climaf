#!/bin/bash
# Applies the timavg cdo operator to a list of FILES 
# and applies ncwa for discarding degenerated singleton time dimension
# Puts results in OUT 
# Exit with non-0 status if any problem

set -ex 
out=$1
files=$2

tmp3=$(mktemp /tmp/tmp_file.XXXXXX) 

cdo timavg $files $out
ncwa -O -a time $out $tmp3 && ncks -O -x -v time $tmp3 $out && rm $tmp3 
