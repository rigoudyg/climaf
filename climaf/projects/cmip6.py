"""
This module declares locations for searching data for CMIP6 outputs produced by 
libIGCM or Eclis for all frequencies.

Contact: jerome.servonnat@lsce.ipsl.fr, senesi@meteo.fr

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
   root="/ccc/work/cont003/cmip6/cmip6"
if atCNRM:
   # Declare a list of root directories for IPSL data at TGCC
   root="/cnrm/cmip"

if root:
  ## -- Declare a 'CMIP5_bis' CliMAF project (a replicate of the CMIP5 project)
  ## ---------------------------------------------------------------------------- >
  cproject('CMIP6', 'root', 'model', 'institute', 'mip', 'table', 'experiment', 'realization', 'grid', 'version', ensemble=['model','realization'],separator='%')
  ## --> systematic arguments = simulation, frequency, variable
  ## -- Set the aliases for the frequency
  ## -- Set default values
  cdef('root'         , root          , project='CMIP6')
  cdef('institute'    , '*'           , project='CMIP6')
  cdef('mip'          , '*'           , project='CMIP6')
  #cdef('table'        , '*'           , project='CMIP6') # impossible, because of ambiguities
  cdef('grid'         , 'g*'          , project='CMIP6')
  if atCNRM:
      cdef('realization'  , 'r1i1p1f2'    , project='CMIP6')
  else:
      cdef('realization'  , 'r1i1p1f1'    , project='CMIP6')
  cdef('experiment'  , 'historical'   , project='CMIP6')
  cdef('version'     , 'latest'       , project='CMIP6')


  ## -- Define the patterns
  base_pattern="${root}/CMIP6/${mip}/${institute}/${model}/${experiment}/${realization}/${table}/${variable}/${grid}/${version}/${variable}_${table}_${model}_${experiment}_${realization}_${grid}_"
  patterns=[]
  for date_format in [ "YYYY-YYYY" ,"YYYYMM-YYYYMM" , "YYYYMMDD-YYYYMMDD" , "YYYYMMDDHHMM-YYYYMMDDHHMM" ] :
      patterns.append(base_pattern + date_format + ".nc")

  ## -- call the dataloc CliMAF function
  dataloc(project='CMIP6', organization='generic', url=patterns)

  calias('CMIP6', 'tos', offset=273.15)
  calias('CMIP6', 'thetao', offset=273.15)
  calias('CMIP6', 'sic', 'siconc')
  calias('CMIP6', 'sit', 'sithick')
  calias('CMIP6', 'wfo', 'wfonocorr')
  calias('CMIP6', 'sivolu', 'sivol')
  calias('CMIP6', 'NO3', 'no3')
  calias('CMIP6', 'PO4', 'po4')
  calias('CMIP6', 'Si', 'si')
  calias('CMIP6', 'O2', 'o2')




