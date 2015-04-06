__doc__="""
Example for CliMAF access to data organized according to CNRM-CM's 'EM' scheme
"""

# S.Senesi - arpil 2015

from climaf.api import *
dataloc(organization="EM", project="CNRM-CM", url=["dummy"])

# Define default value for some dataset facets
cdef("frequency","monthly") ;  

# Define your dataset (a number of facets take default values)
tas=ds(project="CNRM-CM", experiment="GSAGNS1", variable="tas", period="1975")

# Display the basic filenames involved in the dataset (all filenames in one single string)
# CliMAF will search them at the data location which is the most specific among all declared data locations 
files=tas.baseFiles()
print files

# Let CliMAF generate a file with the exact dataset in its disk cache (this
# select period and/or variables, aggregate files...) 
my_file=cfile(tas)
print my_file

# Check file size and content
import os
os.system("ls -al "+my_file)
#os.system("type ncdump && ncdump -h "+my_file)

# Test access to Ocean data
tos=ds(project="CNRM-CM", experiment="CSU260a", variable="tos", period="213001")
print(tos.baseFiles())

# Remap Ocean data to atmospheric grid. Use remapbil because default remapcon2 option needs cell areas
tos_on_tas_grid=regrid(tos,tas, option="remapbil")
ncview(tos_on_tas_grid)

if (cfile(tosçon_tas_grid) is None) : exit(1)