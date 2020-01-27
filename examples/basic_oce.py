#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example for CliMAF use with ORCA data

This example will work as is on CNRM's Lustre or Ciclad
"""

# S.Senesi - march 2015

# Load Climaf functions and site settings
# This sets logical flags 'onCiclad' and 'atCNRM'
import os

from climaf.api import *

# Define default value for some dataset facets
cdef("project", "CMIP5")
cdef("frequency", "monthly")

# Choose a model and define your dataset
if onCiclad:
    cdef("model", "IPSL-CM5A-LR")
else:
    if atCNRM:
        cdef("model", "CNRM-CM5", project="CMIP5")
    else:
        print("I do not know how to find CMIP5 data on this machine")
        exit(0)

tos = ds(experiment="historical", variable="tos", period="186001", table="Omon", model="CNRM-CM5")

# Display the basic filenames involved in the dataset (all filenames
# in one single string). CliMAF will search them at the data location
# which is the most specific among all declared data locations
print tos.baseFiles()

# Let CliMAF provide the filename for the exact dataset in its disk
# cache (select period and/or variables, aggregate files...)
my_file = cfile(tos)
print my_file

# Check file size and content

os.system("ls -al " + my_file)
# os.system("type ncdump && ncdump -h "+my_file)

# Plot first time step
fig = plot(tos)
cshow(fig)

# Select a latlon box and plot it
tos_box = llbox(tos, latmin=40, lonmin=-30, lonmax=5, latmax=66)
ncview(tos_box)

# Compute a time average on 10 years
tos = ds(experiment="historical", variable="tos", period="1860-1869", table="Omon")
tosavg = time_average(tos)
ncview(tosavg)

# Compute annual cycle over 10 years, using swiss knife operator 'ccdo', and look at it
anncycle = ccdo(tos, operator='ymonavg')
ncview(anncycle)

# Define the average annual cycle over the NINO34 box
nino34 = dict(lonmin=-170, lonmax=-120, latmin=-5, latmax=5)
extract = llbox(anncycle, **nino34)
space_averaged_cycle = ccdo(extract, operator='fldavg')
# print cfile(space_averaged_cycle)
ncview(space_averaged_cycle)

# Regrid the 2D annual cycle to a latlon grid, using CDO grid names
anncycle_4deg = regridn(anncycle, cdogrid="r90x45")
ncview(anncycle_4deg)

if cfile(anncycle) is None:
    exit(1)
