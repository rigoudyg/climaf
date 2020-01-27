#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Computig and plotting an annual cycle

# Load Climaf functions
from climaf.api import *

# Define a dataset, in the pre-defined 'example' project (which datafiles
# locations are also pre-defined)
dg = ds(project="example", simulation="AMIPV6ALB2G", variable="tas",
        period="1980-1981", frequency="monthly")

# Compute annual cycle, using swiss knife operator 'ccdo', and look at it
anncycle = ccdo(dg, operator='ymonavg')
ncview(anncycle)

# Define the average annual cycle over a latlon box
extract = llbox(anncycle, latmin=30, latmax=60, lonmin=-30, lonmax=30)
space_average = ccdo(extract, operator='fldavg')

# Show it (this triggers computation)
ncview(space_average)

# Creating a figure with standard operator 'curves'
fig_avg = curves(space_average, title="Annual cycle")

# Get the figure computed, and get its filename in CliMAF file cache
figfile = cfile(fig_avg)

# Next command to ensure exit code is meaningful (for testing purposes)
if figfile is None:
        exit(1)

# Also test an operator which computed mean and standard deviation in one call
help(mean_and_std)
mean = mean_and_std(extract)
# Look at output 'sdev' (which is the standard deviation)
ncview(mean.sdev)
