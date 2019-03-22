#!/usr/bin/python
# -*- coding: utf-8 -*-

# example for remapping a dataset
#  1- to a named grid,
#  2- to the grid of another dataset

from climaf.api import *

# 0 - define a dataset
cdef("project", "example")
cdef("frequency", "monthly")
dg = ds(simulation="AMIPV6ALB2G", variable="tas", period="1980")

# 1- regrid to a named grid : use operator 'regridn'
dgr = regridn(dg, cdogrid="r90x45")
ncview(dgr)

# 2- regrid to a latlon box of a regular,named, grid : use operator 'regridll'
llbox_dg = regridll(dg, cdogrid="r180x90", latmin=-10., latmax=10, lonmin=-180, lonmax=180)
ncview(llbox_dg)

# 3- regrid to the grid of another datset (here, a trivial case : same grid) :
# use operator 'regridn'
dg2 = ds(simulation="AMIPV6ALB2G", variable="rst", period="1980")
dgr2 = regrid(dg, dg2)
ncview(dgr2)

if (cfile(dgr2) is None):
    exit(1)
