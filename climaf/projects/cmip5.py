#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module declares locations for searching data for CMIP5 outputs produced by
libIGCM or Eclis for all frequencies.

Attributes for CMIP5 datasets are: model, experiment, table, realization, grid, version, institute, mip, root

Syntax for these attributes is described in `the CMIP5 DRS document
  <http://cmip-pcmdi.llnl.gov/cmip5/docs/cmip5_data_reference_syntax.pdf>`

Example for a CMIP5 dataset declaration:

 >>> tas1pc = ds(project='CMIP5', model='CNRM-CM6-1', experiment='1pctCO2', variable='tas', table='Amon',
 ...             realization='r3i1p1f2', period='1860-1861')

"""

from __future__ import print_function, division, unicode_literals, absolute_import

import os

from env.environment import *
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef
from env.site_settings import atTGCC, onCiclad, onSpip, atCNRM

root = None
if onCiclad:
    # Declare a list of root directories for CMIP5 data on IPSL's Ciclad file system
    root = "/bdd"
if atCNRM:
    # Declare a list of root directories for IPSL data at TGCC
    root = "/cnrm/cmip/cnrm/ESG"

# if root:
if True:
    # -- Declare a CMIP5 CliMAF project
    # ------------------------------------ >
    cproject('CMIP5', 'root', 'model', 'table', 'experiment', 'realization', 'frequency', 'realm',
             'version', ensemble=['model', 'realization'], separator='%')
    # -- Declare a CMIP5 'extent' CliMAF project = extracts a period covering historical and a scenario
    # ------------------------------------ >
    cproject('CMIP5_extent', 'root', 'model', 'table', 'experiment', 'extent_experiment', 'realization', 'frequency',
             'realm',
             'version', 'extent_version', ensemble=['model', 'realization'], separator='%')

    # -- Define the pattern for CMIP5
    if atCNRM:
        pattern1 = '${root}/CMIP5/output*/*/${model}/${experiment}/${frequency}/${realm}/${table}/' \
                   '${realization}/${version}/${variable}/'
    else:
        pattern1 = '${root}/CMIP5/output/*/${model}/${experiment}/${frequency}/${realm}/${table}/' \
                   '${realization}/${version}/${variable}/'

    # a pattern for fixed fields
    patternf = pattern1 + '${variable}_${table}_${model}_${experiment}_r0i0p0.nc'
    patternf=patternf.replace("/${realization}","/r0i0p0").replace("/${version}","/latest")
    patternf=patternf.replace("/${frequency}","/fx").replace("/${table}","/fx")
    # On Ciclad, some fixed fields don't have the last (per-variable) directories level
    patternf2=patternf.replace("/${variable}/","/")

    # The pattern for fields with a period
    pattern1 += '${variable}_${table}_${model}_${experiment}_${realization}_${PERIOD}.nc'

    # -- And the additionnal pattern for extent
    pattern2 = '${root}/CMIP5/output*/*/${model}/${extent_experiment}/${frequency}/${realm}/${table}/${realization}/' \
               '${extent_version}/${variable}/'
    pattern2 += '${variable}_${table}_${model}_${extent_experiment}_${realization}_${PERIOD}.nc'

    # -- call the dataloc CliMAF function
    # -- CMIP5
    dataloc(project='CMIP5', organization='generic', url=pattern1)
    dataloc(project='CMIP5', organization='generic', url=patternf)
    dataloc(project='CMIP5', organization='generic', url=patternf2)
    # -- CMIP5_extent
    dataloc(project='CMIP5_extent', organization='generic', url=pattern1)
    dataloc(project='CMIP5_extent', organization='generic', url=pattern2)

    # -- Make the alias and default values for both projects
    for project in ['CMIP5', 'CMIP5_extent']:
        # calias(project, 'tos', offset=273.15)
        # calias(project, 'thetao', offset=273.15)
        # calias(project, 'sivolu', 'sivol')
        # calias(project, 'sic', 'siconc')
        # calias(project, 'sit', 'sithick')
        calias(project, 'NO3', 'no3')
        calias(project, 'PO4', 'po4')
        calias(project, 'Si', 'si')
        calias(project, 'O2', 'o2')

        cdef('root', root, project=project)
        # cdef('institute'   , '*'          , project=project)
        cdef('table', '*', project=project)  # impossible, because of ambiguities
        cdef('realm', '*', project=project)
        cdef('realization', 'r1i1p1', project=project)
        cdef('experiment', 'historical', project=project)
        if atCNRM:
            cdef('version', '*', project=project)
        else:
            cdef('version', 'latest', project=project)
        cdef('frequency', '*', project=project)
    cdef('extent_experiment', 'rcp85', project='CMIP5_extent')

    # -- Declare a CMIP5-Adjust CliMAF project: bias corrected CMIP5 simulations
    # ------------------------------------ >
    pattern = '${root}/CMIP5-Adjust/bias-adjusted-output/*/${model}/${experiment}/${frequency}/${realm}/${table}/' \
              '${realization}/${gr}/${bias_correction}/${version}/${variable}/' \
              '${variable}_${table}_${model}_${experiment}_${realization}_${gr}_${bias_correction}_${PERIOD}.nc'
    cproject('CMIP5-Adjust', 'root', 'model', 'experiment', 'bias_correction', 'frequency', 'table', 'gr', 'realm',
             'realization', 'experiment', 'version', ensemble=['model', 'realization'], separator='%')
    dataloc(project='CMIP5-Adjust', url=pattern)

    for var in ['tas', 'tasmax', 'tasmin', 'pr', 'rsds', 'sfcWind']:
        calias('CMIP5-Adjust', var, var + 'Adjust')

    cdef('root', root, project='CMIP5-Adjust')
    # cdef('institute'      , '*'           , project='CMIP5-Adjust')
    cdef('table', '*', project='CMIP5-Adjust')  # impossible, because of ambiguities
    cdef('realm', '*', project='CMIP5-Adjust')  # impossible, because of ambiguities
    cdef('realization', 'r1i1p1', project='CMIP5-Adjust')
    cdef('experiment', 'rcp85', project='CMIP5-Adjust')
    cdef('version', 'latest', project='CMIP5-Adjust')
    cdef('gr', '*', project='CMIP5-Adjust')
    cdef('bias_correction', '*', project='CMIP5-Adjust')
    cdef('frequency', '*', project='CMIP5-Adjust')

    for project in ['CMIP5', 'CMIP5_extent', 'CMIP5-Adjust']:
        cfreqs(project, {'daily': 'day', 'monthly': 'mon', 'yearly': 'yr'})
