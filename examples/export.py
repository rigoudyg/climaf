#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

# How to export CliMAF results as NetCDF files or Numpy Masked Arrays
#####################################################################

from __future__ import print_function, division, unicode_literals, absolute_import

# Load Climaf functions and site settings
from climaf.api import *

# Define a default value for two dataset facets
cdef("project", "example")
cdef("frequency", "monthly")

# Define some dataset you want to study ( a number of facets take default values )
dg = ds(simulation="AMIPV6ALB2G", variable="tas", period="1980-1981")

# Compute its space_average using a CliMAF standard operator based on a script based on CDO
sa = space_average(dg)

# Computing and exporting a CliMAF object as a NetCDF file
# ----------------------------------------------------------
# Just requiring the filename if CliMAF cache
saFile = cfile(sa)
# Requiring a copy the result as some other place
saFile = cfile(sa, "~/tmp/space_average.nc")

# Requiring a symbolic link to CliMAF cache result
saFile = cfile(sa, "~/tmp/space_average_link.nc", ln=True)

# Requiring a hard link to CliMAF cache result
saFile = cfile(sa, "~/tmp/space_average_hard.nc", hard=True)

# Looking at the result
print(saFile)
os.system("ncdump -h " + saFile)

# Computing and exporting a CliMAF object as a NumPy Masked Array
# ----------------------------------------------------------------
saMA = cMA(sa)

# Looking at the result
type(saMA)
# -> numpy.ma.core.MaskedArray
saMA.shape
saMA.data

# next line is only for systematic tests purpose
if saFile is None:
    exit(1)
