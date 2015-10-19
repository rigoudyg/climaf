"""
Management of CliMAF standard operators

"""
import os

from climaf import __path__ as cpath
from climaf.operators import cscript
from climaf.clogging import clogger

scriptpath=cpath[0]+"/../scripts/" 

def load_standard_operators():
    """ 
    Load CliMAF standard operators. Invoked by standard CliMAF setup

    The operators list also show in variable 'cscripts'
    They are documented elsewhere
    """
    #
    # Compute scripts
    #
    
    cscript('select' ,scriptpath+'mcdo.sh "${operator}" "${out}" "${var}" "${period_iso}" "${domain}" "${alias}" "${units}" "${missing}" ${ins} ',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #
    cscript('ccdo',
            scriptpath+'mcdo.sh ${operator} "${out}" "${var}" "${period_iso}" "${domain}" "${alias}" "${units}" "${missing}" ${ins}')
    #
    cscript('minus', 'cdo sub ${in_1} ${in_2} ${out}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #
    cscript('space_average',
            scriptpath+'mcdo.sh fldmean "${out}" "${var}" "${period_iso}" "${domain}" "${alias}" "${units}" "${missing}" ${ins}', 
            commuteWithTimeConcatenation=True)
    #
    cscript('time_average' ,
            scriptpath+'mcdo.sh timmean  "${out}" "${var}" "${period_iso}" "${domain}" "${alias}" "${units}" "${missing}" ${ins}' ,
            commuteWithSpaceConcatenation=True)
    #
    cscript('llbox' ,
            scriptpath+'mcdo.sh ""  "${out}" "${var}" "${period_iso}" "${latmin},${latmax},${lonmin},${lonmax}" "${alias}" "${units}" "${missing}" ${ins}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #
    cscript('regrid' ,
            scriptpath+'regrid.sh ${in} ${in_2} ${out} ${option}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #
    cscript('regridn' ,
            scriptpath+'regrid.sh ${in} ${cdogrid} ${out} ${option}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #
    cscript('rescale' ,
            'cdo expr,\"${var}=${scale}*${var}+${offset};\" ${in} ${out}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #
    cscript('mean_and_std',
            scriptpath+'mean_and_std.sh ${in} ${var} ${out} ${out_sdev}', 
            # This tells CliMAF how to compute varname for name output 'sdev' 
	    # using input varname
            sdev_var="std(%s)" , 
            commuteWithTimeConcatenation=True)
    #
    # Declare plot scripts
    cscript('ncview'    ,'ncview ${in} 1>/dev/null 2>&1&' )
    #
    cscript('timeplot', 'ncl '+scriptpath+'timeplot.ncl infile=\'\"${in}\"\' outfile=\'\"${out}\"\' '
            'var=\'\"${var}\"\' title=\'\"${title}\"\'',format="png")
    #
    # plot: main field (main_file) + auxiliary field (aux_file, optional) + vectors (u_file & v_file, optionals)
    #
    cscript('plot'  , '(ncl -Q '+ scriptpath +'gplot.ncl main_file=\'\"${in}\"\' aux_file=\'\"${in_2}\"\' '
            'u_file=\'\"${in_3}\"\' v_file=\'\"${in_4}\"\' rotation=${rotation} '
            'plotname=\'\"${out}\"\' cmap=\'\"${color}\"\' vmin=${min} vmax=${max} vdelta=${delta} '
            'main_var=\'\"${var}\"\' aux_var=\'\"${var_2}\"\' u_var=\'\"${var_3}\"\' v_var=\'\"${var_4}\"\' '
            'title=\'\"${title}\"\' scale=${scale} offset=${offset} mpCenterLonF=${mpCenterLonF} '
            'vcRefMagnitudeF=${vcRefMagnitudeF} vcRefLengthF=${vcRefLengthF} vcMinDistanceF=${vcMinDistanceF} '
            'vcGlyphStyle=\'\"${vcGlyphStyle}\"\' vcLineArrowColor=\'\"${vcLineArrowColor}\"\' '
            'units=\'\"${units}\"\' linp=${linp} levels=\'\"${levels}\"\' '
            'proj=\'\"${proj}\"\' contours=\'\"${contours}\"\' focus=\'\"${focus}\"\' && '
            'convert ${out} -trim ${out}) ', format="png")    
    #
    cscript('lines'     , '(ncl -Q '+ scriptpath +'lineplot.ncl infile=\'\"${mmin}\"\' '
            'plotname=\'\"${out}\"\' var=\'\"${var}\"\' title=\'\"${title}\"\' '
            'linp=${linp} labels=\'\"${labels}\"\'  colors=\'\"${colors}\"\'  thickness=${thickness}'
            'T_axis=\'\"${T_axis}\"\' fmt=\'\"${fmt}\"\'  && '
            'convert ${out} -trim ${out}) ', format="png")
    #


    if (os.system("type cdfmean >/dev/null 2>&1")== 0 ) :
        load_cdftools_operators()
    else :
        clogger.warning("No Cdftool available")

    

def load_cdftools_operators():
    #
    # CDFTools operators 
    #
    # cdfmean
    #
    cscript('ccdfmean',
            'cdfmean ${in} ${var} ${pos_grid} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} ${opt}; ncks -O -x -v mean_${var} cdfmean.nc ${out}; rm -f cdfmean.nc cdfmean.txt', _var="mean_3D%s")    
    #
    cscript('ccdfmean_profile',
            'cdfmean ${in} ${var} ${pos_grid} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} ${opt}; ncks -O -x -v mean_3D${var} cdfmean.nc ${out}; rm -f cdfmean.nc cdfmean.txt', _var="mean_%s")
    #    
    cscript('ccdfvar',
            'cdfmean ${in} ${var} ${pos_grid} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} -var ${opt}; ncks -O -x -v mean_${var},mean_3D${var},var_${var} cdfmean.nc ${out}; rm -f cdfmean.nc cdfmean.txt cdfvar.txt', _var="var_3D%s")
    #    
    cscript('ccdfvar_profile',
            'cdfmean ${in} ${var} ${pos_grid} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} -var ${opt}; ncks -O -x -v mean_${var},mean_3D${var},var_3D${var} cdfmean.nc ${out}; rm -f cdfmean.nc cdfmean.txt cdfvar.txt', _var="var_%s")
    
    #
    # cdftransport : case where VT file must be given 
    #
    #cscript('ccdftransport',
    #        scriptpath+'cdftransport.sh ${in_1} ${in_2} ${in_3} ${in_4} ${in_5} ${in_6} "${imin}" "${imax}" "${jmin}" "${jmax}" "${opt1}" "${opt2}" ${out} ${out_htrp} ${out_strp}',
     #       canSelectVar=True)
    
    cscript('ccdftransport',
            scriptpath+'cdftransp.sh ${in_1} ${in_2} ${in_3} "${imin}" "${imax}" "${jmin}" "${jmax}" "${opt1}" "${opt2}" ${out} ${out_htrp} ${out_strp}',
            _var='vtrp', htrp_var='htrp', strp_var='strp', canSelectVar=True)  
    #
    # cdfheatc 
    #
    cscript('ccdfheatc',
            'echo ""; cdfheatc ${in} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} ${opt}', _var="heatc", canSelectVar=True)
    #
    cscript('ccdfheatcm',
            'echo ""; tmp_file=`echo $(mktemp /tmp/tmp_file.XXXXXX)`; cdo merge ${in_1} ${in_2} $tmp_file; cdfheatc $tmp_file ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} ${opt}; rm -f $tmp_file', _var="heatc", canSelectVar=True)
    # 
    # cdfsections 
    #
    cscript('ccdfsections',
            scriptpath+'cdfsections.sh ${in_1} ${in_2} ${in_3} ${larf} ${lorf} ${Nsec} ${lat1} ${lon1} ${lat2} ${lon2} ${n1} "${more_points}" ${out} ${out_Utang} ${out_so} ${out_thetao} ${out_sig0} ${out_sig1} ${out_sig2} ${out_sig4}',  _var="Uorth", Utang_var="Utang", so_var="so", thetao_var="thetao", sig0_var="sig0", sig1_var="sig1", sig2_var="sig2", sig4_var="sig4", canSelectVar=True) 
    #
    cscript('ccdfsectionsm',
            scriptpath+'cdfsectionsm.sh ${in_1} ${in_2} ${in_3} ${in_4} ${in_5} ${larf} ${lorf} ${Nsec} ${lat1} ${lon1} ${lat2} ${lon2} ${n1} "${more_points}" ${out} ${out_Utang} ${out_so} ${out_thetao} ${out_sig0} ${out_sig1} ${out_sig2} ${out_sig4}', _var="Uorth", Utang_var="Utang", so_var="so", thetao_var="thetao", sig0_var="sig0", sig1_var="sig1", sig2_var="sig2", sig4_var="sig4", canSelectVar=True)
    #
    # cdfmxlheatc
    #
    cscript('ccdfmxlheatc',
            'echo ""; cdfmxlheatc ${in} ${opt}; mv mxlheatc.nc ${out}; rm -f mxlheatc.nc', _var="somxlheatc", canSelectVar=True)
    #
    cscript('ccdfmxlheatcm',
            'echo ""; tmp_file=`echo $(mktemp /tmp/tmp_file.XXXXXX)`; cdo merge ${in_1} ${in_2} $tmp_file; cdfmxlheatc $tmp_file ${opt}; mv mxlheatc.nc ${out}; rm -f mxlheatc.nc $tmp_file', _var="somxlheatc", canSelectVar=True) 
    #
    # cdfstd
    #
    cscript('ccdfstd',
            'cdfstd ${opt} ${ins}; mv cdfstd.nc ${out}; rm -f cdfstd.nc', _var="%s_std", canSelectVar=True)
    #
    cscript('ccdfstdmoy',
            'cdfstd -save ${opt} ${ins}; mv cdfstd.nc ${out}; mv cdfmoy.nc ${out_moy}; rm -f cdfstd.nc cdfmoy.nc', _var="%s_std", moy_var="%s", canSelectVar=True) 
    
    #
    # cdfvT ; a bit tricky about naming the output
    #
    cscript('ccdfvT', 'cdfvT ${in_1} ${in_2} ${in_3} ${in_4} -o ${out}', _var="vomevt,vomevs,vozout,vozous", canSelectVar=True)
    #

