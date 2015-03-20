#!/bin/bash
set -e
# Just a dummy test of CliMAF handling of multiple ouputs
# Applies CDO operators fldmean and fldstd to IN.
# Output fields are OUT_MEAN and OUT_VAR
set -x
in=$1
varin=$2
out_mean=$3
out_sdev=$4
#
cdo fldmean $in $out_mean.tmp
ncwa -O -a lat,lon $out_mean.tmp $out_mean 
rm $out_mean.tmp  
#
cdo fldstd  $in $out_sdev.tmp  
ncwa -O -a lat,lon $out_sdev.tmp $out_sdev 
ncrename -v $varin,"std($varin)" $out_sdev 
rm $out_sdev.tmp  
