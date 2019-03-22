#!/usr/bin/python
# -*- coding: utf-8 -*-

# example for :
#  1- defining a dataset restricted to a lat-lon box
#  2- applying a further, explicit extraction of a sub box

# Load Climaf functions and site settings
from climaf.api import *

cdef("frequency", "monthly")
cdef("project", "example")
dg = ds(simulation="AMIPV6ALB2G", variable="tas",
        period="1980-1981", domain=[10, 80, -50, 40])
ncview(dg)

# How to further extract from a dataset ( even if it is not a global one )
de = llbox(dg, latmin=30, latmax=60, lonmin=-30, lonmax=30)
ncview(de)

# How to use names rather than latmin/latmax/lonmin/lonmax
box = dict()
box["nino28"] = [-150, -130, -5, 5]
dg_nino28 = ds(simulation="AMIPV6ALB2G", variable="tas",
               period="1980-1981", domain=box["nino28"])
f = cfile(dg_nino28)

if (f is None):
    exit(1)
