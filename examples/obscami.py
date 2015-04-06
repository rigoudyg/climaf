__doc__="""
Example for CliMAF access to data organized according to CAMI atlas naming scheme such as :
[/cnrm/aster/data1/UTILS/cami/V1.7/climlinks]/CAYAN/hfls_1m_194601_199803_CAYAN.nc

  - 
"""

# S.Senesi - feb 2015

from climaf.api import *

# Declare a list of root directories for obs data organized 'a la CAMI' on CNRM's Lustre file system.
urls_OBS_CAMI=["/cnrm/aster/data1/UTILS/cami/V1.7/climlinks"]

# Declare a default location for searching OBS_CAMI data and that data located
# in dirs listed in urls_OBS_CAMI follow organization named OBS_CAMI
dataloc(project="OBS_CAMI", organization="OBS_CAMI", url=urls_OBS_CAMI)

# Define default value for some dataset facets
cdef("frequency","monthly") ; 

# Define your dataset (a number of facets take default values).
# For OBS_CAMI organization, for the time being, use attribute 'model' for indicating
# 'instrument' or 'source', and set experiment to "none"
pr_gpcp=ds(project="OBS_CAMI", model="GPCP2.5d", variable="pr", period="1979-1980", experiment="none")

# Display the basic filenames involved in the dataset (all filenames in one single string)
# CliMAF will search them at the data location which is the most specific among all declared data locations 
files=pr_gpcp.baseFiles()
print files

# Let CliMAF generate a file with the exact dataset in its disk cache (select period and/or variables, aggregate files...) 
my_file=cfile(pr_gpcp)
print my_file

# Check file size and content
import os
os.system("ls -al "+my_file)
#os.system("type ncdump && ncdump -h "+my_file)

if (myfile is None) : exit(1)

