#!/bin/bash

set -x

in_1=$1 ; shift
in_2=$1 ; shift
in_3=$1 ; shift
in_4=$1 ; shift 
in_5=$1 ; shift
in_6=$1 ; shift 
imin=$1 ; shift 
imax=$1 ; shift 
jmin=$1 ; shift 
jmax=$1 ; shift
opt1=$1 ; shift
opt2=$1 ; shift
out=$1 ; shift

tmp_file=$(mktemp /tmp/tmp_file.XXXXXX)

cdo merge ${in_1} ${in_2} ${in_3} ${in_4} $tmp_file

(echo climaf; echo ${imin},${imax},${jmin},${jmax}; echo EOF) | cdftransport ${opt1} $tmp_file ${in_5} ${in_6} ${opt2}

cdo selname,vtrp climaf_transports.nc ${out}
cdo selname,htrp climaf_transports.nc htrp.nc
cdo selname,strp climaf_transports.nc strp.nc

rm -f climaf_transports.nc $tmp_file section_trp.dat htrp.txt vtrp.txt strp.txt

