# How to export CliMAF results as NetCDF files or Numpy Masked Arrays, when
# you are sure that you cannot go further using CliMAF

from climaf.api import *
import os

# Define data location for an experiment, as concisely as possible
dataloc(experiment="AMIPV6ALB2G", organization="example", url=[cpath+"/../examples/data/AMIPV6ALB2G"])

# Define a default value for one dataset facet
cdef("frequency","monthly")

# Define some dataset you want to study ( a number of facets take default values )
dg=ds(experiment="AMIPV6ALB2G", variable="tas", period="1980-1981")

# Compute its space_average using a CliMAF standard operator based on a script based on CDO 
sa=space_average(dg)

# Computing and exporting a CliMAF object as a NumPy Masked Array
#----------------------------------------------------------------
saMA=cexport(sa,format="MaskedArray")
# Shortcut :
saMA=cMA(sa)

# Looking at the result
type(saMA)
# -> numpy.ma.core.MaskedArray
saMA.shape
saMA.data

# Computing and exporting a CliMAF object as a NetCDF file
#----------------------------------------------------------
saFile=cexport(sa,format="NetCDF")
# Shortcut :
saFile=cfile(sa)

# Looking at the result
print saFile
os.system("ncdump -h "+saFile)
