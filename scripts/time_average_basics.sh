#!/bin/bash
# Applies the timavg cdo operator to a list of FILES 
# Puts results in OUT 
# Exit with non-0 status if any problem

set -ex 
out=$1
files=$2
cdo timavg $files $out

