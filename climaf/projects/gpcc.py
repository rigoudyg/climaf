#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This module declares GPCC data organization and specifics, as managed by Sophie T. at CNRM;
see file:///cnrm/amacs/DATA/OBS/netcdf/

**Also declares how to derive CMIP5 variables from the original GPCC variables set**

Attributes are 'grid'

Various grids are available. Grids write e.g. as: grid='05d', grid ='1d' and grid ='T127'

Example of an 'gpcc' project dataset declaration ::

 >>> cdef('project','gpcc')
 >>> d=ds(variable='pr',period='198001',grid='05d')
 >>> d2=ds(variable='pr',period='198001',grid='1d')
 >>> d3=ds(variable='pr',period='198001',grid='T127')

"""

from __future__ import print_function, division, unicode_literals, absolute_import

from env.site_settings import atCNRM
from env.environment import *
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias

if atCNRM:
    cproject('gpcc', 'grid')  # grid writes as '05d', '1d' or 'T127'

    url_gpcc = "/cnrm/amacs/DATA/OBS/netcdf/monthly_mean/gpcc/GPCC.Reanalysis.${grid}.nc"
    dataloc(project='gpcc', organization='generic', url=[url_gpcc])

    # Defining alias and derived variables for GPCC, together with filenames
    ##############################################################################

    calias("gpcc", 'pr', 'GPCC', scale=1. / 86400., missing=1.e+20, units="kg m-2 s-1")

    # calias("gpcc",'GPCC'    ,'GPCC' ,                                   ,units="mm/day")
    # NSTA:="Number of stations available for a specific analysis grid in a specific month"
    # calias("gpcc",'site'    ,'NSTA'   )
