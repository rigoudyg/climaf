"""
Loads CliMAF standard operators. Invoked by standard CliMAF setup

The operators list also show in variable 'cscripts'

"""

import climaf
scriptpath=climaf.__path__[0]+"/../scripts/" 
from climaf.operators import cscript

# Compute scripts
cscript('mean_and_std',
        scriptpath+'mean_and_std.sh ${in} ${var} ${out} ${out_sdev}', 
        sdev_var="std(%s)" ) # This tells CliMAF how to name output 'sdev' using input variable name
cscript('space_average',scriptpath+'mcdo.sh fldmean ${out} ${var} ${period} ${ins}' )
cscript('time_average' ,scriptpath+'mcdo.sh timavg  ${out} ${var} ${period} ${ins}' )

# Declare plot scripts
cscript('ncview'    ,'ncview ${in}' , format=None)
cscript('timeplot'  , scriptpath+'timeplot.sh ${in} ${out} ${var} ${args}',format="png")
cscript('plotmap'   , "ncl "+ scriptpath +"plotmap.ncl infile=${in} plotname=${out} "+\
        "cmap=${color} vmin=${min} vmax=${max} vdelta=${delta} var=${var} title=${crs} "+\
        "scale=${scale} offset=${offset} units=${units}",format="png")
