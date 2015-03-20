__doc__="""
Example for CliMAF access to data organized according to CMIP5 DRS such as :
...../CMIP5/output1/CNRM-CERFACS/CNRM-CM5/1pctCO2/mon/atmos/Amon/r1i1p1/v20110701/clivi/clivi_Amon_CNRM-CM5_1pctCO2_r1i1p1_185001-189912.nc

This example will work as is on CNRM's Lustre , and can be easily tuned to other local CMIP5 datasets
Current shortcoming : duplicates are not removed (e.g. re. CMIP5_table, realm or lab)
  - 
"""

# S.Senesi - feb 2015

from climaf.api import *

# Declare a list of root directories for CNRM-CM CMIP5 data on CNRM's Lustre file system.
urls_CMIP5_CNRM=["/cnrm/aster/data2/ESG/data1", "/cnrm/aster/data2/ESG/data2", "/cnrm/aster/data2/ESG/data5",
      "/cnrm/aster/data4/ESG/data6", "/cnrm/aster/data4/ESG/data7", "/cnrm/aster/data4/ESG/data8"]

# Declare a list of root directories for CMIP5 data on IPLS's Ciclad file system
urls_CMIP5_Ciclad=["/prodigfs/esg"]

# Declare locations for searching data for all projects,experiment and
# frequencies, and that data located in dirs listed in urls_CMIP5_CNRM
# and urls_CMIP5_Ciclad is organized as 'CMIP5_DRS'
dataloc(organization="CMIP5_DRS", url=urls_CMIP5_CNRM+urls_CMIP5_Ciclad)

# Define default value for some dataset facets
cdef("frequency","monthly") ;  cdef("project","CMIP5")

# Define your dataset (a number of facets take default values)
tas1pc=ds(model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1860-1861")

# Display the basic filenames involved in the dataset (all filenames in one single string)
# CliMAF will search them at the data location which is the most specific among all declared data locations 
files=tas1pc.selectFiles()
print files

# Let CliMAF generate a file with the exact dataset in its disk cache (select period and/or variables, aggregate files...) 
my_file=cfile(tas1pc)
print my_file

# Check file size and content
import os
os.system("ls -al "+my_file)
#os.system("type ncdump && ncdump -h "+my_file)


