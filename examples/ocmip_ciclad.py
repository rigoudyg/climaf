__doc__="""
Example for CliMAF access to data organized according to OCMIP5 on Ciclad as in :
/prodigfs/OCMIP5/OUTPUT/IPSL/IPSL-CM4/CTL/mon/CACO3/CACO3_IPSL_IPSL-CM4_CTL_1860-1869.nc

Current shortcoming : a number of OCMIP5 data facets used on Ciclad are not managed
  - 
"""

# S.Senesi - feb 2015

from climaf.api import *

# Declare a list of root directories for OCMIP5 data on Ciclad fiile system.
# The last value here contains a limited dataset, on lxaster7.cnrm.meteo.fr, for test purposes
urls_OCMIP5_Ciclad=["/prodigfs","/home/senesi/tmp/ciclad/prodigfs"]

# Declare a default location for searching data for all projects,experiment and frequencies,
# and that data located in dirs listed in urls_OCMIP_Ciclad is organized as 'OCMIP_Ciclad'
# i.e. as e.g. :  
# /prodigfs/OCMIP5/OUTPUT/IPSL/IPSL-CM4/CTL/mon/CACO3/CACO3_IPSL_IPSL-CM4_CTL_1860-1869.nc
dataloc(organization="OCMIP5_Ciclad", url=urls_OCMIP5_Ciclad)

# Define default value for some dataset facets
cdef("frequency","monthly") ; cdef("project","OCMIP5")

# Define your dataset (a number of facets take default values)
cactl=ds(experiment="CTL", model="IPSL-CM4", variable="CACO3", period="1860-1861")

# Display the basic filenames involved in the dataset (all filenames in one single string)
# CliMAF will search them at the data location which is the most specific among all declared data locations 
files=cactl.baseFiles()
print files

# Let CliMAF generate a file with the exact dataset in its disk cache (select period and/or variables, aggregate files...) 
my_file=cfile(cactl)
print my_file

# Check file size and content
import os
os.system("ls -al "+my_file)
#os.system("type ncdump && ncdump -h "+my_file)

if (myfile is None) : exit(1)

