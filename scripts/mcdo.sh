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


clim_timefix ()
{
    # Check if the time axis for a data file should be fixed, based solely on its name, 
    # and hence echoes the relevant CDO syntax (to be inserted in a CDO pipe) for fixing it
    file=$1
    # Case for IPSL Seasonal cycle files, such as 
    # ... IGCM_OUT/IPSLCM6/DEVT/piControl/O1T04V04/ICE/Analyse/SE/O1T04V04_SE_1850_1859_1M_icemod.nc 
    if [[ $file =~ IGCM_OUT.*SE/.*_SE_.*([0-9]{4})_[0-9]{4}_1M.*nc ]] ; then 
	echo -settaxis,${BASH_REMATCH[1]}-01-16:12:00:00,1mon
    fi
}

nemo_timefix ()
{
    # Rename alternate time_counter variables to 'time_counter' for some kind 
    # of Nemo outputs  (Nemo 3.2 had a bug when using IOIPSL ...)
    # Echoes the name of a file with renamed variable (be it a modified file or a copy)
    # Creates an alternate file in $tmp if no write permission and renaming is actually useful
    file=$1
    out=""
    if [[ $file =~ .*1[md].*grid_T_table2.2.nc ]] ; then 
	if ncdump -h $file  | \grep -E -q '(coord.*t_ave_01month|t_ave_00086400 )' ; then 
	    var2rename=""
	    if [[ $file =~ .*1m.*grid_T_table2.2.nc ]] ; then 
		var2rename=t_ave_01month 
		vars2d="pbo sos tos tossq zos zoss zossq zosto"
		vars3d="rhopoto so thetao thkcello rhopoto"
	    fi
	    if [[ $file =~ .*1d.*grid_T_table2.2.nc ]] ; then 
		var2rename=t_ave_00086400 
		vars2d="tos tossq" ; vars3d=""
	    fi
	    if [ "$var2rename" ] ; then 
		out=$tmp/renamed_$(basename $file) ; rm -f $out 
		if [[ $(ncdump -k $file) == 'classic' ]] ; then
		    temp=$file
		else
		    temp=$out
		    ncks -3 $file $temp 
		fi
		ncrename -d .$var2rename,time_counter -v .$var2rename,time_counter $temp $out >&2
		for lvar in $vars2d; do 
#		    ncatted -a coordinates,$lvar,m,c,'time_counter nav_lat nav_lon' $out >&2
		    ncatted -a coordinates,$lvar,m,c,'nav_lat nav_lon' $out >&2
		done
		for lvar in $vars3d; do 
#		    ncatted -a coordinates,$lvar,m,c,'time_counter deptht nav_lat nav_lon' $out >&2
		    ncatted -a coordinates,$lvar,m,c,'deptht nav_lat nav_lon' $out >&2
		done
		if [ -w $file ] ; then mv -f $out $file ; out="" ; fi
	    fi
	fi
    fi
    if [ $out ]; then echo $out ; else echo $file ; fi 
}

aladin_coordfix ()
{
    # Rename attribute 'coordinates' of file variable $filevar to 'latitude longitude'
    # for some kind of ALADIN outputs which have 'lat lon' (or 'lon lat') for attribute 'coordinates'
    # of file variable (particularly for outputs created with post-treatment tool called 'postald') 
    # Echoes the name of a file with renamed variable attribute (be it a modified file or a copy)
    # Creates an alternate file in $tmp if no write permission and renaming is actually useful
    file=$1
    out=""

    if [[ $file =~ .*ALADIN.*.nc && ( ! $file =~ .*r1i1p1.*.nc || ! $file =~ .*MED-11.*.nc ) ]] ; then 

	if ncdump -h $file | \grep -E -q '(coord.*lon lat|coord.*lat lon)' \
	    && ncdump -h $file | \grep -E -q '(float longitude|float latitude)' ; then 

	    out=$tmp/renamed_$(basename $file) ; rm -f $out 
	    ncks -3 $file $out 
	    ncatted -a coordinates,$filevar,o,c,'latitude longitude' $out >&2 
	    if [ -w $file ] ; then mv -f $out $file ; out="" ; fi

	fi
    fi
    if [ $out ]; then echo $out ; else echo $file ; fi 
}


# For the time being, at most sites, must use NetCDF3 file format chained CDO
# operations because NetCDF4 is not threadsafe there
if [[ $(uname -n ) == ciclad* ]] ; then CDO="cdo -O " ; else CDO="cdo -O -f nc" ; fi

# Prepare CDO operator strings

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
else
    filevar=$var
fi

if [ "$vm" ] ; then 
    setmiss="-setctomiss,$vm"
fi

# 'files' is the list of input filenames
files=$*
vfiles=""
vfiles_are_original=0

# Make all selections (setmiss, aliasing, time, space, variable) 
# before applying the operator
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
    if [ $setmiss ] ; then 
	$CDO ${setmiss#-} $selalias $selregion $seldate ${selvar} \
	    $file $tmp2  && [ -f $tmp2 ] && vfiles+=" "$tmp2 
    else
	if [ $alias -a $selalias ] ; then 
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
			vfiles_are_original=1
		    fi
		fi
	    fi
	fi
    fi
done


if [ "$vfiles" ] ; then 
    tmp3=$tmp/$(basename $0).nc ; rm -f $tmp3
    #
    # Then, assemble all datafiles in a single one before applying the operator 
    # if it is non-linear in time - e.g. eigenvectors 
    if [ ${timelinear:-no} == no ] ; then 
        # avoid single file copy followed by rm ...
	if [ $(echo $vfiles | wc -w) -gt 1 ] ; then 
	    cdo copy $vfiles $tmp3 && [ $vfiles_are_original -eq 0 ] && rm $vfiles 
	else  # Only one file to process
	    if [ $vfiles_are_original -eq 1 ]
	    then cp $vfiles $tmp3 ; 
	    else mv $vfiles $tmp3 ; fi
	fi
        #
        # Change units before applying further operations, if applicable
	if [ "$units" ] ; then ncatted -O -a units,$var,o,c,"$units" $tmp3 ; fi
	#
        # Apply operator if requested
	if [ "$operator" ] ; then 
	    cdo $operator $tmp3 $out && rm $tmp3 || exit 1
	else mv $tmp3 $out ; fi
    else
	cdo $operator $vfiles $out
	if [ "$units" ] ; then ncatted -O -a units,$var,o,c,"$units" $out ; fi
    fi
else
    echo "Issue while selecting data from $files ">&2
    rm -fr $tmp
    exit 1
fi

rm -fr $tmp
