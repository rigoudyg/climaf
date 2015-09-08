#!/bin/bash

# Applies cdftransport operator of cdftools (which computes the transports accross a section) 
# to IN, on a optional section defined by IMIN, IMAX, JMIN, JMAX
# with possible options OPT1 and OPT2
# Output fields are OUT and OUT_VAR

set -x

in_x=$1 ; shift
in_u=$1 ; shift
in_v=$1 ; shift
imin=$1 ; shift 
imax=$1 ; shift 
jmin=$1 ; shift 
jmax=$1 ; shift
opt1=$1 ; shift
opt2=$1 ; shift
out=$1 ; shift
out_htrp=$1 ; shift
out_strp=$1 ; shift

tmp_file=$(mktemp /tmp/tmp_file.XXXXXX)

(echo climaf; echo ${imin},${imax},${jmin},${jmax}; echo EOF) | cdftransport ${opt1} ${in_x} ${in_u} ${in_v} ${opt2}

cdo selname,vtrp climaf_transports.nc ${out}
cdo selname,htrp climaf_transports.nc ${out_htrp}
cdo selname,strp climaf_transports.nc ${out_strp}

rm -f climaf_transports.nc $tmp_file section_trp.dat htrp.txt vtrp.txt strp.txt
