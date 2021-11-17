#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module declares project example and its data location for the standard CliMAF distro

Only one additionnal attribute: frequency (but data sample actually includes only frequency= 'monthly')

Example of an 'example' dataset definition ::

 >>> dg=ds(project='example', simulation='AMIPV6ALB2G', variable='tas', period='1980-1981', frequency='monthly')


"""

from __future__ import print_function, division, unicode_literals, absolute_import

import os

from env.environment import *
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs

from climaf import __path__ as cpath

cpath = os.path.abspath(cpath[0])

cproject("example", ("frequency", "monthly"), separator='|')
cfreqs('example', {'monthly': 'mon'})

data_pattern_L = cpath + "/../examples/data/${simulation}/L/${simulation}SFX${PERIOD}.nc"
data_pattern_A = cpath + "/../examples/data/${simulation}/A/${simulation}PL${PERIOD}.nc"
data_pattern_histmth = cpath + "/../examples/data/${simulation}_SE_1982_1991_1M_ua_pres.nc"
dataloc(project="example", organization="generic", url=[data_pattern_A, data_pattern_L, data_pattern_histmth])

# calias("example",'tas','tas_${frequency}')
