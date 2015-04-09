__doc__="""
Example for CliMAF access to data organized according to OBS4MIPS data at CNRM such as :
[/cnrm/vdr/DATA/Obs4MIPs/netcdf/]monthly_mean/clt_MODIS_L3_C5_200003-201109.nc

  - 
"""

# S.Senesi - feb 2015

from climaf.api import *

# Declare a list of root directories for CMIP5 data on CNRM's Lustre file system.
urls_OBS4MIPS_CNRM=["/cnrm/vdr/DATA/Obs4MIPs/netcdf"]

# Declare a default location for searching OBS4MIPS data and that data located
# in dirs listed in urls_OBS4MIPS_CNRM follow organization named OBS4MIPS_CNRM
dataloc(project="OBS4MIPS", organization="OBS4MIPS_CNRM", url=urls_OBS4MIPS_CNRM)

# Define default value for some dataset facets
cdef("frequency","monthly") ; 

# Define your dataset (a number of facets take default values).
# For Obs4MIPS, for the time being, use attribute 'model' for indicating 'instrument', and set experiment to "none"
pr_obs=ds(project="OBS4MIPS", model="GPCP", variable="pr", period="1979-1980", experiment="none")

# Display the basic filenames involved in the dataset (all filenames in one single string)
# CliMAF will search them at the data location which is the most specific among all declared data locations 
files=pr_obs.baseFiles()
print files

# Let CliMAF generate a file with the exact dataset in its disk cache (select period and/or variables, aggregate files...) 
my_file=cfile(pr_obs)
print my_file

# Check file size and content
import os
os.system("ls -al "+my_file)
#os.system("type ncdump && ncdump -h "+my_file)

if (my_file is None) : exit(1)
