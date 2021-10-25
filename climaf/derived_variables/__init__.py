#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import  # , unicode_literals

# Some projects like atmosphere_derived_variables, others don't
# __all__= [ "atmosphere_derived_variables", "ocean_derived_variables" ]
__all__ = ["ocean_derived_variables", ]

from env.site_settings import *
from env.environment import *

# -- Load only the ipsl derived variables if we are at IPSL
if atIPSL:
    from . import atmosphere_derived_variables
    from . import ipsl_derived_variables

# Load atmosphere derived variables at Cerfacs
if atCerfacs:
    from . import atmosphere_derived_variables

# Load some variable at CNRM
if atCNRM:
    from . import cnrm_derived_variables
