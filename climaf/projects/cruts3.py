#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

This module declares CRUTS3 data organization and specifics, as managed by Sophie T. at CNRM;
see file:///cnrm/amacs/DATA/OBS/netcdf/

**Also declares how to derive CMIP5 variables from the original CRUTS3 variables set**

Attributes are 'grid'

Various grids are available. Original grid writes as : grid=''. Other grids write e.g. as : grid ='T127'

Example of an 'cruts3' project dataset declaration ::

 >>> cdef('project','cruts3')
 >>> d=ds(variable='tas',period='198001',grid='')
 >>> d2=ds(variable='tas',period='198001',grid='T127')

"""

from __future__ import print_function, division, unicode_literals, absolute_import

from env.environment import *
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cdef
from env.site_settings import atCNRM

if atCNRM:
    cproject('cruts3', 'grid')  # no grid writes as '', otherwise as e.g. 'T127'

    url1_cruts3 = "/cnrm/amacs/DATA/OBS/netcdf/monthly_mean/cruts3/${variable}_cru_ts_3${grid}.nc"
    # for original grid
    url2_cruts3 = "/cnrm/amacs/DATA/OBS/netcdf/monthly_mean/cruts3/${variable}_cru_ts_3.${grid}.nc"
    # for other grids write e.g. as : grid ='T127'
    dataloc(project='cruts3', organization='generic', url=[url1_cruts3, url2_cruts3])

    # Defining alias and derived variables for CRUTS3, together with filenames
    ##############################################################################

    calias("cruts3", 'clt', 'cld', filenameVar='cld')

    calias("cruts3", 'evspsbl', 'pet', scale=1. / 86400., filenameVar='pet', units="kg m-2 s-1")
    # pet:="potential evapotranspiration"; units="mm/day"
    # evspsbl:="water_evaporation_flux" en kg.m-2.s-1

    calias("cruts3", 'pr', 'pr', scale=1. / (86400. * 30.3), filenameVar='pr', units="kg m-2 s-1")
    # pr:="precipitation"; units="mm"
    # pr[CMIP5]:="precipitation" en kg.m-2.s-1

    calias("cruts3", 'tasmin', 'tmn', scale=1., offset=273.15, filenameVar='tmn', units="K")
    calias("cruts3", 'tas', 'tmp', scale=1., offset=273.15, filenameVar='tmp', units="K")
    calias("cruts3", 'tasmax', 'tmx', scale=1., offset=273.15, filenameVar='tmx', units="K")
    calias("cruts3", 'prw', 'vap', scale=1. / 0.0980665, filenameVar='vap', units="kg.m-2")

    # dtr:="diurnal temperature range"; units="degrees Celsius"
    # frs:="ground frost frequency"; units="days"
    # wet:="wet day frequency"; units="days"
