#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, unicode_literals, absolute_import

from climaf.api import calias
from climaf.operators_derive import derive
from env.environment import *

# Content was sent to various places : prokect IGCM_OUT, atmposphere_derived_variables, ocean_derived_variables


# -- LMDZ

# -- GPP total ready for comparison with obs
# calias("IGCM_OUT", 'cfracgpp', 'gpp' ,filenameVar='stomate_ipcc_history')
# derive("IGCM_OUT", 'gpptot', 'divide', 'cfracgpp','Contfrac')
# -> alias for the obs


derive('*', 'dtr', 'minus', 'tasmax', 'tasmin')
derive('IGCM_OUT', 'pme', 'minus', 'precip', 'evap')
calias('CMIP6', 'wfo', 'wfonocorr')
