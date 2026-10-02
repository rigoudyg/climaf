#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module declares locations for searching data for CORDEX-CMIP6 outputs on Ciclad-CLIMERI

Attributes are:
- CORDEX-CMIP6: 'model','CORDEX_domain', 'model_version', 'frequency', 'driving_model',
                'realization', 'experiment', 'version', 'institute', ensemble=['model', 'driving_model', 'realization']

"""

from __future__ import print_function, division, unicode_literals, absolute_import


from env.site_settings import atTGCC, onCiclad, onSpirit, onSpip, atCNRM
from env.environment import *
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef

root = None
if onCiclad or onSpirit:
    root = "/bdd"
# if atCNRM:
#   # Declare a list of root directories for IPSL data at TGCC
#   root="/cnrm/cmip"

if root:
    # -- Declare the various CORDEX CliMAF project
    # --------------------------------------------- >

    # -- CORDEX
    pattern = '${root}/CORDEX-CMIP6/DD/${CORDEX_domain}/${institute}/${driving_model}/${experiment}/${realization}/' \
              '${model}/${model_version}/${frequency}/${variable}/${version}/' \
              '${variable}_${CORDEX_domain}_${driving_model}_${experiment}_${realization}_${institute}_${model}_${model_version}_' \
              '${frequency}_${PERIOD}.nc'
    patternfx = '${root}/CORDEX-CMIP6/DD/${CORDEX_domain}/${institute}/${driving_model}/${experiment}/${realization}/' \
                '${model}/${model_version}/${frequency}/${variable}/${version}/' \
                '${variable}_${CORDEX_domain}_${driving_model}_${experiment}_${realization}_${institute}_${model}_${model_version}_'\
                'fx.nc'

    # a dict translating CliMAF facets to CORDEX facets (those known by intake)
    translate_facet = {
        'CORDEX_domain': 'domain',
        'realization': 'ensemble',
        'model': 'rcm_model',
        'model_version': 'rcm_version',
        'frequency': 'time_frequency',
        'simulation': None,
        'domain': None,
        'root': None,
    }

    # A pattern for finding period in filename when using intake
    # catalogs (which, at IPSL, as of 20240517, have buggy values for
    # period_start and period_end)
    period_pattern = "*_${PERIOD}.nc"

    cproject('CORDEX-CMIP6', 'root', 'model', 'CORDEX_domain', 'model_version', 'frequency', 'driving_model',
             'realization', 'experiment', 'version', 'institute', ensemble=['model', 'driving_model', 'realization'],
             translate_facet=translate_facet, period_pattern=period_pattern, separator='%')
    dataloc(project='CORDEX', url=[patternfx, pattern])
    cdef('experiment', '*', project='CORDEX')
    cdef('model_version', '*', project='CORDEX')

    for project in ['CORDEX', ]:
        cdef('version', 'latest', project=project)
        cdef('root', root, project=project)
        cdef('institute', '*', project=project)
        cdef('realization', 'r1i1p1', project=project)
        cdef('frequency', '*', project=project)
        cdef('driving_model', '*', project=project)
        cdef('CORDEX_domain', '*', project=project)
        cdef('model', '*', project=project)
