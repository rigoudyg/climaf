#!/usr/bin/python
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
from climaf.classes import cproject, calias, cfreqs, cdef
from climaf.site_settings import atTGCC, onCiclad, onSpip, atCNRM


root = None
if atTGCC:
   # Declare a list of root directories for IPSL data at TGCC
   root="/ccc/work/cont003/cmip6/cmip6"
if onCiclad :
   # Declare a list of root directories for CMIP5 data on IPSL's Ciclad file system
   root="/bdd"
   #root="/ccc/work/cont003/cmip6/cmip6"
if atCNRM:
   # Declare a list of root directories for IPSL data at TGCC
   root="/cnrm/cmip"

if root:
  ## -- Declare a 'CMIP6 CliMAF project
  ## ------------------------------------ >
  cproject('CMIP6', 'root', 'model', 'institute', 'mip', 'table', 'experiment', 'realization',
           'grid', 'version', ensemble=['model','realization'],separator='%')
  ## --> systematic arguments = simulation, frequency, variable
  ## -- Set the aliases for the frequency
  ## -- Set default values
  cdef('root'         , root          , project='CMIP6')
  cdef('institute'    , '*'           , project='CMIP6')
  cdef('model'        , '*'           , project='CMIP6')
  cdef('mip'          , '*'           , project='CMIP6')
  #cdef('table'        , '*'           , project='CMIP6') # impossible, because of ambiguities
  cdef('grid'         , 'g*'          , project='CMIP6')
  cdef('realization'  , 'r1i1p1f*'    , project='CMIP6')
  cdef('experiment'  , 'historical'   , project='CMIP6')
  cdef('version'     , 'latest'       , project='CMIP6')
  cdef('table'        , '*'           , project='CMIP6')


  ## -- Define the patterns
  base_pattern="${root}/CMIP6/${mip}/${institute}/${model}/${experiment}/${realization}/${table}/"
  base_pattern+="${variable}/${grid}/${version}/${variable}_${table}_${model}_${experiment}_${realization}_${grid}"
  patterns=[base_pattern + "_${PERIOD}" + ".nc", base_pattern + ".nc"]

  ## -- call the dataloc CliMAF function
  dataloc(project='CMIP6', organization='generic', url=patterns)

  calias('CMIP6', 'tos', offset=273.15)
  calias('CMIP6', 'thetao', offset=273.15)
  calias('CMIP6', 'sivolu', 'sivol')
  calias('CMIP6', 'sic', 'siconc')
  calias('CMIP6', 'sit', 'sithick')
  calias('CMIP6', 'NO3', 'no3')
  calias('CMIP6', 'PO4', 'po4')
  calias('CMIP6', 'Si', 'si')
  calias('CMIP6', 'O2', 'o2')




