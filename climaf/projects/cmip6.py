"""
This module declares locations for searching data for IPSL CMIP6 outputs produced by libIGCM for all frequencies,
on Ciclad.

Contact: jerome.servonnat@lsce.ipsl.fr

"""

import os
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, crealms, cdef
from climaf.site_settings import atTGCC, onCiclad, onSpip



root = None
login= None
if atTGCC:
   # Declare a list of root directories for IPSL data at TGCC
   root="/ccc/work/cont003/cmip6/cmip6"
if onCiclad :
   # Declare a list of root directories for CMIP5 data on IPSL's Ciclad file system
   root="/ccc/work/cont003/cmip6/cmip6"

if root:
  ## -- Declare a 'CMIP5_bis' CliMAF project (a replicate of the CMIP5 project)
  ## ---------------------------------------------------------------------------- >
  cproject('CMIP6', ('frequency','monthly'), 'root', 'model', 'institute', 'table', 'experiment', 'realization', 'grid', 'version', ensemble=['model','realization'],separator='%')
  ## --> systematic arguments = simulation, frequency, variable
  ## -- Set the aliases for the frequency
  cfreqs('CMIP6', {'monthly':'mon', 'yearly':'yr', 'daily':'day'})
  ## -- Set default values
  cdef('root'         , root          , project='CMIP6')
  cdef('institute'    , '*'           , project='CMIP6')
  cdef('grid'         , 'gr'          , project='CMIP6')
  cdef('realization'  , 'r1i1p1f1'    , project='CMIP6')
  cdef('frequency'   , 'monthly'      , project='CMIP6')
  cdef('experiment'  , 'historical'   , project='CMIP6')
  cdef('version'     , 'latest'       , project='CMIP6')


  ## -- Define the pattern
  pattern=["${root}/CMIP6/CMIP/${institute}/${model}/${experiment}/${realization}/${table}/${variable}/${grid}/${version}/${variable}_${table}_${model}_${experiment}_${realization}_${grid}_YYYYMM-YYYYMM.nc", 
           "${root}/CMIP6/CMIP/${institute}/${model}/${experiment}/${realization}/${table}/${variable}/${grid}/${version}/${variable}_${table}_${model}_${experiment}_${realization}_${grid}_YYYYMMDD-YYYYMMDD.nc"]

  ## --> Note that the YYYYMM-YYYYMM string means that the period is described in the filename and that CliMAF can
  ## --> perform period selection among the files it found in the directory (can be YYYY, YYYYMM, YYYYMMDD).
  ## --> You can use an argument like ${years} instead if you just want to do string matching (no smart period selection)
  #
  ## -- call the dataloc CliMAF function
  dataloc(project='CMIP6', organization='generic', url=pattern)

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




