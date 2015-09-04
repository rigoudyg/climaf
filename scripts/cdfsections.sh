#!/bin/bash

# Applies cdfsections operator of cdftools (which computes temperature, salinity, 
# sig0, sig1, sig2, sig4, Uorth, Utang along a section made of Nsec linear segments)
# to IN with a list of arguments LARF, LORF, NSEC, LAT1, LON1, LAT2, LON2, N1
# and other optional arguments MORE_POINTS
# Output fields are OUT and OUT_VAR

set -x

in_1=$1 ; shift
in_2=$1 ; shift
in_3=$1 ; shift
in_4=$1 ; shift 
in_5=$1 ; shift
larf=$1 ; shift 
lorf=$1 ; shift 
Nsec=$1 ; shift 
lat1=$1 ; shift
lon1=$1 ; shift
lat2=$1 ; shift
lon2=$1 ; shift
n1=$1 ; shift
more_points=$1 ; shift
out=$1 ; shift
out_Utang=$1 ; shift
out_so=$1 ; shift
out_thetao=$1 ; shift
out_sig0=$1 ; shift
out_sig1=$1 ; shift
out_sig2=$1 ; shift
out_sig4=$1 ; shift

tmp_file=$(mktemp /tmp/tmp_file.XXXXXX)

cdo merge ${in_1} ${in_2} ${in_3} $tmp_file

cdfsections ${in_4} ${in_5} $tmp_file ${larf} ${lorf} ${Nsec} ${lat1} ${lon1} ${lat2} ${lon2} ${n1} ${more_points}

cdo selname,Uorth section.nc ${out}
cdo selname,Utang section.nc ${out_Utang}
cdo selname,vosaline section.nc ${out_so}
cdo selname,votemper section.nc ${out_thetao}
cdo selname,sig0 section.nc ${out_sig0}
cdo selname,sig1 section.nc ${out_sig1}
cdo selname,sig2 section.nc ${out_sig2}
cdo selname,sig4 section.nc ${out_sig4}

rm -f section.nc $tmp_file
