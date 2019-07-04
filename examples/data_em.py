#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Example for CliMAF access to data organized according to CNRM-CM's 'em' scheme

See also  :download:`climaf/projects/em.py <../climaf/projects/em.py>`

"""

# S.Senesi - april 2015

import os

from climaf.api import *

if not atCNRM:
    exit(0)

cdef("project", "em")

# What is my EM root directory (EM_NETCDF_DIR)
cdef("root", "/cnrm/est/USERS/senesi/NO_SAVE/expes", project="em")

# Define some datasets based on private experiments

# Basic case : no need to quote a realm if the variable is unambiguous among realms
pr1 = ds(simulation="CPICTLbx", variable="clt", period="1975")

# If your experiment belongs to an ECLIS group
pr2 = ds(simulation="GSAG", variable="pr", period="1975", group="PRE_AR6")

# Getting the tas value explictly from Atmosphere data
tasA = ds(simulation="GSAG", variable="tas", period="1975", group="PRE_AR6", realm="A")
# ... or getting anyone (atmos or land)
tas = ds(simulation="GSAG", variable="tas", period="1975", group="PRE_AR6")

# For ocean data, must provide a specific frequency name
tos = ds(simulation='PICTLWS2', variable="tos", period="225011", frequency="m")
sic = ds(simulation='HISTNATr8', variable="sic", period="186001")

# Next datasets (implicitly) refer to shared experiments
Pr = ds(simulation="C1P60", variable="pr", period="1850", group="SC")
Tas = ds(simulation="C1P60", variable="tas", period="1850", group="SC")
Tos = ds(simulation="CHISTr1", variable="tos", period="1975", group="SC", frequency="m")
Sic = ds(simulation="CHIST2", variable="sic", period="1975", group="SC")

# Display the basic filenames involved in the dataset (all filenames in one single string)
# CliMAF will search them at the data location which is the most specific among all declared data locations
files = tas.baseFiles()
print files

# Let CliMAF generate a file with the exact dataset in its disk cache (this
# select period and/or variables, aggregate files...)
my_file = cfile(tas)
print my_file

# Check file size and content
os.system("ls -al " + my_file)
# os.system("type ncdump && ncdump -h "+my_file)

# Try with Ocean data
print(Tos.baseFiles())

# Remap Ocean data to atmospheric grid. Use remapbil because default remapcon2 option needs cell areas

# WARNING : some ocean data have bad dimension names and/or bad
# coordinates names (eg 't_ave_01_month' instead of
# 'time_counter'); you should set 'export CLIMAF_FIX_NEMO_TIME=1'
# before launching CliMAF for ClIMAF to correct for that before
# regridding; It will take some processing time, but only if needed ...

tos_on_tas_grid = regrid(tos, tas, option="remapbil")
ncview(tos_on_tas_grid)

# Next line for automated tests
if cfile(tos_on_tas_grid) is None:
    exit(1)
