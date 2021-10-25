#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script aims at reading netcdf files in python.
"""

from __future__ import division, print_function, unicode_literals, absolute_import

import os
import netcdftime
import math

from netCDF4 import Dataset as NetCDFFile

import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point

filename = "/home/rigoudy/Bureau/dev/CliMAF/tests/test_data/tas_Amon_CNRM-CM5_historical_r1i1p1_1850.nc"

nc = NetCDFFile(filename)

tas = nc.variables["tas"][:]
lat = nc.variables["lat"][:]
lon = nc.variables["lon"][:]
time = nc.variables["time"][:]

projection = ccrs.PlateCarree()
transform = ccrs.PlateCarree()

tas, lon = add_cyclic_point(tas, coord=lon)

tas_mean = np.mean(tas, axis=0)

ax = plt.axes(projection=projection)
plt.contourf(lon, lat, tas_mean, 50, cmap="Set3", transform=transform)
plt.colorbar(orientation="horizontal", extend="max", drawedges=False, format="%.1e", ax=ax)

ax.coastlines()

plt.show()
