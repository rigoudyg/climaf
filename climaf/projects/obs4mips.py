#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module declares locations for searching data for project OBS4MIP at CNRM (VDR),  for
all frequencies; see file:///cnrm/amacs/DATA/Obs4MIPs/doc/

Additional attribute for OBS4MIPS datasets : 'frequency'

Example for an OBS4MIPS CMIP5 dataset declaration ::

 >>> pr_obs=ds(project='OBS4MIPS', variable='pr', simulation='GPCP-SG', frequency='monthly', period='1979-1980')


"""

from __future__ import print_function, division, unicode_literals, absolute_import


from env.site_settings import atCNRM
from env.environment import *


if atCNRM:
    from climaf.dataloc import dataloc
    from climaf.classes import cproject, calias, cfreqs

    cproject("OBS4MIPS", "experiment", ("frequency", "monthly"))
    # Frequency alias
    cfreqs('OBS4MIPS', {'monthly': 'monthly_mean'})
    #
    pattern = "/cnrm/amacs/DATA/Obs4MIPs/netcdf/${frequency}/${variable}_${simulation}_*_${PERIOD}.nc"
    dataloc(project="OBS4MIPS", organization="generic", url=[pattern])
