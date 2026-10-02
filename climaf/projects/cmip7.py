#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module declares locations for searching data for CMIP7 outputs organized according to CMIP7 DRS

Attributes for CMIP7 datasets are: root, mip, institute, model, experiment, realization, domain, frequency, branding_suffix, grid, version


Example for a CMIP7 dataset declaration ::

 >>> taspiC=ds(project='CMIP7', model='CNRM-ESM2-1e', experiment='piControl', variable='tas',
 ...           branding_suffix='tavg-h2m-hxy-u', frequency='6hr', realization='r1i1p1f1', period='1860-1861')



"""

from __future__ import print_function, division, unicode_literals, absolute_import

from env.site_settings import atTGCC, onCiclad, onSpirit, onSpip, atCNRM
from env.environment import *
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef

root = None
if atTGCC:
    # Declare a list of root directories for IPSL data at TGCC
    root = "/ccc/work/cont003/cmip6/cmip6"
if onCiclad or onSpirit:
    # Declare a list of root directories for CMIP7 data on IPSL's meso center
    root = "/bdd"
    # root="/ccc/work/cont003/cmip6/cmip6"
if atCNRM:
    # Declare a list of root directories for CMIP7 data at CNRM
    root = "/cnrm/cmip7/cmip7"

# a dict translating CliMAF facets to CMIP7 facets (those known by intake)
translate_facet = {
    'mip': 'activity_id',
    'institute': 'institution_id',
    'model': 'source_id',
    'experiment': 'experiment_id',
    'realization': 'member_id',
    'frequency': None,
    'branding_suffix': None,
    'grid': 'grid_label',
    'domain': "region",
    'variable': 'variable_id',
    'simulation': None,
    'root': None,
}

period_pattern = "*_${PERIOD}.nc"

if True:
    # -- Declare a 'CMIP7 CliMAF project
    # ------------------------------------ >
    cproject('CMIP7', 'root', 'mip', 'institute', 'model',
             'experiment', 'realization', 'domain', 'frequency', 'branding_suffix', 'grid', 'version',
             ensemble=['model', 'realization'], separator='%',
             translate_facet=translate_facet, period_pattern=period_pattern)

    for project in ['CMIP7', ]:
       # --> systematic arguments = simulation, frequency, variable
       # -- Set the aliases for the frequency
       # -- Set default values
       cdef('root', root, project=project)
       cdef('mip', '*', project=project)
       cdef('institute', '*', project=project)
       cdef('model', '*', project=project)
       cdef('experiment', 'historical', project=project)
       cdef('realization', 'r1i1p1f*', project=project)
       cdef('domain', 'glb', project=project)
       cdef('branding_suffix', '*', project=project)
       cdef('grid', 'g*', project=project)
       cdef('version', 'latest', project=project)
       #
       calias(project, 'tos', offset=273.15, units="K")
       calias(project, 'thetao', offset=273.15, units="K")

    # ------------
    # -- Define the patterns
    base_pattern = "${root}/MIP-DRS7/CMIP7/${mip}/${institute}/${model}/${experiment}/${realization}/${domain}/"
    base_pattern += "${frequency}/${variable}/${branding_suffix}/${grid}/${version}/"
    base_pattern += "${variable}_${branding_suffix}_${frequency}_${domain}_${grid}_${model}_${experiment}_${realization}"
    patterns = [base_pattern + "_${PERIOD}" + ".nc", base_pattern + ".nc"]

    # -- call the dataloc CliMAF function
    dataloc(project='CMIP7', organization='generic', url=patterns)
