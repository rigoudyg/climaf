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
    cscript('select' ,scriptpath+'mcdo.sh "${operator}" ${out} ${var} ${period_iso} ${domain} "${alias}" ${ins} ',
            commuteWithTimeConcatenation=True, commuteWithSpaceConcatenation=True)
    #
    cscript('ccdo',
            scriptpath+'mcdo.sh ${operator} ${out} ${var} ${period_iso} ${domain} "${alias}" ${ins}')
    #
    cscript('space_average',
            scriptpath+'mcdo.sh fldmean ${out} ${var} ${period_iso} ${domain} "${alias}" ${ins}', 
            commuteWithTimeConcatenation=True)
    #
    cscript('time_average' ,
            scriptpath+'mcdo.sh timavg  ${out} ${var} ${period_iso} ${domain} "${alias}" ${ins}' ,
            commuteWithSpaceConcatenation=True)
    #
    cscript('llbox' ,
            scriptpath+'mcdo.sh ""  ${out} ${var} ${period_iso} '
            '${latmin},${latmax},${lonmin},${lonmax} "${alias}" ${ins}',
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
            "cdo expr,\"${var}=${scale}*${var}+${offset};\" ${in} ${out}",
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
    #cscript('timeplot'  , scriptpath+'timeplot.sh ${in} ${out} ${var} ${title}',format="png")
    cscript('timeplot', 'ncl '+scriptpath+'timeplot.ncl infile=${in} outfile=${out} '
            'var=${var} title=${crs}',format="png")
    #
    cscript('plotmap'   , "(ncl -Q "+ scriptpath +"plotmap.ncl infile=${in} "
            "plotname=${out} cmap=${color} vmin=${min} vmax=${max} vdelta=${delta} "
            "var=${var} title=${crs} scale=${scale} offset=${offset} units=${units}) "
            "; convert ${out} -trim ${out}", format="png")
