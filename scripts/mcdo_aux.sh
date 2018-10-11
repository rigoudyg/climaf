#These are auxilliary functions for script mcdo.sh

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

