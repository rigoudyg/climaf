#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module declares locations for searching data for CORDEX, CORDEX_extent and CORDEX-Adjust outputs on Ciclad-CLIMERI

Attributes are :
- CORDEX: 'model','CORDEX_domain', 'model_version', 'frequency', 'driving_model',
         'realization', 'experiment', 'version', 'institute', ensemble=['model', 'driving_model', 'realization']
- CORDEX_extent: 'model','CORDEX_domain', 'model_version', 'frequency', 'driving_model',
         'realization', 'experiment', 'extent_experiment', 'version', 'institute', ensemble=['model','driving_model',
         'realization']
- CORDEX-Adjust: 'model','CORDEX_domain', 'bias_correction', 'frequency', 'driving_model',
         'realization', 'experiment', 'version', 'institute', ensemble=['model', 'driving_model', 'realization']


"""

import os
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef
from climaf.site_settings import atTGCC, onCiclad, onSpip, atCNRM

root = None
if onCiclad:
    root = "/prodigfs/project"
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

    # -- CORDEX
    cproject('CORDEX', 'root', 'model', 'CORDEX_domain', 'model_version', 'frequency', 'driving_model',
             'realization', 'experiment', 'version', 'institute', ensemble=['model', 'driving_model', 'realization'],
             separator='%')
    dataloc(project='CORDEX', url=[pattern1])
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

    # BCCORDEX
    project='BCCORDEX'
    #
    #/bdd/BCCORDEX/prAdjust/EOBS/prAdjust_EUR-11_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_MPI-CSC-REMO2009_v1-LSCE-IPSL-CDFt-EOBS10-1971-2005_day_20910101-20951231.nc
    pattern = '/bdd/BCCORDEX/${variable}/${correction_reference}/${variable}_${CORDEX_domain}_${GCM}_${experiment}_${realization}_${RCM}_${bias_correction}_${frequency}_${period}.nc'
    cproject('BCCORDEX', 'GCM', 'RCM', 'CORDEX_domain', 'bias_correction', 'correction_reference',
             'frequency', 
             'realization', 'experiment', ensemble=['GCM', 'RCM', 'realization'],
             separator='%')
    dataloc(project='BCCORDEX', url=pattern)
    cdef('bias_correction', '*', project='BCCORDEX')
    cdef('correction_reference', '*', project='BCCORDEX')
    cdef('experiment', 'rcp85', project='BCCORDEX')
    #
    cfreqs(project, {'daily': 'day'})
    #    cdef('version', 'latest', project=project)
    project='BCCORDEX'
    cdef('realization', 'r1i1p1', project=project)
    cdef('frequency', '*', project=project)
    cdef('GCM', '*', project=project)
    cdef('CORDEX_domain', '*', project=project)
    cdef('RCM', '*', project=project)
    # -- Overwrite root only for CORDEX-Adjust
    for var in ['tas', 'tasmax', 'tasmin', 'pr', 'rsds', 'sfcWind']:
        calias('BCCORDEX', var, var + 'Adjust')

