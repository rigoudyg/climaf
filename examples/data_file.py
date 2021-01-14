#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example for declaring a dataset from a datafile, quite simply, using function fds()
"""

# S.Senesi - sept 2015

from __future__ import print_function

# Load Climaf functions
from __future__ import print_function, division, unicode_literals, absolute_import

from climaf.api import *

# Let us use a CMIP5-compliant datafile which is included in CliMAF distro
datafile = cpath + "/../examples/data/tas_Amon_CNRM-CM5_historical_r1i1p1_185001-185212.nc"

# If you want to explore the data file
explore = fds(datafile)
print('variable(s)=', explore.variable)
print('period=', explore.period)
print('model=', explore.model)
print('simu=', explore.simulation)
print('file=', explore.baseFiles())

# What is the internal representation (or 'CRS') of the dataset
print(repr(explore))

# Let us play with a multi-variable file (a file which is not CMIP5 compliant -> must provide period)
multifile = cpath + "/../examples/data/AMIPV6ALB2G/A/AMIPV6ALB2GPL1980.nc"
all = fds(multifile, period="1980")
print('variable(s)=', all.variable)
print('model=', all.model)

# If you know what you want from the data file
my_rst = fds(multifile, variable='rst', period='198004')

# You may whish that CliMAF handles the model name, and a sensible simulation name
my_rst = fds(multifile, simulation='my_simu', model='CNRM-CM', variable='rst', period='198004')
cshow(plot(my_rst, title='Multivar file example'))
