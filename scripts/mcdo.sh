#!/bin/bash
# Applies a cdo OPERATOR without arg to a number of list of FILES, 
# selecting a variable VAR and a PERIOD in the files
#
# Puts results in OUT (assumed to be a string have the right number of filenames in it)
# Exit with non-0 status if any problem
# PERIOD and/or VAR can be empty, in which case filtering will not occur
# OPERATOR can be empty, in which case processing will not occur

# Lack of variable VAR in some file(s) is not considered an error
# Having no data for the PERIOD is not considered an error

set -x 
operator=$1
outs=$2
var=$3
period=$4
region=$5
shift;shift; shift ;shift; shift
#filesList=$*

tmp=~/tmp/$(basename $0)
mkdir -p $tmp
i=0
if [ "$region" ] ; then 
    latmin=$(echo $region | cut -d "," -f 1)
    latmax=$(echo $region | cut -d "," -f 2)
    lonmin=$(echo $region | cut -d "," -f 3)
    lonmax=$(echo $region | cut -d "," -f 4)
    selregion="-sellonlatbox,$lonmin,$lonmax,$latmin,$latmax"
fi
for out in $outs ; do 
    i=$((i+1))
    eval files=\$$i
    vfiles=""
    for file in $files ; do
	tmp2=$tmp/$(basename $file)
	if [ "$period" ] ; then 
	    [ "$var" ] && selvar="-selname,$var" 
	    cdo seldate,${period/-/,} $selvar $selregion $file $tmp2  && vfiles+=" "$tmp2
	else
	    if [ "$var" ] ; then 
		cdo selname,$var $selregion $file $tmp2 && vfiles+=" "$tmp2
	    else 
		if [ "$region" ] ; then 
		    cdo $selregion $file $tmp2 && vfiles+=" "$tmp2
		else
		    vfiles+=" "$file ; 
		fi
	    fi
	fi
    done
    if [ "$vfiles" ] ; then 
	tmp3=$tmp/$(basename $0).nc
        # let us avoid single file copy followed by rm ...
	if [ $(echo $vfiles | wc -w) -gt 1 ] ; then 
	    cdo copy $vfiles $tmp3 && [ "$var" -o "$period" -o "$region" ] && rm $vfiles 
	else
	    mv $vfiles $tmp3
	fi
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
done
