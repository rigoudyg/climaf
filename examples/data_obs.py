#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Example for CliMAF access to various obs/reanalyses data as managed on
CNRM's Lustre, using the pre-defined 'projects' : gpcp, gpcc, erai, erai-land, cruts3, ceres

"""

# S.Senesi - may 2015

# Load Climaf functions and site settings
# This sets logical flags 'onCiclad' and 'atCNRM'
from climaf.api import *

if not atCNRM:
    print "This example script access data available only at CNRM"
    exit(0)

# Playing with GPCP data
############################
cdef("project", "gpcp")
cdef("grid", '2.5d')
cdef("frequency", 'monthly')

# Basic field provided by GPCP is named precip and is in mm/day
pr_mmday = ds(variable="precip", period="197901")
# cshow(plot(pr_mmday,title='gpcp 1979-1980'))

# CliMAF provides 'pr' in SI units
pr_gpcp = ds(variable="pr", period="1979-1980")

pr_gpcp_avg = time_average(pr_gpcp)
cshow(plot(pr_gpcp_avg, title='gpcp 1979-1980'))

# Playing with GPCC data
############################
cdef("project", "gpcc")
cdef("grid", 'T127')
cdef("frequency", 'monthly')

# Basic field provided by GPCC is named 'GPCC' and is in mm/day
pr_gpcc_mmday = ds(variable="GPCC", period="197901")
# cshow(plot(pr_gpcc_mmday,title='gpcp 1979-1980'))

# CliMAF provide 'pr' in SI units
pr_gpcc = ds(variable="pr", period="1979-1980")

pr_gpcc_avg = time_average(pr_gpcc)
# cshow(plot(pr_gpcc_avg,title='gpcc 1979-1980'))

pr_gpcc_regridded = regrid(pr_gpcp_avg, pr_gpcc_avg)

# Compare GPCC and GPCC, with regridding
##########################################
gpcc_minus_gpcc = minus(pr_gpcc_avg, pr_gpcc_regridded)
cshow(plot(gpcc_minus_gpcc, title="GPCC minus GPCC - [1979-1980]"))

# ERAI
########################################
cdef('project', 'erai')
cdef("frequency", 'monthly')
d = ds(variable='z', period='198001', grid='_', frequency='monthly')
cross = ccdo(d, operator='zonmean')
cshow(plot(cross, title='ERAI Z 198001'))

# ERAI-LAND
#######################################
cdef('project', 'erai-land')
cdef("frequency", 'monthly')
# Only one variable is aliased by CliMAF:
d = ds(variable='snd', period='198001', grid='_')
fig = plot(d, title="ERAI-LAND Snow depth, 198001")
cshow(fig)

# CRUTS3
###############################
tcru = ds(project='cruts3', variable='tas', period='1980-2000', grid='T127')
tcru_ga = space_average(tcru)
tcru_yga = ccdo(tcru_ga, operator='yearmean')
f = curves(tcru_yga, title="Tempe CRUTS3")

# CERES
###########################
rlut = ds(project='ceres', variable='rlut', period='2001-2013')
# Compute annual cycle
rlut_cycle = ccdo(rlut, operator='ymonavg')
# Average annual cycle on a latlon box
cycle = space_average(llbox(rlut_cycle, latmin=-20, latmax=30, lonmin=-30, lonmax=50))
cshow(curves(cycle, title='rlut on box'))
