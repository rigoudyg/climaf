#!/bin/bash
# Applies a cdo OPERATOR without arg to a number of list of FILES, 
# selecting a variable VAR and a PERIOD and a REGION in the files
#
# Puts results in OUT (assumed to be a string have the right number of filenames in it)
# Exit with non-0 status if any problem
# PERIOD and/or VAR and/or REGION can be empty, in which case filtering will not occur
# OPERATOR can be empty, in which case processing will not occur

# Lack of variable VAR in some file(s) is not considered an error
# Having no data for the PERIOD is not considered an error

set -x 
operator=$1 ; shift
outs=$1 ; shift
var=$1 ; shift
period=$1 ; shift
region=$1 ; shift
alias=$1 ; shift

tmp=~/tmp/$(basename $0)
mkdir -p $tmp

# Prepare CDO operator strings

[ "$var" ] && selvar="-selname,$var" 
[ "$period" ] && seldate="-seldate,$period"
if [ "$region" ] ; then 
    latmin=$(echo $region | cut -d "," -f 1)
    latmax=$(echo $region | cut -d "," -f 2)
    lonmin=$(echo $region | cut -d "," -f 3)
    lonmax=$(echo $region | cut -d "," -f 4)
    selregion="-sellonlatbox,$lonmin,$lonmax,$latmin,$latmax"
fi
if [ "$alias" ] ; then 
    IFS=", " read var filevar scale offset <<< $alias 
    selalias=-expr,"$var=${filevar}*${scale}+${offset};"
fi
i=0
# Loop on the list of list of files 
for out in $outs ; do 
    i=$((i+1))

    # 'files' is the next list of filenames (listed in a single string)
    eval files=\$$i
    vfiles=""

    # Make all selections (aliasing, time, space, variable) before applying the operator
    for file in $files ; do
	tmp2=$tmp/$(basename $file) ; rm -f $tmp2
	if [ $alias ] ; then 
	    cdo ${selalias#-} ${selvar} $selregion $seldate $file $tmp2  && [ -f $tmp2 ] && vfiles+=" "$tmp2 
	else
	    if [ "$period" ] ; then 
		cdo ${selvar#-} $selregion $seldate $file $tmp2  && [ -f $tmp2 ] && vfiles+=" "$tmp2 
	    else
		if [ "$var" ] ; then 
		    cdo ${selvar#-} $selregion $file $tmp2 && [ -f $tmp2 ] && vfiles+=" "$tmp2
		else 
		    if [ "$region" ] ; then 
			cdo ${selregion#-} $file $tmp2 && [ -f $tmp2 ] && vfiles+=" "$tmp2
		    else
			vfiles+=" "$file ; 
		    fi
		fi
	    fi
	fi
    done

    # Then, assemble all datafiles in a single one before applying the operator 
    # (because it may be non-linear in time - e.g. eigenvectors )
    if [ "$vfiles" ] ; then 
	tmp3=$tmp/$(basename $0).nc ; rm -f $tmp3
        # let us avoid single file copy followed by rm ...
	if [ $(echo $vfiles | wc -w) -gt 1 ] ; then 
	    cdo copy $vfiles $tmp3 && [ "$var" -o "$period" -o "$region" ] && rm $vfiles 
	else
	    mv $vfiles $tmp3
	fi

	# Apply operator if requested, plus some house keeping on coordinates
	if [ "$operator" ] ; then 
	    if cdo $operator $tmp3 $out ;then 
		rm $tmp3 
	        # Fix some issues : CDO does not discard degenerated dimensions
		#if [ $operator == fldavg  -o $operator == fldmean ] ; then 
		#    ncwa -O -a lat,lon $out $tmp3  && ncks -O -x -v lat,lon $tmp3 $out && rm $tmp3 
		#elif [ $operator == timavg ] ; then 
		#    ncwa -O -a time $out $tmp3 && ncks -O -x -v time $tmp3 $out && rm $tmp3 
		#fi
	    fi
	else mv $tmp3 $out ; fi
	#ls -al $out
    else
	echo "Issue while selecting data from $files ">&2
	exit 1
    fi
done
