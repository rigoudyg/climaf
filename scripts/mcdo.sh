#!/bin/bash
# Applies a cdo OPERATOR without arg to a list of FILES, 
# selecting a variable VAR and a PERIOD and a REGION in the files
#
# Puts results in file OUT 
# Exit with non-0 status if any problem
# PERIOD and/or VAR and/or REGION can be empty, in which case filtering will not occur
# OPERATOR can be empty, in which case processing will not occur
# ALIAS, LISIING, UNITS  .....

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

tmp=$(mktemp -d --tmpdir climaf_mcdo_XXXXXX) # Will use TMPDIR if set, else /tmp

# For the time being, must use NetCDF3 file format chained CDO
# operations because NetCDF4 is not threadsafe at CNRM
CDO="cdo -f nc"

# Prepare CDO operator strings

timefix ()
{
    # Check if the time axis for a data file should be fixed, based solely on its name, 
    # and hence echoes the relevant CDO syntax (to be inserted in a CDO pipe) for fixing it
    file=$1
    # Case for IPSL Seasonal cycle files, such as 
    # .../SIMULATIONS/p86mart/IGCM_OUT/IPSLCM6/DEVT/piControl/O1T04V04/ICE/Analyse/SE/O1T04V04_SE_1850_1859_1M_icemod.nc 
    if [[ $file =~ IGCM_OUT.*SE/.*_SE_.*([0-9]{4})_[0-9]{4}_1M.*nc ]] ; then 
	echo -settaxis,${BASH_REMATCH[1]}-01-16:12:00:00,1mon
    fi
}

[ "$period" ] && seldatebase="-seldate,$period"

[ "$var" ] && selvar="-selname,$var" 

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
if [ "$vm" ] ; then 
    setmiss="-setctomiss,$vm"
fi

# 'files' is the list of input filenames
files=$1
vfiles=""

# Make all selections (setmiss, aliasing, time, space, variable) 
# before applying the operator
for file in $files ; do
    tmp2=$tmp/$(basename $file) ; rm -f $tmp2
    # If needed, transform date selection command in (time fix + date selection)
    seldate=$seldatebase
    [ "$seldate" ] && seldate=$seldatebase" "$(timefix $file) 
    #
    if [ $setmiss ] ; then 
	$CDO ${setmiss#-} $selalias $selregion $seldate ${selvar} \
	    $file $tmp2  && [ -f $tmp2 ] && vfiles+=" "$tmp2 
    else
	if [ $alias ] ; then 
	    $CDO ${selalias#-} $selregion $seldate ${selvar} \
		$file $tmp2  && [ -f $tmp2 ] && vfiles+=" "$tmp2 
	else
	    if [ "$region" ] ; then 
		$CDO ${selregion#-} $seldate $selvar $file $tmp2  && \
		    [ -f $tmp2 ] && vfiles+=" "$tmp2 
	    else
		if [ $period ] ; then 
		    $CDO ${seldate#-} ${selvar} $file $tmp2 && [ -f $tmp2 ] \
			&& vfiles+=" "$tmp2
		else 
		    if [ "$var" ] ; then 
			$CDO ${selvar#-} $file $tmp2 && \
			    [ -f $tmp2 ] && vfiles+=" "$tmp2
		    else
			vfiles+=" "$file ; 
		    fi
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
	cdo copy $vfiles $tmp3 && [ "$var" -o "$period" -o "$region" ] && \
	    rm $vfiles 
    else mv $vfiles $tmp3 ; fi
    # Chagne units before applying further operations, if applicable
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
