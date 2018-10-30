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

[ "$units" ] && setunits="-setattribute,"${var}"@units="${units} 

if [ "$alias" ] ; then 
    IFS=", " read var filevar scale offset <<< $alias 
    selalias="-expr,"$var=${filevar}*${scale}+${offset}";"
else
    filevar=$var
fi

[ "$vm" ] && setmiss="-setctomiss,"$vm 

# 'files' is the list of input filenames
files=$*

# prepare to invoke CDO operator 'mergetime' if needed
merge="" ; [ $(echo $files | wc -w) -gt 1 ] && merge="-mergetime"

# If needed, transform date selection command in (time fix + date selection)
ffile=$(echo $files | cut -d " " -f 1)
seldate=$seldatebase
[ "$seldate" ] && seldate=$seldatebase" "$(clim_timefix $ffile) 

# Prepare all selections (setmiss, aliasing, time, space, variable) :
# construct CDO operators chain, optimizing operations list and order
if [[ $ffile == *${filevar}_* ]] ; then 
    # varname is in filename -> assume seldate before selvar is best
    ops=$setmiss" "$setunits" "$selalias" "$selvar" "$seldate" "$selregion" "$merge
else
    # varname is not in filename -> assume selvar before selvar is best
    ops=$setmiss" "$setunits" "$selalias" "$seldate" "$selvar" "$selregion" "$merge
fi
[ $operator ] && ops="-"${operator}" "$ops 
#

# Construct files list, which may involve transformed files
vfiles=""
for file in $files ; do
    # If requested, fix time_counter for Nemo outputs. Feature not yet tested !!
    [ "${CLIMAF_FIX_NEMO_TIME:-no}" != no ] && file=$(nemo_timefix $file) 
    # If requested, fix attribute 'coordinates' of file variable for Aladin outputs.
    [ "${CLIMAF_FIX_ALADIN_COORD:-no}" != no ] && file=$(aladin_coordfix $file)
    #
    vfiles+=" "$file
done

time $CDO $ops "$vfiles" $out

rm -fr $tmp
