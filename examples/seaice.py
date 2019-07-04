#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Example of CliMAF session with SeaIce data (here organized 'a la EM')

"""
# S.Senesi - may 2015

from climaf.api import *

import os

if not atCNRM or (os.getenv("USER") != "senesi" and os.getenv("USER") != "salas"):
    print "This example does work only at CNRM for some users"
    exit(0)

# Next declaration is actually built-in
dataloc(project="EM", organization="EM", url=["dummy"])

# Next declaration is now built-in in CliMAF (and also for a number of non-ambiguous variables)
calias('EM', 'sic', missing=1.e+20)

# Define default value for some dataset facets
cdef("frequency", "monthly")
cdef("project", "EM")

# Define your dataset (a number of facets take default values)
sic = ds(simulation="NG89", variable="sic", period="198310", realm="I")

# Display the basic filenames involved in the dataset (all filenames in one single string)
# CliMAF will search them at the data location which is the most specific among all declared data locations
files = sic.baseFiles()
print files

# Let CliMAF generate a file with the exact dataset in its disk cache (this
# select period and/or variables, aggregate files...)
my_file = cfile(sic)
print my_file

# Check file size and content
os.system("ls -al " + my_file)
os.system("type ncdump && ncdump -h " + my_file)

# Stereopolar plot with explicit levels. See other plot arguments in on-line help : 'help(plot)'
fig1 = plot(sic, title="Sic 198310 2", proj="NH70", colors="0.1 10 30 60 80 90 95 97 98 99", contours=1, focus="ocean")
cshow(fig1)

# Create a dictionnary in order to simplify the way to provide constant plot args :
pa = dict(proj="NH70", colors="0.1 10 30 60 80 90 95 97 98 99", contours=1, focus="ocean")

# Mask part of the SIC field
masked_sic = ccdo(sic, operator='setrtomiss,99,100')
figm = plot(masked_sic, title="mask above 0.99", **pa)
cshow(figm)

# Remap Sea Ice data to atmospheric grid. Use default option (remapbil)
tas = ds(project="EM", simulation="GSAGNS1", variable="tas", period="1975", realm="L")
sic_on_tas_grid = regrid(sic, tas)
fig2 = plot(sic_on_tas_grid, title="regridded_sic", **pa)
cshow(fig2)

# Access daily data
sicd = ds(simulation="NG89", variable="sic", period="198303-198304", realm="I", frequency='daily')
print sicd.baseFiles()

exit(0)
