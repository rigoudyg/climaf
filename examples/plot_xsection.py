#!/usr/bin/python
# -*- coding: utf-8 -*-

# import sys; sys.path.append("/home/stephane/Bureau/climaf")
from climaf.api import *

craz()

# Define a 3D dataset, using a pre-defined data set
##################################################################
january_ta = ds(project='example', simulation="AMIPV6ALB2G", variable="ta", frequency='monthly', period="198001")

# plot map for first level
map = plot(january_ta, title='January')
cshow(map)
# Plot on stereopolar grid
mapNH = plot(january_ta, title='January', proj="NH", min=240, max=290, delta=5)
cshow(mapNH)

# Compute zonal mean and plot it
ta_zonal_mean = ccdo(january_ta, operator="zonmean")
zplot = plot(ta_zonal_mean, title="Zonal mean")
cshow(zplot)

# Plot with vertical levels equally spaced (with their index)
zplotl = plot(ta_zonal_mean, title='title', y="index")
cshow(zplotl)

# Compute meridional mean and plot it
ta_merid_mean = ccdo(january_ta, operator="mermean")
mplot = plot(ta_merid_mean, title="Meridional mean")
cshow(mplot)

# Profile of global mean
ta_profile = ccdo(ta_merid_mean, operator="zonmean")
gplot = plot(ta_profile, title="TA profile, log", y="log")
cshow(gplot)

# Same plot except levels equally spaced
gplotl = plot(ta_profile, title="TA profile, index-linear", y="index")
cshow(gplotl)

# Plot horizontal profile : Meridional profile of zonal tas mean
jtas = ds(project='example', simulation="AMIPV6ALB2G", variable="tas", frequency='monthly', period="198001")
tas_profile = ccdo(jtas, operator="zonmean")
profplot = plot(tas_profile, title="Meridional tas profile")
cshow(profplot)

# Newt line is used for systematic test suite
fig = cfile(profplot)
if fig is None:
    exit(1)
