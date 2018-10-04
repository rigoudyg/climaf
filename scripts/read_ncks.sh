#!/bin/bash

# Use ncks to read a series of files possibly remote ones through
# OpenDAP selecting a variable VAR and a PERIOD and a REGION in the
# files
#
# Puts results in file OUT 
# Exit with non-0 status if any problem
# PERIOD and/or VAR and/or REGION can be empty, in which case filtering will not occur
# ALIAS, LISIING, UNITS  .....


set -x 
out=$1 ; shift
var=$1 ; shift
period=$1 ; shift
region=$1 ; shift
alias=$1 ; shift
units=$1 ; shift
vm=$1 ; shift

tmp=$(mktemp -d --tmpdir climaf_mcdo_XXXXXX) # Will use TMPDIR if set, else /tmp


# Prepare NCO selector strings

[ "$var" ] && selvar="-v $var" 
[ "$period" ] && seldate="-d time,$period"
if [ "$region" ] ; then 
    latmin=$(echo $region | cut -d "," -f 1)
    latmax=$(echo $region | cut -d "," -f 2)
    lonmin=$(echo $region | cut -d "," -f 3)
    lonmax=$(echo $region | cut -d "," -f 4)
    selregion="-d lon,$lonmin,$lonmax -d lat,$latmin,$latmax"
fi

# Prepare CDO operator strings
if [ "$alias" ] ; then 
    IFS=", " read var filevar scale offset <<< $alias 
    selalias=-expr,"$var=${filevar}*${scale}+${offset};"
fi
if [ "$vm" ] ; then 
    setmiss="-setctomiss,$vm"
fi
# For the time being, must use NetCDF3 file format chained CDO
# operations because NetCDF4 is not threadsafe at CNRM
CDO="cdo -f nc"

# 'files' is the list of input filenames
files=$1
vfiles=""

# First read space-time-var domain using ncks 
for file in $files ; do
    tmp2=$tmp/$(basename $file) ; rm -f $tmp2
    ncks ${selvar#-} $selregion $seldate $file $tmp2  && \
	[ -f $tmp2 ] && vfiles+=" "$tmp2 
done


if [ $setmiss ] ; then 
    $CDO ${setmiss#-} $selalias $file $tmp2  && [ -f $tmp2 ] && vfiles+=" "$tmp2 
else
    if [ $alias ] ; then 
	$CDO ${selalias#-} $file $tmp2  && [ -f $tmp2 ] && vfiles+=" "$tmp2 
    else
	

# Then, assemble all datafiles in a single one 
if [ "$vfiles" ] ; then 
    tmp3=$tmp/$(basename $0).nc ; rm -f $tmp3
    # let us avoid single file copy followed by rm ...
    if [ $(echo $vfiles | wc -w) -gt 1 ] ; then 
	cdo copy $vfiles $tmp3 && [ "$var" -o "$period" -o "$region" ] && \
	    rm $vfiles 
    else mv $vfiles $tmp3 ; fi
    # Change units before applying further operations, if applicable
    if [ "$units" ] ; then ncatted -O -a units,$var,o,c,"$units" $tmp3 ; fi
    
    # Apply operator if requested
    if [ "$operator" ] ; then 
	cdo $operator $tmp3 $out && rm $tmp3 || exit 1
    else mv $tmp3 $out ; fi
else
    echo "Issue while selecting data from $files ">&2
    rm -fr $tmp
    exit 1
fi

rm -fr $tmp
