"""
This module declares locations for searching data for IPSL CMIP6 outputs produced by libIGCM for all frequencies,
on Ciclad.

Contact: jerome.servonnat@lsce.ipsl.fr

"""

import os
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef
from climaf.site_settings import atTGCC, onCiclad, onSpip, atCNRM



root = None
login= None
if atTGCC:
   # Declare a list of root directories for IPSL data at TGCC
   root="/ccc/store/cont003/thredds"
if onCiclad :
   # Declare a list of root directories for CMIP5 data on IPSL's Ciclad file system
   root="/ccc/store/cont003/thredds"
   login="fabric"
if onSpip:
   # Declare a list of root directories for IPSL data at TGCC
   root="/Users/marti/Volumes/CURIE/ccc/store/cont003/dsm"
   print 'igcm_out : declaration root sur Spip : ', root
if atCNRM:
   # Declare a list of root directories for IPSL data at TGCC
   root="/cnrm/cmip/CMIP6"

if root:

  # -- Declare a 'CMIP' CliMAF project (a replicate of the CMIP5 project)
  # ---------------------------------------------------------------------------- >
  cproject('CMIP6', ('frequency','monthly'), 'model', 'realm', 'table', 'experiment', \
           'gr', 'root', 'version', 'mip','institute',\
           ensemble=['model','simulation'],separator='%')

  # -- Set the aliases for the frequency
  cfreqs('CMIP6', {'monthly':'mon'})
  
  # --> systematic arguments = simulation, frequency, variable
  # -- Set default values
  cdef('simulation'  , 'r1i1p1f2'     , project='CMIP6')
  cdef('experiment'  , 'historical'   , project='CMIP6')
  cdef('table'       , '*'            , project='CMIP6')
  cdef('realm'       , '*'            , project='CMIP6')
  cdef('gr'          , 'g*'           , project='CMIP6')
  cdef('root'        , '/prodigfs'    , project='CMIP6')
  cdef('version'     , 'latest'       , project='CMIP6')
  cdef('mip'         , '*'            , project='CMIP6')
  cdef('institute'   , '*'            , project='CMIP6')

  
  # -- Define the pattern
  pattern="${root}/${model}/${experiment}/${frequency}/${realm}/${table}/${simulation}/latest/${variable}/${variable}_${table}_${model}_${experiment}_${simulation}_YYYYMM-YYYYMM.nc"
  if not atCNRM :
     pattern1="${root}/*/${variable}_${table}_${model}_${experiment}_${simulation}_${gr}_YYYYMM-YYYYMM.nc"
     pattern2="${root}/${variable}_${table}_${model}_${experiment}_${simulation}_${gr}_YYYYMM-YYYYMM.nc"
     # -- call the dataloc CliMAF function
     dataloc(project='CMIP6', organization='generic', url=[pattern1,pattern2])
  else :
     cdef('root'        , root            , project='CMIP6')
     file_pattern="${variable}_${table}_${model}_${experiment}_${simulation}_${gr}_YYYYMM-YYYYMM.nc"

     # Declare final organization on Lustre /cnrm
     path_pattern="${root}/${mip}/${institute}/${model}/${experiment}/${simulation}/${table}/${variable}/${gr}/${version}/"
     # Declare temporary organization on Lustre /cnrm
     path_pattern2="${root}/${model}/*/${model}_${experiment}_${simulation}/"
     #
     dataloc(project="CMIP6",organization='generic',url=[path_pattern+file_pattern,path_pattern2+file_pattern])

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


