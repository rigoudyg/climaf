#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, unicode_literals, absolute_import

from env.clogging import clogger
from env.environment import *

try:
    from Scientific.IO.NetCDF import NetCDFFile as ncf
except ImportError:
    try:
        from NetCDF4 import netcdf_file as ncf
    except ImportError:
        try:
            from netCDF4 import Dataset as ncf
        except ImportError:
            try:
                from scipy.io.netcdf import netcdf_file as ncf
            except ImportError:
                clogger.critical(
                    "Netcdf handling is yet available only with modules Scientific.IO.Netcdf or NetCDF4 or "
                    "scipy.io.netcdf ")
                exit()
                # raise Climaf_Netcdf_Error("Netcdf handling is yet available only with modules Scientific.IO.Netcdf or
                #                            NetCDF4 or scipy.io.netcdf ")
