#!/bin/bash
# Example a quite fully capable CLiMAF script, regarding
# the share of work between CliMAF driver and a script:
# 
# Applies a cdo OPERATOR without arg to a number of list of FILES, 
# (each of the last arguments is a list of files, each list 
# composed of a series of files which together cover the period)
#
# Script selects a variable VAR and a PERIOD in the files 
# If ALTVAR is not empty, read it instead of VAR, but give name 
# VAR to the output variable (a kind of aliasing)
# If OFFSET and SCALE are not empty, applies scaling and offset
#
# Puts results in OUT (assumed to be a string have the right number of filenames in it)
# Exit with non-0 status if any problem
# PERIOD and/or VAR can be empty, in which case filtering will not occur
# OPERATOR can be empty, in which case processing will not occur

# Lack of variable VAR in some file(s) is not considered an error
# Having no data for the PERIOD is not considered an error

set -x 
operator=$1 ;shift
outs=$1 ; shift
var=$1 ; shift
altvar=$1 ; shift 
offset=$1 ; shift ; 
scale=$1 ; shift ; 
period=$1 ; shift
#filesList=$*

tmp=~/tmp/$(basename $0)
mkdir -p $tmp
i=0
for out in $outs ; do 
    i=$((i+1))
    eval files=\$$i
    vfiles=""
    for file in $files ; do
	# TBD : schema plus robuste de noms de fichier tmp
	tmp2=$tmp/$(basename $file)
	if [ "$period" ] ; then 
	    [ "$var" ] && selvar="-selname,$var" 
	    [ "$altvar" ] && selvar="-selname,$altvar" 
	    cdo seldate,$period $selvar $file $tmp2  && vfiles+=" "$tmp2
	else
	    if [ "$var" ] ; then 
		if [ "$altvar" ] ; then 
		    cdo selname,$altvar $file $tmp2 && vfiles+=" "$tmp2
		else
		    cdo selname,$var $file $tmp2 && vfiles+=" "$tmp2
		fi
	    else vfiles+=" "$file ; fi
	fi
    done
    if [ "$vfiles" ] ; then 
	tmp3=$tmp/$(basename $0).nc
        # In next line, should avoid single file copy followed by rm ...
	cdo copy $vfiles $tmp3 && [ "$var" -o "$period" ] && rm $vfiles 
	if [ "$scale" ] || [ "$offset" ] ; then 
	    tmp4=$tmp/$(basename $0)2.nc
	    [ ! $scale ] && scale=1.
	    [ ! $offset ] && offset=0.
	    cdo mulc,$scale -addc,$offset $tmp3 $tmp4 && rm $tmp3
	    tmpn=$tmp4
	else
	    tmpn=$tmp3
	fi
	if [ "$operator" ] ; then 
	    if cdo $operator $tmpn $out ;then 
		rm $tmpn 
	        # Fix some issues : CDO does not discard degenerated dimensions
		if [ $operator == fldavg  -o $operator == fldmean ] ; then 
		    ncwa -O -a lat,lon $out $tmp3  && ncks -O -x -v lat,lon $tmp3 $out && rm $tmp3 
		elif [ $operator == timavg ] ; then 
		    ncwa -O -a time $out $tmp3 && ncks -O -x -v time $tmp3 $out && rm $tmp3 
		fi
	    fi
	else mv $tmpn $out ; fi
    fi
    [ "$var" ] && [ "$altvar" ] && [ "$var"!="$altvar" ] && ncrename -v $var,$altvar $out 
done
