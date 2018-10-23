#!/bin/bash
# Applies a cdo OPERATOR without arg to a list of FILES, 
# selecting a variable VAR and a PERIOD and a REGION in the files
#
# Puts results in file OUT 
# Exit with non-0 status if any problem
# PERIOD and/or VAR and/or REGION can be empty, in which case filtering will not occur
# OPERATOR can be empty, in which case processing will not occur
# ALIAS, UNITS  .....

# Lack of variable VAR in some file(s) is not considered an error
# Having no data for the PERIOD is not considered an error

set -x 
operator=$1 ; shift
out=$1 ; shift
var=$1 ; shift
period=$1 ; shift
region=$1 ; shift
alias=$1 ; shift
units=$1 ; shift
vm=$1 ; shift

tmp=$(mktemp -d -t climaf_mcdo_XXXXXX) # Will use TMPDIR if set, else /tmp
# Option -t/--tmpdir is not available at all sites -> test result
[ $? -ne 0 ] && tmp=$(mktemp -d  climaf_mcdo_XXXXXX) 

# Load functions  clim_timefix, nemo_timefix, aladin_coordfix from auxilliary file
aux=$0 ; aux=${aux/.sh/_aux.sh}
. $aux

# For the time being, at most sites, must use NetCDF3 file format chained CDO
# operations because NetCDF4 is not threadsafe there
if [[ $(uname -n ) == ciclad* ]] ; then CDO="cdo -O " ; else CDO="cdo -O -f nc" ; fi

# Prepare CDO operator strings

[ "$period" ] && seldatebase="-seldate,"$period

[ "$var" ] && selvar="-selname,"$var

if [ "$region" ] ; then 
    latmin=$(echo $region | cut -d "," -f 1)
    latmax=$(echo $region | cut -d "," -f 2)
    lonmin=$(echo $region | cut -d "," -f 3)
    lonmax=$(echo $region | cut -d "," -f 4)
    selregion="-sellonlatbox,$lonmin,$lonmax,$latmin,$latmax"
fi

if [ "$units" ] ; then
    setunits="-setattribute,"${var}"@units="${units}
fi

if [ "$alias" ] ; then 
    IFS=", " read var filevar scale offset <<< $alias 
    selalias="-expr,"$var=${filevar}*${scale}+${offset}";"
else
    filevar=$var
fi

if [ "$vm" ] ; then 
    setmiss="-setctomiss,"$vm
fi


# 'files' is the list of input filenames
files=$*
single_file=no ; [ $(echo $files | wc -w) -eq 1 ] && single_file=yes
vfiles=""
vfiles_are_original=0

# Make all selections (setmiss, aliasing, time, space, variable) 
# before applying the operator
# however, operator si also applied here if there is only one file

for file in $files ; do
    tmp2=$tmp/$(basename $file) ; rm -f $tmp2
    # If needed, transform date selection command in (time fix + date selection)
    seldate=$seldatebase
    [ "$seldate" ] && seldate=$seldatebase" "$(clim_timefix $file) 
    #
    # If requested, fix time_counter for Nemo outputs. Feature not yet tested !!
    [ "${CLIMAF_FIX_NEMO_TIME:-no}" != no ] && file=$(nemo_timefix $file) 
    # If requested, fix attribute 'coordinates' of file variable for Aladin outputs.
    [ "${CLIMAF_FIX_ALADIN_COORD:-no}" != no ] && file=$(aladin_coordfix $file)
    #
    # Construct CDO operators chain as needed, optimizing operations list and order
    if [[ $file == *${filevar}_* ]] ; then 
	# varname is in filename -> assume seldate before selvar is best
	ops=$setmiss" "$setunits" "$selalias" "$selvar" "$seldate" "$selregion
    else
	# varname is not in filename -> assume selvar before selvar is best
	ops=$setmiss" "$setunits" "$selalias" "$seldate" "$selvar" "$selregion
    fi
    #
    if [ "${ops// /}" ] ; then
	# There is some operator to apply
	[ $single_file = yes ] && [ $operator ] && ops="-"${operator}" "$ops 
	$CDO $ops $file $tmp2 && [ -f $tmp2 ] && vfiles+=" "$tmp2
    else
	# Just keep the file as is
	vfiles+=" "$file ; vfiles_are_original=1
    fi
done


if [ "$vfiles" ] ; then
    if [ $single_file = yes ] ; then
	file=$vfiles
	# Operator was applied upstream (if one is defined )
	if [ $vfiles_are_original -eq 1 ]; then cp $file $out ; else mv $file $out ; fi
    else
	tmp3=$tmp/$(basename $0).nc ; rm -f $tmp3
	#
	if [ ${timelinear:-no} == no ] ; then 
	    # Must assemble all datafiles in a single one before applying 
	    # the operator if it is non-linear in time - e.g. eigenvectors 
            # (but avoid single file copy followed by rm ...)
	    if [ $(echo $vfiles | wc -w) -gt 1 ] ; then 
		cdo copy $vfiles $tmp3 && [ $vfiles_are_original -eq 0 ] && rm $vfiles 
	    else  # Only one file to process
		file=$vfiles
		if [ $vfiles_are_original -eq 1 ]
		then cp $file $tmp3 ; 
		else mv $file $tmp3 ; fi
	    fi
            #
            # Apply operator if requested
	    if [ "$operator" ] ; then 
		cdo $operator $tmp3 $out && rm $tmp3 || exit 1
	    else mv $tmp3 $out ; fi
	else
	    cdo $operator $vfiles $out && [ $vfiles_are_original -eq 0 ] && rm $vfiles 
	fi
    fi
else
    echo "Issue while selecting data from $files ">&2
    rm -fr $tmp
    exit 1
fi

rm -fr $tmp
