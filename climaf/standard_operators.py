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

