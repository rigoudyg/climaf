"""
Management of CliMAF standard operators

"""
import os

from climaf import __path__ as cpath
from climaf.operators import cscript, fixed_fields
from climaf.clogging import clogger
from climaf.site_settings import onCiclad

scriptpath=cpath[0]+"/../scripts/" 
binpath=cpath[0]+"/../bin/" 

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
            scriptpath+'mcdo.sh "${operator}" "${out}" "${var}" "${period_iso}" "${domain}" "${alias}" "${units}" "${missing}" ${ins}')
    #
    cscript('ccdo2','cdo ${operator} ${in_1} ${in_2} ${out}')
    #
    cscript('ccdo_ens','cdo ${operator} ${mmin} ${out}')
    #
    cscript('minus', 'cdo sub ${in_1} ${in_2} ${out}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #
    cscript('plus', 'cdo add ${in_1} ${in_2} ${out}',
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
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=False)
    #
    cscript('regridn' ,
            scriptpath+'regrid.sh ${in} ${cdogrid} ${out} ${option}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=False)
    #
    cscript('regridll',scriptpath+'regridll.sh ${in} ${out} ${cdogrid} '
            '${latmin} ${latmax} ${lonmin} ${lonmax} ${remap_option}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=False)
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
    # plot: main field (main_file) + auxiliary field (aux_file, optional) + vectors (u_file & v_file, optionals)
    #
    cscript('plot'  , '(ncl -Q '+ scriptpath +'gplot.ncl main_file=\'\"${in}\"\' aux_file=\'\"${in_2}\"\' '
            'u_file=\'\"${in_3}\"\' v_file=\'\"${in_4}\"\' rotation=${rotation} '
            'plotname=\'\"${out}\"\' colormap=\'\"${color}\"\' vmin=${min} vmax=${max} vdelta=${delta} '
            'main_var=\'\"${var}\"\' aux_var=\'\"${var_2}\"\' u_var=\'\"${var_3}\"\' v_var=\'\"${var_4}\"\' '
            'title=\'\"${title}\"\' myscale=${scale} myoffset=${offset} mpCenterLonF=${mpCenterLonF} '
            'vcRefMagnitudeF=${vcRefMagnitudeF} vcRefLengthF=${vcRefLengthF} vcMinDistanceF=${vcMinDistanceF} '
            'vcGlyphStyle=\'\"${vcGlyphStyle}\"\' vcLineArrowColor=\'\"${vcLineArrowColor}\"\' '
            'units=\'\"${units}\"\' y=\'\"${y}\"\' colors=\'\"${colors}\"\' level=${level} time=${time} '
            'proj=\'\"${proj}\"\' contours=\'\"${contours}\"\' focus=\'\"${focus}\"\' '
            'type=\'\"${format}\"\' resolution=\'\"${resolution}\"\' trim=${trim} fmt=\'\"${fmt}\"\' '
            'vcb=${vcb} lbLabelFontHeightF=${lbLabelFontHeightF} invXY=${invXY} reverse=${reverse} '
            'tmYLLabelFontHeightF=${tmYLLabelFontHeightF} tmXBLabelFontHeightF=${tmXBLabelFontHeightF} '
            'tmYRLabelFontHeightF=${tmYRLabelFontHeightF} tiXAxisFontHeightF=${tiXAxisFontHeightF} '
            'tiYAxisFontHeightF=${tiYAxisFontHeightF} gsnPolarLabelFontHeightF=${gsnPolarLabelFontHeightF} '
            'tiMainFont=\'\"${tiMainFont}\"\' tiMainFontHeightF=${tiMainFontHeightF} '
            'tiMainPosition=\'\"${tiMainPosition}\"\' gsnLeftString=\'\"${gsnLeftString}\"\' '
            'gsnRightString=\'\"${gsnRightString}\"\' gsnCenterString=\'\"${gsnCenterString}\"\' '
            'gsnStringFont=\'\"${gsnStringFont}\"\' gsnStringFontHeightF=${gsnStringFontHeightF} '
            'shade_below=${shade_below} shade_above=${shade_above} options=\'\"${options}\"\' '
            'aux_options=\'\"${aux_options}\"\' shading_options=\'\"${shading_options}\"\' '
            'myscale_aux=${scale_aux} myoffset_aux=${offset_aux} )', format="graph")
    # 
    cscript('curves'     , '(ncl -Q '+ scriptpath +'curves.ncl infile=\'\"${mmin}\"\' '
            'plotname=\'\"${out}\"\' var=\'\"${var}\"\' title=\'\"${title}\"\' '
            'y=\'\"${y}\"\' labels=\'\"${labels}\"\' colors=\'\"${colors}\"\' units=\'\"${units}\"\' '
            'X_axis=\'\"${X_axis}\"\' fmt=\'\"${fmt}\"\' options=\'\"${options}\"\' aux_options=\'\"${aux_options}\"\' '
            'lgcols=${lgcols} myscale=${scale} myoffset=${offset} type=\'\"${format}\"\' '
            'resolution=\'\"${resolution}\"\' trim=${trim} invXY=${invXY} vmin=${min} vmax=${max} '
            'myscale_aux=${scale_aux} myoffset_aux=${offset_aux} )', format="graph")
    #
    # cpdfcrop : pdfcrop by preserving metadata
    #
    cscript('cpdfcrop'     , binpath + 'pdfcrop ${in} ${out} ', format="pdf")
    #
    # cepscrop : crop 'eps' file using epstopdf, pdfcrop and pdftops
    #
    if (os.system("type exiv2 >/dev/null 2>&1") == 0) :
        cscript('cepscrop'     , 'epstopdf ${in} --outfile=tmpfile.pdf;' + binpath + 'pdfcrop tmpfile.pdf tmpfile-crop.pdf; pdftops -eps tmpfile-crop.pdf ${out}; rm -f tmpfile.pdf tmpfile-crop.pdf ', format="eps")
    #    
    cscript('ncdump'     , 'ncdump -h ${in} ', format="txt")
    #
    cscript('slice',"ncks -O -F -v ${var} -d ${dim},${min},${max} ${in} tmp.nc ; ncwa -O -a ${dim} tmp.nc ${out} ; rm -f tmp.nc")
    #
    cscript("mask","cdo setctomiss,${miss} ${in} ${out}")
    #
    cscript("ncpdq","ncpdq ${arg} ${in} ${out}")
    #
    # timesection : to plot hovmoller diagrams
    #
    cscript('timesection', 'ncl '+scriptpath+'timesection.ncl infile=\'\"${in}\"\' plotname=\'\"${out}\"\' '
            ' var=\'\"${var}\"\' latS=\'\"${latS}\"\' latN=\'\"${latN}\"\' lonW=\'\"${lonW}\"\' lonE=\'\"${lonE}\"\' '
            ' cmap=\'\"${color}\"\' myscale=${scale} myoffset=${offset} units=\'\"${units}\"\' reverse=${reverse} '
            ' axmean=\'\"${axmean}\"\' xpoint=${xpoint} ypoint=${ypoint} zpoint=${zpoint} '
            ' type=\'\"${format}\"\' resolution=\'\"${resolution}\"\' trim=${trim} options=\'\"${options}\"\' ',format="graph")
    #
    if onCiclad:
        cscript("ml2pl", scriptpath+"ml2pl.sh -p ${var_2} -v ${var_1} ${in_1} ${out} ${in_2}",
                commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
        fixed_fields("ml2pl",("press_levels.txt",scriptpath+"press_levels.txt"))
    #   
    if (os.system("type cdfmean >/dev/null 2>&1")== 0 ) :
        load_cdftools_operators()
    else :
        clogger.warning("Binary cdftools not found. Some operators won't work")

    

def load_cdftools_operators():
    #
    # CDFTools operators 
    #
    # cdfmean
    #
    cscript('ccdfmean',
            'cdfmean ${in} ${var} ${pos_grid} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} ${opt}; ncks -O -x -v mean_${var} cdfmean.nc ${out}; rm -f cdfmean.nc cdfmean.txt', _var="mean_3D%s", canSelectVar=True)    
    #    
    cscript('ccdfmean_profile',
            'cdfmean ${in} ${var} ${pos_grid} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} ${opt}; ncks -O -x -v mean_3D${var} cdfmean.nc ${out}; rm -f cdfmean.nc cdfmean.txt', _var="mean_%s", canSelectVar=True)
    #    
    cscript('ccdfvar',
            'cdfmean ${in} ${var} ${pos_grid} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} -var ${opt}; ncks -O -x -v mean_${var},mean_3D${var},var_${var} cdfmean.nc ${out}; rm -f cdfmean.nc cdfmean.txt cdfvar.txt', _var="var_3D%s", canSelectVar=True)
    #    
    cscript('ccdfvar_profile',
            'cdfmean ${in} ${var} ${pos_grid} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} -var ${opt}; ncks -O -x -v mean_${var},mean_3D${var},var_3D${var} cdfmean.nc ${out}; rm -f cdfmean.nc cdfmean.txt cdfvar.txt', _var="var_%s", canSelectVar=True)
    
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
            'echo ""; cdfheatc ${in} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} ${opt}; mv cdfheatc.nc ${out}; rm -f cdfheatc.nc', _var="heatc_2D,heatc_3D", canSelectVar=True)
    #
    cscript('ccdfheatcm',
            'echo ""; tmp_file=`echo $(mktemp /tmp/tmp_file.XXXXXX)`; cdo merge ${in_1} ${in_2} $tmp_file; cdfheatc $tmp_file ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} ${opt}; mv cdfheatc.nc ${out}; rm -f cdfheatc.nc $tmp_file', _var="heatc_2D,heatc_3D", canSelectVar=True)
    
    #
    # cdfsaltc 
    #
    cscript('ccdfsaltc',
            'echo ""; cdfsaltc ${in} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} ${opt}; mv cdfsaltc.nc ${out}; rm -f cdfsaltc.nc', _var="saltc_2D,saltc_3D", canSelectVar=True)
    
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
    # cdfzonalmean
    #
    cscript('ccdfzonalmean',
            'cdfzonalmean ${in} ${point_type} -var ${var} ${opt}; varname=${var}; ncrename -v zo${varname:2}_glo,zo${var}_glo zonalmean.nc ${out}; rm -f zonalmean.nc', _var="zo%s_glo", canSelectVar=True)
    #
    # cdfzonalmean_bas
    #
    cscript('ccdfzonalmean_bas',
            'cdfzonalmean ${in} ${point_type} new_maskglo.nc -var ${var} ${opt}; varname=${var}; ncks -O -v zo${varname:2}_${basin} zonalmean.nc tmpfile.nc; ncrename -v zo${varname:2}_${basin},zo${var}_${basin} tmpfile.nc ${out}; rm -f tmpfile.nc zonalmean.nc', _var="zo%s_${basin}", canSelectVar=True)
    
