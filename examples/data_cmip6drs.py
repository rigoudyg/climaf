#!/usr/bin/python
# -*- coding: utf-8 -*-

__doc__ = """
Example for CliMAF access to data organized according to CMIP6 DRS such as :
/cnrm/cmip6/CMIP/CNRM-CERFACS/CNRM-CM6-1/historical/r1i1p1f2/Amon/clivi/gr/latest/clivi_Amon_CNRM-CM6-1_historical_r1i1p1f2_gr_185001-201412.nc

This example should work as is at CNRM and IPSL, and can be easily tuned to 
other local CMIP6 datasets

NOTE : Both the CMIP5 project definition and the CMIP5 data locations 
indicated here are actually already declared in standard CliMAF API 
setup (by ``import site_settings`` and ``import standard_projects``)
"""

# S.Senesi - feb 2015

import os

from climaf.api import *

# Define default value for some dataset facets
cdef("project", "CMIP6")
cdef("model", "CNRM-CM6-1", project="CMIP6")

# Define your dataset (a number of facets take default values)
tas1pc = ds(experiment="1pctCO2", realization='r1i1p1f2', variable="tas", table="Amon", period="1862-1863", )

# Display the basic filenames involved in the dataset (all filenames
# in one single string). CliMAF will search them at the data location
# which is the most specific among all declared data locations
files = tas1pc.baseFiles()
print files

# Let CliMAF generate a file with the exact dataset in its disk cache
# (select period and/or variables, aggregate files...)
my_file = cfile(tas1pc)
print my_file

# Check file size and content
os.system("ls -al " + my_file)
# os.system("type ncdump && ncdump -h "+my_file)

if my_file is None:
    exit(1)
