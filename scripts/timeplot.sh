#!/bin/bash
doc="""
Usage $(basename $0) IN OUT VAR FORMAT ARGS 

Assuming only one variable in Netcdf file IN and, assuming it is a one-dimensional value, 
plots it in file OUT according to FORMAT, using Xmgrace.
If FORMAT = screen, plots on screen using ncview and also plots PNG format

Should be improved by reading data description in CRS metadata
"""
set -x
in=$1
out=$2
var=$3
title=${4:--}
xmgrace -netcdf $in -netcdfxy time "$var" -hardcopy -hdevice PNG -printfile $out 
#exit 0
