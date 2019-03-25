#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, unicode_literals, absolute_import

from climaf.api import *

# Define a dataset, using a built-in pre-defined datafile location
##################################################################
cdef("project", "example")
cdef("frequency", "monthly")
dg = ds(simulation="AMIPV6ALB2G", variable="tas", period="1980-1981")
cfile(dg)

# Compute its basic climatology using a stndard operator external script
##########################################################################
ta = time_average(dg)

# A simple plotting using standard operator ncview
##################################################
# For reference, here is the declaration of oeprator 'ncview' :
# cscript('ncview' ,'ncview ${in}' , format=None)
# ncview(ta)

# A NCL-quality plot, using standard operator plot
#############################################################
map = plot(ta, title="TAS")

# Ensure figure is computed, and get its cache filename in CliMAF disk cache
figfile = cfile(map)

# Displaying a figure object will compute and cache it if not already done
cshow(map)


# A more comprehensive way of configuring plots
###################################################
def map_graph_attributes(var):
    """
    Return a dictionnary with graphic attributes :
    - relevant to the geophysical variable in argument
    - with adequate keys for operator 'plot'
    """
    rep = dict()
    rep["min"] = 0
    rep["max"] = 100
    rep["delta"] = 10.
    #
    if var == 'tas':
        rep["offset"] = -273.15
        rep["units"] = "C"
        rep["min"] = -15
        rep["max"] = 25
        rep["delta"] = 2.
    #
    return rep


map2 = plot(ta, title="Surface temperature (tas)", **map_graph_attributes(varOf(ta)))
cshow(map2)

if cfile(map2) is None:
    exit(1)
