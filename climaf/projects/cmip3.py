#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module declares locations for searching data for CMIP3 outputs on e.g. Ciclad

Attributes for CMIP3 datasets are : model, experiment, realm, frequency, realization, root

No unit conversion nor variable is renaming performed, yet

Example for a CMIP3 dataset declaration ::

 >>> ps=ds(project='CMIP3', model='ncar_ccsm3', experiment='sresa1b', variable='ps', realm='atm', realization='run1', period='*')

>>> d=ds(project="CMIP3",variable="*",model="*")
>>> d.explore('choices')

"""

from __future__ import print_function, division, unicode_literals, absolute_import

from env.environment import *
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef
from env.site_settings import atTGCC, onCiclad, onSpip, atCNRM

root = None
if onCiclad:
    # Declare a root directory for CMIP3 data on IPSL's Ciclad file system
    root = "/bdd/CMIP3"

if atCNRM:
    pass

if root:
    # -- Declare a CMIP3 CliMAF project
    # ------------------------------------ >
    cproject('CMIP3', 'root', 'model', 'realm', 'experiment', 'realization', 'frequency',
             ensemble=['model', 'realization'], separator='%')

    # -- Define the pattern for CMIP3 data
    pattern1 = '${root}/${experiment}/${realm}/${frequency}/${variable}/${model}/${realization}/'
    pattern1 += '${variable}_*.nc'

    # -- call the dataloc CliMAF function
    dataloc(project='CMIP3', organization='generic', url=pattern1)

    # -- Make the alias and default values for both projects
    for project in ['CMIP3']:
        # calias(project, 'tos', offset=273.15)

        cdef('root', root, project=project)
        cdef('realm', '*', project=project)
        cdef('realization', '*', project=project)
        cdef('experiment', 'sresa1b', project=project)
        cdef('frequency', 'mo', project=project)
        cdef('period', '*', project=project)

        cfreqs(project, {'monthly': 'mo', })
