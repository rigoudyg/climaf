#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module declares locations for searching data for CMIP6 outputs produced by 
libIGCM or Eclis for all frequencies.

Attributes for CMIP6 datasets are : model, experiment, table, realization, grid, version, institute, mip, root

Syntax for these attributes is described in `the CMIP6 DRS document <https://goo.gl/v1drZl>`_

Example for a CMIP6 dataset declaration ::

 >>> tas1pc=ds(project='CMIP6', model='CNRM-CM6-1', experiment='1pctCO2', variable='tas', table='Amon', realization='r3i1p1f2', period='1860-1861')



"""

import os
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef, cvalid
from climaf.site_settings import atTGCC, onCiclad, onSpip, atCNRM

root = None
if atTGCC:
    # Declare a list of root directories for IPSL data at TGCC
    root = "/ccc/work/cont003/cmip6/cmip6"
if onCiclad:
    # Declare a list of root directories for CMIP5 data on IPSL's Ciclad file system
    root = "/bdd"
    # root="/ccc/work/cont003/cmip6/cmip6"
if atCNRM:
    # Declare a list of root directories for IPSL data at TGCC
    root = "/cnrm/cmip"

#if root:
if True :
  ## -- Declare a 'CMIP6 CliMAF project 
  ## ------------------------------------ >
  cproject('CMIP6', 'root', 'model', 'institute', 'mip', 'table', 'experiment', 'realization',
           'grid', 'version', ensemble=['model','realization'], separator='%')

  ## -- Declare a CMIP6 'extent' CliMAF project = extracts a period covering historical and a scenario
  ## ------------------------------------ >
  cproject('CMIP6_extent', 'root', 'model', 'institute', 'mip', 'table', 'experiment', 'extent_experiment', 'realization',
           'grid', 'version', ensemble=['model','realization'], separator='%')


  for project in ['CMIP6', 'CMIP6_extent']:
      ## --> systematic arguments = simulation, frequency, variable
      ## -- Set the aliases for the frequency
      ## -- Set default values
      cdef('root'         , root          , project=project)
      cdef('institute'    , '*'           , project=project)
      cdef('model'        , '*'           , project=project)
      cdef('mip'          , '*'           , project=project)
      #cdef('table'        , '*'           , project='CMIP6') # impossible, because of ambiguities
      cdef('grid'         , 'g*'          , project=project)
      cvalid('grid'         , [ "gr", "gn", "gr1", "gr2" ] , project=project)
      cdef('realization'  , 'r1i1p1f*'    , project=project)
      cdef('experiment'  , 'historical'   , project=project)
      cdef('version'     , 'latest'       , project=project)
      cdef('table'        , '*'           , project=project)
      #
      calias(project, 'tos', offset=273.15)
      calias(project, 'thetao', offset=273.15)
      calias(project, 'sivolu', 'sivol')
      calias(project, 'sic', 'siconc')
      calias(project, 'sit', 'sithick')
      calias(project, 'NO3', 'no3')
      calias(project, 'PO4', 'po4')
      calias(project, 'Si', 'si')
      calias(project, 'O2', 'o2')

  cdef('extent_experiment', 'ssp585'      , project='CMIP6_extent')


  # -------------
  ## -- Define the patterns
  base_pattern1="${root}/CMIP6/${mip}/${institute}/${model}/${experiment}/${realization}/${table}/"
  base_pattern1+="${variable}/${grid}/${version}/${variable}_${table}_${model}_${experiment}_${realization}_${grid}"
  patterns1=[base_pattern1 + "_${PERIOD}" + ".nc", base_pattern1 + ".nc"]

  base_pattern2="${root}/CMIP6/${mip}/${institute}/${model}/${extent_experiment}/${realization}/${table}/"
  base_pattern2+="${variable}/${grid}/${version}/${variable}_${table}_${model}_${extent_experiment}_${realization}_${grid}"
  patterns2=[base_pattern2 + "_${PERIOD}" + ".nc"]

  ## -- call the dataloc CliMAF function
  #dataloc(project='CMIP6', organization='generic', url=patterns)
  ## -- CMIP6
  dataloc(project='CMIP6', organization='generic', url=patterns1)
  #dataloc(project='CMIP6', organization='generic', url=patternf)
  ## -- CMIP6_extent
  dataloc(project='CMIP6_extent', organization='generic', url=patterns1)
  dataloc(project='CMIP6_extent', organization='generic', url=patterns2)






