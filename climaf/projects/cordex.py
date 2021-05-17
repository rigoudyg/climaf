#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module declares locations for searching data for CORDEX, CORDEX_extent and CORDEX-Adjust outputs on Ciclad-CLIMERI

Attributes are:
- CORDEX: 'model','CORDEX_domain', 'model_version', 'frequency', 'driving_model',
         'realization', 'experiment', 'version', 'institute', ensemble=['model', 'driving_model', 'realization']
- CORDEX_extent: 'model','CORDEX_domain', 'model_version', 'frequency', 'driving_model',
         'realization', 'experiment', 'extent_experiment', 'version', 'institute', ensemble=['model','driving_model',
         'realization']
- CORDEX-Adjust: 'model','CORDEX_domain', 'bias_correction', 'frequency', 'driving_model',
         'realization', 'experiment', 'version', 'institute', ensemble=['model', 'driving_model', 'realization']


"""

from __future__ import print_function, division, unicode_literals, absolute_import

import os

from env.environment import *
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef
from env.site_settings import atTGCC, onCiclad, onSpip, atCNRM

root = None
if onCiclad:
    root = "/bdd"
# if atCNRM:
#   # Declare a list of root directories for IPSL data at TGCC
#   root="/cnrm/cmip"

if root:
    # -- Declare the various CORDEX CliMAF project
    # --------------------------------------------- >
    pattern1 = '${root}/CORDEX/output/${CORDEX_domain}/${institute}/${driving_model}/${experiment}/${realization}/' \
               '${model}/${model_version}/${frequency}/${variable}/${version}/' \
               '${variable}_${CORDEX_domain}_${driving_model}_${experiment}_${realization}_${model}_${model_version}_' \
               '${frequency}_${PERIOD}.nc'
    pattern2 = '${root}/CORDEX/output/${CORDEX_domain}/${institute}/${driving_model}/${extent_experiment}/' \
               '${realization}/${model}/${model_version}/${frequency}/${variable}/${version}/' \
               '${variable}_${CORDEX_domain}_${driving_model}_${extent_experiment}_${realization}_${model}_' \
               '${model_version}_${frequency}_${PERIOD}.nc'
    patternfx = '${root}/CORDEX/output/${CORDEX_domain}/${institute}/${driving_model}/${experiment}/${realization}/' \
                '${model}/${model_version}/${frequency}/${variable}/${version}/' \
                '${variable}_${CORDEX_domain}_${driving_model}_${experiment}_${realization}_${model}_${model_version}_'\
                'fx.nc'
    # -- CORDEX
    cproject('CORDEX', 'root', 'model', 'CORDEX_domain', 'model_version', 'frequency', 'driving_model',
             'realization', 'experiment', 'version', 'institute', ensemble=['model', 'driving_model', 'realization'],
             separator='%')
    dataloc(project='CORDEX', url=[patternfx, pattern1])
    cdef('experiment', '*', project='CORDEX')
    cdef('model_version', '*', project='CORDEX')

    # -- CORDEX extent (historical + scenario at once)
    cproject('CORDEX_extent', 'root', 'model', 'CORDEX_domain', 'model_version', 'frequency', 'driving_model',
             'realization', 'experiment', 'extent_experiment', 'version', 'institute',
             ensemble=['model', 'driving_model', 'realization'], separator='%')
    dataloc(project='CORDEX_extent', url=[pattern1])
    dataloc(project='CORDEX_extent', url=[pattern2])
    cdef('extent_experiment', 'rcp85', project='CORDEX_extent')
    cdef('experiment', 'historical', project='CORDEX_extent')
    cdef('model_version', '*', project='CORDEX_extent')

    # -- CORDEX Adjust
    pattern = '${root}/CORDEX-Adjust/bias-adjusted-output/${CORDEX_domain}/${institute}/${driving_model}/' \
              '${experiment}/${realization}/${model}/${bias_correction}/${frequency}/${variable}/${version}/' \
              '${variable}_${CORDEX_domain}_${driving_model}_${experiment}_${realization}_${model}_' \
              '${bias_correction}_${frequency}_${PERIOD}.nc'
    cproject('CORDEX-Adjust', 'root', 'model', 'CORDEX_domain', 'bias_correction', 'frequency', 'driving_model',
             'realization', 'experiment', 'version', 'institute', ensemble=['model', 'driving_model', 'realization'],
             separator='%')
    dataloc(project='CORDEX-Adjust', url=pattern)
    cdef('bias_correction', '*', project='CORDEX-Adjust')
    cdef('experiment', 'rcp85', project='CORDEX-Adjust')

    for project in ['CORDEX', 'CORDEX_extent', 'CORDEX-Adjust']:
        cfreqs(project, {'daily': 'day'})
        cdef('version', 'latest', project=project)
        cdef('root', root, project=project)
        cdef('institute', '*', project=project)
        cdef('realization', 'r1i1p1', project=project)
        cdef('frequency', '*', project=project)
        cdef('driving_model', '*', project=project)
        cdef('CORDEX_domain', '*', project=project)
        cdef('model', '*', project=project)
    # -- Overwrite root only for CORDEX-Adjust 
    cdef('root', '/prodigfs/project', project='CORDEX-Adjust')

    for var in ['tas', 'tasmax', 'tasmin', 'pr', 'rsds', 'sfcWind']:
        calias('CORDEX-Adjust', var, var + 'Adjust')
