#!/bin/bash
# 
Usage=" wcdo.sh OPERATOR 'FILES' VAR PERIOD OUT"
#
# Applies a cdo OPERATOR without arg to a list of FILES, 
# possibly selecting a variable VAR and a PERIOD in the files
#
# Puts results in file OUT 
# Exit with non-0 status if any problem
# PERIOD and/or VAR can be empty, in which case filtering will not occur
# OPERATOR can be empty, in which case processing will not occur

# Lack of variable VAR in some file(s) is not considered an error
# Having no data for the PERIOD is not considered an error

set -x 
operator=$1
files=$2
var=$3
period=$4
out=$5

tmp=~/tmp/$(basename $0)
mkdir -p $tmp
i=0
vfiles=""
for file in $files ; do
    tmp2=$tmp/$(basename $file)
    if [ "$period" ] ; then 
	if [ "$var" ] ; then selvar="-selname,$var" ; fi
	cdo seldate,$period $selvar $file $tmp2  && vfiles+=" "$tmp2
    else
	if [ "$var" ] ; then 
	    cdo selname,$var $file $tmp2 && vfiles+=" "$tmp2
	else vfiles+=" "$file ; fi
    fi
done
if [ "$vfiles" ] ; then 
    tmp3=$tmp/$(basename $0).nc
    # In next line, should avoid single file copy followed by rm ...
    cdo copy $vfiles $tmp3 && [ "$var" -o "$period" ] && rm $vfiles 
    if [ "$operator" ] ; then 
	if cdo $operator $tmp3 $out ;then 
	    rm $tmp3 
	    # Fix some issues : CDO does not discard degenerated dimensions
	    if [ $operator == fldavg  -o $operator == fldmean ] ; then 
		ncwa -O -a lat,lon $out $tmp3  && ncks -O -x -v lat,lon $tmp3 $out && rm $tmp3 
	    elif [ $operator == timavg ] ; then 
		ncwa -O -a time $out $tmp3 && ncks -O -x -v time $tmp3 $out && rm $tmp3 
	    fi
	fi
    else mv $tmp3 $out ; fi
fi
