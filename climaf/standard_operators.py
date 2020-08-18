#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Management of CliMAF standard operators

"""

from __future__ import print_function, division, unicode_literals, absolute_import

import os
import subprocess

from climaf import __path__ as cpath
from climaf.operators import cscript, fixed_fields
from env.clogging import clogger
from env.site_settings import onCiclad
from env.environment import *


scriptpath = cpath[0] + "/../scripts/"
binpath = cpath[0] + "/../bin/"


def load_standard_operators():
    """
    Load CliMAF standard operators. Invoked by standard CliMAF setup

    The operators list also show in variable 'cscripts'
    They are documented elsewhere
    """
    #
    # Compute scripts
    #
    cscript('select',
            scriptpath + 'mcdo.py --operator="${operator}" --output_file="${out}" --var="${var}"'
                         ' --period="${period_iso}" --region="${domain}" --alias="${alias}" --units="${units}" '
                         '--vm="${missing}" ${ins} ',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #
    cscript('remote_select',
            scriptpath + 'mcdo_remote.py --operator="${operator}" --output_file="${out}" --var="${var}"'
                         ' --period="${period_iso}" --domain="${domain}" '
                         '--alias="${alias}" --units="${units}" --vm="${missing}" ${ins} ',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #
    cscript('ccdo',
            scriptpath + 'mcdo.py --operator="${operator}" --output_file="${out}" --var="${var}"'
                         ' --period="${period_iso}" --region="${domain}" --alias="${alias}" --units="${units}" '
                         '--vm="${missing}" ${ins}')
    #
    cscript('ccdo_fast', 'cdo ${operator} ${in} ${out}')
    cscript('ccdo2', 'cdo ${operator} ${in_1} ${in_2} ${out}')
    cscript('ccdo3', 'cdo ${operator} ${in_1} ${in_2} ${in_3} ${out}')
    #
    # Define some CliMAF operators with tricky arguments ordering in order that CliMAF 
    # do not loose track of variable name for the output of some CDO operators
    # because it takes it from operand ${in_1}, while some CDO operators impose to have it second
    cscript('ccdo2_flip', 'cdo ${operator} ${in_2} ${in_1} ${out}')
    cscript('ccdo3_flip', 'cdo ${operator} ${in_3} ${in_1} ${in_2} ${out}')
    #
    cscript('ccdo_ens', 'cdo ${operator} ${mmin} ${out}')
    #
    cscript('minus', 'cdo sub ${in_1} ${in_2} ${out}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #
    cscript('plus', 'cdo add ${in_1} ${in_2} ${out}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #
    cscript('multiply', 'cdo mul ${in_1} ${in_2} ${out}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #
    cscript('divide', 'cdo div ${in_1} ${in_2} ${out}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #
    cscript('select_level', 'cdo sellevel,${level} ${in} ${out}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #
    cscript('space_average',
            scriptpath + 'mcdo.py --operator="fldmean" --output_file="${out}" --var="${var}" --period="${period_iso}"'
                         ' --region="${domain}" --alias="${alias}" --units="${units}" --vm="${missing}" ${ins}',
            commuteWithTimeConcatenation=True)
    cscript('space_average_fast',
            scriptpath + 'mcdo.py --operator="fldmean" --output_file="${out}" ${ins}',
            commuteWithTimeConcatenation=True)
    #
    cscript('time_average',
            scriptpath + 'mcdo.py --operator="timmean" --output_file="${out}" --var="${var}" --period="${period_iso}"'
                         ' --region="${domain}" --alias="${alias}" --units="${units}" --vm="${missing}" ${ins}',
            commuteWithSpaceConcatenation=True)
    cscript('time_average_fast',
            scriptpath + 'mcdo.py --operator="timmean" --output_file="${out}" ${ins}',
            commuteWithSpaceConcatenation=True)
    #
    cscript('llbox',
            scriptpath + 'mcdo.py --output_file="${out}" --var="${var}" --period="${period_iso}"'
                         ' --region="${latmin},${latmax},${lonmin},${lonmax}" '
                         '--alias="${alias}" --units="${units}" --vm="${missing}" ${ins}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    cscript('llbox_fast',
            scriptpath + 'mcdo.py --output_file="${out}" --region="${latmin},${latmax},${lonmin},${lonmax}" ${ins}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)

    #
    cscript('regrid',
            scriptpath + 'regrid.sh ${in} ${in_2} ${out} ${option}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=False)
    #
    cscript('regridn',
            scriptpath + 'regrid.sh ${in} ${cdogrid} ${out} ${option}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=False)
    #
    cscript('regridll', scriptpath + 'regridll.sh ${in} ${out} ${cdogrid} '
                                     '${latmin} ${latmax} ${lonmin} ${lonmax} ${remap_option}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=False)
    #
    cscript('rescale',
            'cdo expr,\"${var}=${scale}*${var}+${offset};\" ${in} ${out}',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #
    cscript('mean_and_std',
            scriptpath + 'mean_and_std.sh ${in} ${Var} ${out} ${out_sdev}',
            # This tells CliMAF how to compute varname for name output 'sdev'
            # using input varname
            sdev_var="std(%s)",
            commuteWithTimeConcatenation=True)
    #
    # Declare plot scripts (only where it is defined
    cscript('ncview', 'ncview ${in} 1>/dev/null 2>&1&', fatal=False)
    #
    # plot: main field (main_file) + auxiliary field (aux_file, optional) + vectors (u_file & v_file, optionals)
    #
    cscript('plot', '(ncl -Q ' + scriptpath + 'gplot.ncl main_file=\'"${in}"\' aux_file=\'"${in_2}"\' '
                                              'u_file=\'"${in_3}"\' v_file=\'"${in_4}"\' rotation=${rotation} '
                                              'plotname=\'"${out}"\' colormap=\'"${color}"\' vmin=${min} '
                                              'vmax=${max} vdelta=${delta} main_var=\'"${Var}"\' '
                                              'aux_var=\'"${var_2}"\' u_var=\'"${var_3}"\' v_var=\'"${var_4}"\' '
                                              'title=\'"${title}"\' myscale=${scale} myoffset=${offset} '
                                              'mpCenterLonF=${mpCenterLonF} vcRefMagnitudeF=${vcRefMagnitudeF} '
                                              'vcRefLengthF=${vcRefLengthF} vcMinDistanceF=${vcMinDistanceF} '
                                              'vcGlyphStyle=\'"${vcGlyphStyle}"\' '
                                              'vcLineArrowColor=\'"${vcLineArrowColor}"\' units=\'"${units}"\' '
                                              'y=\'"${y}"\' ccolors=\'"${colors}"\' level=${level} time=${time} '
                                              'date=\'"${date}"\' proj=\'"${proj}"\' contours=\'"${contours}"\' '
                                              'focus=\'"${focus}"\' type=\'"${format}"\' '
                                              'resolution=\'"${resolution}"\' trim=${trim} fmt=\'"${fmt}"\' '
                                              'vcb=${vcb} lbLabelFontHeightF=${lbLabelFontHeightF} invXY=${invXY} '
                                              'reverse=${reverse} tmYLLabelFontHeightF=${tmYLLabelFontHeightF} '
                                              'tmXBLabelFontHeightF=${tmXBLabelFontHeightF} '
                                              'tmYRLabelFontHeightF=${tmYRLabelFontHeightF} '
                                              'tiXAxisFontHeightF=${tiXAxisFontHeightF} '
                                              'tiYAxisFontHeightF=${tiYAxisFontHeightF} '
                                              'gsnPolarLabelFontHeightF=${gsnPolarLabelFontHeightF} '
                                              'tiMainFont=\'"${tiMainFont}"\' tiMainFontHeightF=${tiMainFontHeightF} '
                                              'tiMainPosition=\'"${tiMainPosition}"\' '
                                              'gsnLeftString=\'"${gsnLeftString}"\' '
                                              'gsnRightString=\'"${gsnRightString}"\' '
                                              'gsnCenterString=\'"${gsnCenterString}"\' '
                                              'gsnStringFont=\'"${gsnStringFont}"\' '
                                              'gsnStringFontHeightF=${gsnStringFontHeightF} '
                                              'shade_below=${shade_below} shade_above=${shade_above} '
                                              'options=\'"${options}"\' aux_options=\'"${aux_options}"\' '
                                              'shade2_options=\'\"${shade2_options}\"\' shade2_var=\'\"${var_5}\"\' '
                                              'shade2_file=\'\"${in_5}\"\' '
                                              'shade2_below=\'\"${shade2_below}\"\' '
                                              'shade2_above=\'\"${shade2_above}\"\' '
                                              'shading_options=\'\"${shading_options}\"\' myscale_aux=${scale_aux} '
                                              'myoffset_aux=${offset_aux} xpolyline=\'\"${xpolyline}\"\' '
                                              'ypolyline=\'\"${ypolyline}\"\' '
                                              'polyline_options=\'\"${polyline_options}\"\' )',
            format="graph")
    #
    # curves: plot a series of xy curves (along time, lat, lon or pressure/z_index) for an ensemble
    #
    cscript('curves', '(ncl -Q ' + scriptpath + 'curves.ncl infile=\'\"${mmin}\"\' '
                                                'plotname=\'\"${out}\"\' var=\'\"${Var}\"\' title=\'\"${title}\"\' '
                                                'y=\'\"${y}\"\' labels=\'\"${labels}\"\' colors=\'\"${colors}\"\' '
                                                'units=\'\"${units}\"\' X_axis=\'\"${X_axis}\"\' fmt=\'\"${fmt}\"\' '
                                                'options=\'\"${options}\"\' aux_options=\'\"${aux_options}\"\' '
                                                'lgcols=${lgcols} myscale=${scale} myoffset=${offset} '
                                                'type=\'\"${format}\"\' resolution=\'\"${resolution}\"\' trim=${trim} '
                                                'invXY=${invXY} vmin=${min} vmax=${max} myscale_aux=${scale_aux} '
                                                'myoffset_aux=${offset_aux} )',
            format="graph")
    #
    # hovm : to plot Hovmoller diagrams
    #
    cscript('hovm',
            '(ncl -Q ' + scriptpath + 'hovmoller.ncl infile=\'\"${in}\"\' plotname=\'\"${out}\"\' var=\'\"${Var}\"\' '
                                      ' invXY=${invXY} latS=\'\"${latS}\"\' latN=\'\"${latN}\"\' lonW=\'\"${lonW}\"\' '
                                      'lonE=\'\"${lonE}\"\' '
                                      ' colormap=\'\"${color}\"\' myscale=${scale} myoffset=${offset} '
                                      'units=\'\"${units}\"\' reverse=${reverse} mean_axis=\'\"${mean_axis}\"\' '
                                      'xpoint=${xpoint} ypoint=${ypoint} zpoint=${zpoint} title=\'\"${title}\"\' '
                                      ' type=\'\"${format}\"\' resolution=\'\"${resolution}\"\' trim=${trim} '
                                      'options=\'\"${options}\"\' fmt=\'\"${fmt}\"\' )',
            format="graph")
    #
    # cpdfcrop : pdfcrop by preserving metadata
    #
    cscript('cpdfcrop', binpath + 'pdfcrop ${in} ${out} ', format="pdf")
    #
    # cepscrop : crop 'eps' file using epstopdf, pdfcrop and pdftops
    #
    if os.system("type exiv2 >/dev/null 2>&1") == 0:
        cscript('cepscrop',
                'epstopdf ${in} --outfile=tmpfile.pdf;' + binpath + 'pdfcrop tmpfile.pdf tmpfile-crop.pdf; '
                                                                    'pdftops -eps tmpfile-crop.pdf ${out}; '
                                                                    'rm -f tmpfile.pdf tmpfile-crop.pdf ',
                format="eps")
    #
    cscript('ncdump', 'ncdump -h ${in} ', format="txt")
    #
    cscript('cslice_average',
            "ncks -O -F -v ${Var} -d ${dim},${min},${max} ${in} tmp.nc ; "
            "ncwa -O -a ${dim} tmp.nc ${out} ; rm -f tmp.nc")
    #
    cscript('cslice_select',
            "ncks -O -F -v ${Var} -d ${dim},${min},${max} ${in} ${out}")
    #
    cscript("mask", "cdo setctomiss,${miss} ${in} ${out}")
    #
    cscript("ncpdq", "ncpdq ${arg} ${in} ${out}")
    #
    # Add nav_lon and nav_lat to a file
    cscript('add_nav_lat',
            'cp ${in} ${out} ; ncks -A ${nav_lat_file} ${out} ;'
            ' ncatted -O -a coordinates,${Var},o,c,"${coordinates}" ${out}')
    cscript('add_nav_lon_nav_lat_from_mesh_mask',
            'cp ${in} ${out} ; ncks -A -v nav_lon,nav_lat ${mesh_mask_file} ${out}')
    #
    cscript('get_oneVar', 'ncks -v ${Var} ${in} ${out}')
    cscript('cncks', 'ncks -v ${Var} ${in} ${out}')
    # cscript('cnco','${operator} ${arg} ${in} ${out}')
    #
    # ensemble_ts_plot
    cscript('ensemble_ts_plot',
            'python ' + scriptpath + 'ensemble_time_series_plot.py '
                                     '--filenames="${mmin}" '
                                     '--outfig=${out} '
                                     '--labels=\'\"${labels}\"\' '
                                     '--variable=${Var} '
                                     '--colors="${colors}" '
                                     '--min="${min}" '
                                     '--max="${max}" '
                                     '--lw="${lw}" '
                                     '--offset="${offset}" --scale="${scale}" '
                                     '--highlight_period="${highlight_period}" '
                                     '--highlight_period_lw="${highlight_period_lw}" '
                                     '--xlabel="${xlabel}" --ylabel="${ylabel}" '
                                     '--xlabel_fontsize="${xlabel_fontsize}" '
                                     '--ylabel_fontsize="${ylabel_fontsize}" '
                                     '--xlim="${xlim}" --ylim="${ylim}" '
                                     '--tick_size="${tick_size}" '
                                     '--text="${text}" '
                                     '--text_fontsize="${text_fontsize}" '
                                     '--text_colors="${text_colors}" '
                                     '--text_verticalalignment="${text_verticalalignment}" '
                                     '--text_horizontalalignment="${text_horizontalalignment}" '
                                     '--legend_colors="${leg_colors}" '
                                     '--legend_labels="${legend_labels}" '
                                     '--title="${title}" '
                                     '--title_fontsize="${title_fontsize}" '
                                     '--left_string="${left_string}" '
                                     '--right_string="${right_string}" '
                                     '--center_string="${center_string}" '
                                     '--left_string_fontsize="${left_string_fontsize}" '
                                     '--right_string_fontsize="${right_string_fontsize}" '
                                     '--center_string_fontsize="${center_string_fontsize}" '
                                     '--legend_loc="${legend_loc}" '
                                     '--legend_xy_pos="${legend_xy_pos}" '
                                     '--legend_labels="${legend_labels}" '
                                     '--legend_colors="${legend_colors}" '
                                     '--legend_fontsize="${legend_fontsize}" '
                                     '--legend_ncol="${legend_ncol}" '
                                     '--legend_lw="${legend_lw}" '
                                     '--draw_legend="${draw_legend}" '
                                     '--legend_frame="${legend_frame}" '
                                     '--append_custom_legend_to_default="${append_custom_legend_to_default}" '
                                     '--left_margin="${left_margin}" '
                                     '--right_margin="${right_margin}" '
                                     '--top_margin="${top_margin}" '
                                     '--bottom_margin="${bottom_margin}" '
                                     '--horizontal_lines_values="${horizontal_lines_values}" '
                                     '--horizontal_lines_styles="${horizontal_lines_styles}" '
                                     '--horizontal_lines_lw="${horizontal_lines_lw}" '
                                     '--horizontal_lines_colors="${horizontal_lines_colors}" '
                                     '--vertical_lines_values="${vertical_lines_values}" '
                                     '--vertical_lines_styles="${vertical_lines_styles}" '
                                     '--vertical_lines_lw="${vertical_lines_lw}" '
                                     '--vertical_lines_colors="${vertical_lines_colors}" '
                                     '--fig_size="${fig_size}" ',
            format='png')
    #
    # cLinearRegression
    cscript('cLinearRegression',
            'python ' + scriptpath + 'LinearRegression_UVCDAT.py --X ${in_1} --xvariable ${var_1} --Y ${in_2} '
                                     '--yvariable ${var_2} --outfile ${out}',
            _var='slope')
    #
    # ml2pl (only on Ciclad)
    if onCiclad:
        cscript("ml2pl", scriptpath + "ml2pl.sh -p ${var_2} -v ${var_1} ${in_1} ${out} ${in_2}",
                commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
        fixed_fields("ml2pl", ("press_levels.txt", scriptpath + "press_levels.txt"))
    #
    # curl_tau_atm
    cscript('curl_tau_atm',
            'ferret -script ' + scriptpath + 'curl_tau_atm.jnl ${in_1} ${in_2} ${out} ; ncrename -d LON,lon -v LON,lon '
                                             '-d LAT,lat -v LAT,lat -v CURLTAU,curltau ${out} ; '
                                             'ncatted -O -a coordinates,curltau,o,c,"time lat lon" '
                                             '-a long_name,curltau,o,c,"Wind Stress Curl (Ferret: TAUV[D=2,X=@DDC]-TAUU'
                                             '[D=1,Y=@DDC])" ${out}',
            _var='curltau')

    #
    if os.system("type cdfmean >/dev/null 2>&1") == 0:
        load_cdftools_operators()
    else:
        clogger.warning("Binary cdftools not found. Some operators won't work")


def load_cdftools_operators():
    #
    # CDFTools operators
    #
    # cdfmean
    #
    cscript('ccdfmean',
            'cdfmean ${in} ${Var} ${pos_grid} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} ${opt}; ncks -O -x '
            '-v mean_${Var} cdfmean.nc ${out}; rm -f cdfmean.nc cdfmean.txt',
            _var="mean_3D%s", canSelectVar=True)
    #
    cscript('ccdfmean_profile',
            'cdfmean ${in} ${Var} ${pos_grid} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} ${opt}; ncks -O -x '
            '-v mean_3D${Var} cdfmean.nc ${out}; rm -f cdfmean.nc cdfmean.txt',
            _var="mean_%s", canSelectVar=True)
    #
    cscript('ccdfmean_profile_box',
            'cdfmean ${in} ${Var} ${pos_grid} $(cdffindij ${lonmin} ${lonmax} ${latmin} ${latmax} -c mask.nc '
            '-p ${pos_grid} | sed -n 3p) ${kmin} ${kmax} ${opt}; ncks -O -x -v mean_3D${Var} cdfmean.nc ${out}; '
            'rm -f cdfmean.nc cdfmean.txt',
            _var="mean_%s")
    #
    cscript('ccdfvar',
            'cdfmean ${in} ${Var} ${pos_grid} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} -var ${opt}; ncks -O -x '
            '-v mean_${Var},mean_3D${Var},var_${Var} cdfmean.nc ${out}; rm -f cdfmean.nc cdfmean.txt cdfvar.txt',
            _var="var_3D%s", canSelectVar=True)
    #
    cscript('ccdfvar_profile',
            'cdfmean ${in} ${Var} ${pos_grid} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} -var ${opt}; ncks -O -x '
            '-v mean_${Var},mean_3D${Var},var_3D${Var} cdfmean.nc ${out}; rm -f cdfmean.nc cdfmean.txt cdfvar.txt',
            _var="var_%s", canSelectVar=True)

    #
    # cdftransport : case where VT file must be given
    #
    # cscript('ccdftransport',
    #        scriptpath+'cdftransport.sh ${in_1} ${in_2} ${in_3} ${in_4} ${in_5} ${in_6} "${imin}" "${imax}" "${jmin}"
    #        "${jmax}" "${opt1}" "${opt2}" ${out} ${out_htrp} ${out_strp}',
    #       canSelectVar=True)
    cscript('ccdftransport',
            scriptpath + 'cdftransp.sh ${in_1} ${in_2} ${in_3} "${imin}" "${imax}" "${jmin}" "${jmax}" "${opt1}" '
                         '"${opt2}" ${out} ${out_htrp} ${out_strp}',
            _var='vtrp', htrp_var='htrp', strp_var='strp', canSelectVar=True)

    #
    # cdfheatc
    #
    cscript('ccdfheatc',
            'echo ""; cdfheatc ${in} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} ${opt}; mv cdfheatc.nc ${out};'
            ' rm -f cdfheatc.nc',
            _var="heatc_2D,heatc_3D", canSelectVar=True)
    #
    cscript('ccdfheatcm',
            'echo ""; tmp_file=`echo $(mktemp /tmp/tmp_file.XXXXXX)`; cdo merge ${in_1} ${in_2} $tmp_file; cdfheatc '
            '$tmp_file ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} ${opt}; mv cdfheatc.nc ${out}; rm -f cdfheatc.nc'
            ' $tmp_file',
            _var="heatc_2D,heatc_3D", canSelectVar=True)

    #
    # cdfsaltc
    #
    cscript('ccdfsaltc',
            'echo ""; cdfsaltc ${in} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} ${opt}; mv cdfsaltc.nc ${out};'
            ' rm -f cdfsaltc.nc',
            _var="saltc_2D,saltc_3D", canSelectVar=True)

    #
    # cdfsections
    #
    cscript('ccdfsections',
            scriptpath + 'cdfsections.sh ${in_1} ${in_2} ${in_3} ${larf} ${lorf} ${Nsec} ${lat1} ${lon1} ${lat2} '
                         '${lon2} ${n1} "${more_points}" ${out} ${out_Utang} ${out_so} ${out_thetao} ${out_sig0} '
                         '${out_sig1} ${out_sig2} ${out_sig4}',
            _var="Uorth", Utang_var="Utang", so_var="so", thetao_var="thetao", sig0_var="sig0", sig1_var="sig1",
            sig2_var="sig2", sig4_var="sig4", canSelectVar=True)
    #
    cscript('ccdfsectionsm',
            scriptpath + 'cdfsectionsm.sh ${in_1} ${in_2} ${in_3} ${in_4} ${in_5} ${larf} ${lorf} ${Nsec} ${lat1} '
                         '${lon1} ${lat2} ${lon2} ${n1} "${more_points}" ${out} ${out_Utang} ${out_so} ${out_thetao} '
                         '${out_sig0} ${out_sig1} ${out_sig2} ${out_sig4}',
            _var="Uorth", Utang_var="Utang", so_var="so", thetao_var="thetao", sig0_var="sig0", sig1_var="sig1",
            sig2_var="sig2", sig4_var="sig4", canSelectVar=True)

    #
    # cdfmxlheatc
    #
    cscript('ccdfmxlheatc',
            'echo ""; cdfmxlheatc ${in} ${opt}; mv mxlheatc.nc ${out}; rm -f mxlheatc.nc', _var="somxlheatc",
            canSelectVar=True)
    #
    cscript('ccdfmxlheatcm',
            'echo ""; tmp_file=`echo $(mktemp /tmp/tmp_file.XXXXXX)`; cdo merge ${in_1} ${in_2} $tmp_file; cdfmxlheatc '
            '$tmp_file ${opt}; mv mxlheatc.nc ${out}; rm -f mxlheatc.nc $tmp_file',
            _var="somxlheatc", canSelectVar=True)

    #
    # cdfstd
    #
    cscript('ccdfstd',
            'cdfstd ${opt} ${ins}; mv cdfstd.nc ${out}; rm -f cdfstd.nc', _var="%s_std", canSelectVar=True)
    #
    cscript('ccdfstdmoy',
            'cdfstd -save ${opt} ${ins}; mv cdfstd.nc ${out}; mv cdfmoy.nc ${out_moy}; rm -f cdfstd.nc cdfmoy.nc',
            _var="%s_std", moy_var="%s", canSelectVar=True)

    #
    # cdfvT ; a bit tricky about naming the output
    #
    cscript('ccdfvT', 'cdfvT ${in_1} ${in_2} ${in_3} ${in_4} -o ${out}', _var="vomevt,vomevs,vozout,vozous",
            canSelectVar=True)

    #
    # cdfzonalmean
    #
    cscript('ccdfzonalmean',
            'cdfzonalmean ${in} ${point_type} -var ${Var} ${opt}; varname=${Var}; ncrename '
            '-v zo${varname:2}_glo,zo${Var}_glo zonalmean.nc ${out}; rm -f zonalmean.nc',
            _var="zo%s_glo", canSelectVar=True)
    #
    # cdfzonalmean_bas
    #
    cscript('ccdfzonalmean_bas',
            'cdfzonalmean ${in} ${point_type} new_maskglo.nc -var ${Var} ${opt}; varname=${Var}; '
            'ncks -O -v zo${varname:2}_${basin} zonalmean.nc tmpfile.nc; ncrename -v zo${varname:2}_${basin},'
            'zo${Var}_${basin} tmpfile.nc ${out}; rm -f tmpfile.nc zonalmean.nc',
            _var="zo%s_${basin}", canSelectVar=True)
