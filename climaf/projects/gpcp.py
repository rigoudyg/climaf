#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

This module declares GPCP data organization and specifics, as managed by Sophie T. at CNRM;
see file:///cnrm/amacs/DATA/OBS/netcdf/

**Also declares how to derive CMIP5 variables from the original GPCP variables set (aliasing/scaling)**

Attributes are 'grid', and 'frequency'.

Various grids are available. Grids write e.g. as : grid='1d', grid ='2.5d', grid ='T42' and grid ='T127'

Only two variables are available : the original 'precip' (mm/day) and pr (kg m-2 s-1)

Example of an 'gpcp' project dataset declaration ::

 >>> cdef('project','gpcp')
 >>> d=ds(variable='pr',period='198001',grid='2.5d', frequency='monthly')
 >>> d2=ds(variable='pr',period='198001',grid='1d',frequency='daily')

"""

from climaf.dataloc import dataloc
from climaf.classes import cproject, calias
from climaf.site_settings import atCNRM

if atCNRM:
    cproject('gpcp', 'grid', ('frequency', 'monthly'), separator="_")  # grid writes as '1d', '2.5d', 'T42' or 'T127'

    root = "/cnrm/amacs/DATA/OBS/netcdf/${frequency}"
    patmonth = root + "_mean/gpcp/${variable}_gpcp.${grid}.nc"
    patday = root + "/gpcp/${variable}_gpcp.${grid}.nc"
    dataloc(project='gpcp', organization='generic', url=[patmonth, patday])

    # Defining alias and derived variables for GPCP, together with filenames
    ##############################################################################

    # Original data is mm/day
    calias("gpcp", 'precip', 'precip', filenameVar='pr')
    # Compute in SI
    calias("gpcp", 'pr', 'precip', scale=1. / 86400., units="kg m-2 s-1", filenameVar='pr')
