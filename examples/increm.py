#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" CliMAF - testing incremental cache

When, for a dataset or a computed results, two consecutive periods are
requested (and actually computed in file cache), the two periods are
merged in a single file, for efficiency purpose.

"""
# S.Senesi - oct 2014

from __future__ import print_function

# Load Climaf functions and site settings

from __future__ import print_function, division, unicode_literals, absolute_import

from climaf.api import *

# Reset CliMAF cache content
craz()

# Define data location for an simulation, as concisely as possible
cdef("project", "example")
cdef("simulation", "AMIPV6ALB2G")
cdef("variable", "tas")

# Define a 1-year dataset and have it written to cache
ds1 = ds(period="1980")
cfile(ds1)

print("cache index after first dataset evaluation on [1980]")
cdump()

# Define a longer dataset and have it written to cache too
ds2 = ds(period="1980-1981")
cfile(ds2)

# This has lead to a merge with previous file, as shown by file cache index
print("cache index after additional dataset evaluation on [1980-1981] : they are merged ")
cdump()

# Check that further access to sub-periods will use the merged file
dsf = ds(period="1981-1981")
f = cfile(dsf)

print("cache index after evaluation for [1981-1981]. A file was added for the subperiod, because explicitly asked for")
cdump()

if f is None:
    exit(1)
