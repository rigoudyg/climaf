"""
Management of CliMAF standard operators

"""

from climaf import __path__ as cpath
from climaf.operators import cscript

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
            # This tells CliMAF how to name output 'sdev' using input variable name
            sdev_var="std(%s)" , 
            commuteWithTimeConcatenation=True)
    #
    # Declare plot scripts
    cscript('ncview'    ,'ncview ${in} 1>/dev/null 2>&1&' )
    #
    cscript('timeplot', 'ncl '+scriptpath+'timeplot.ncl infile=\'\"${in}\"\' outfile=\'\"${out}\"\' '
            'var=\'\"${var}\"\' title=\'\"${title}\"\'',format="png")
    #
#    cscript('plot'     , '(ncl -Q '+ scriptpath +'gplot.ncl infile=\'\"${in}\"\' '
#            'plotname=\'\"${out}\"\' cmap=\'\"${color}\"\' vmin=${min} vmax=${max} vdelta=${delta} '
#            'var=\'\"${var}\"\' title=\'\"${title}\"\' scale=${scale} offset=${offset} '
#            'units=\'\"${units}\"\' linp=${linp} levels=\'\"${levels}\"\' '
#            ' proj=\'\"${proj}\"\' contours=${contours} focus=\'\"${focus}\"\' && '
#            'convert ${out} -trim ${out}) ', format="png")


    # new version of gplot : plot only main field
    cscript('plot'     , '(ncl -Q '+ scriptpath +'gplot.ncl infile=\'\"${in}\"\' '
            'plotname=\'\"${out}\"\' cmap=\'\"${color}\"\' vmin=${min} vmax=${max} vdelta=${delta} '
            'var=\'\"${var}\"\' title=\'\"${title}\"\' scale=${scale} offset=${offset} '
            'units=\'\"${units}\"\' linp=${linp} levels=\'\"${levels}\"\' '
            ' proj=\'\"${proj}\"\' contours=\'\"${contours}\"\' focus=\'\"${focus}\"\' && '
            'convert ${out} -trim ${out}) ', format="png")
    #
    # gplot_2fields : plot a main field + an auxiliary field
    cscript('plot_2fields'  , '(ncl -Q '+ scriptpath +'gplot_2fields.ncl infile=\'\"${in}\"\' infile2=\'\"${in_2}\"\' '
            'plotname=\'\"${out}\"\' cmap=\'\"${color}\"\' vmin=${min} vmax=${max} vdelta=${delta} '
            'var=\'\"${var}\"\' var2=\'\"${var_2}\"\' title=\'\"${title}\"\' scale=${scale} offset=${offset} '
            'units=\'\"${units}\"\' linp=${linp} levels=\'\"${levels}\"\' '
            ' proj=\'\"${proj}\"\' contours=\'\"${contours}\"\' focus=\'\"${focus}\"\' && '
            'convert ${out} -trim ${out}) ', format="png")
    
        
    #
    cscript('lines'     , '(ncl -Q '+ scriptpath +'lineplot.ncl infile=\'\"${mmin}\"\' '
            'plotname=\'\"${out}\"\' var=\'\"${var}\"\' title=\'\"${title}\"\' '
            'linp=${linp} labels=\'\"${labels}\"\'  colors=\'\"${colors}\"\'  thickness=${thickness} && '
            'convert ${out} -trim ${out}) ', format="png")



    cscript('test_plot'     , '(ncl -Q '+ scriptpath +'test_LV.ncl infile=\'\"${in}\"\' '
            ' infile2=\'\"${in_2}\"\' plotname=\'\"${out}\"\' '
            ' var=\'\"${var}\"\'  var2=\'\"${var_2}\"\' && ' 
            ' convert ${out} -trim ${out}) ', format="png")
# mettre var signifie que le script est capable d aller extraire la variable sinon c climaf qui le fait
#(et donc on ne met pas var=)
