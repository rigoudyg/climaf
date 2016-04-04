"""
This module declares locations for searching data for IGCM outputs produced by libIGCM for all frequencies, and where the data is
at IPSL and on Ciclad

Example for an IGCM_OUT_altern2 dataset declaration ::

 >>> tas1pc=ds(project='IGCM_OUT_altern2', model='IPSLCM6', experiment='piControl', variable='tas', frequency='monthly', period='1860-1861')


"""

import os
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef
from climaf.site_settings import atTGCC, onCiclad, onSpip

# Rajouter login et disk (ou filesystem) = scratch/store/work

# !!! New names for NEMO (cmip5), old names for LMDz

# ajouter realm? atmos -> ATM; ocean -> OCE
root = None
if atTGCC:
   # Declare a list of root directories for IPSL data at TGCC
   root="/ccc/store/cont003/dsm"
if onCiclad :
   # Declare a list of root directories for CMIP5 data on IPSL's Ciclad file system
   root="/data/jservon/IPSL_DATA/SIMULATIONS"
if onSpip:
   # Declare a list of root directories for IPSL data at TGCC
   root="/Users/marti/Volumes/CURIE/ccc/store/cont003/dsm"
   print 'igcm_out : declaration root sur Spip : ', root


p=cproject("IGCM_OUT_altern2", "clim_period", "model", "status", "simulation", "variable", "frequency", "experiment", "OUT", "DIR", "login", "period", "root", ensemble=["model","simulation"], separator="%")

cdef('root',        root,         project='IGCM_OUT_altern2')
cdef('clim_period', '????_????',  project='IGCM_OUT_altern2')
cdef('model',       '*',          project='IGCM_OUT_altern2')
cdef('status',      '*',          project='IGCM_OUT_altern2')
cdef('simulation',  '*',          project='IGCM_OUT_altern2')
cdef('variable',    '*',          project='IGCM_OUT_altern2')
cdef('frequency',   'monthly',    project='IGCM_OUT_altern2')
cdef('experiment',  '*',          project='IGCM_OUT_altern2')
cdef('OUT',         '*',          project='IGCM_OUT_altern2')
cdef('DIR',         '*',          project='IGCM_OUT_altern2')
cdef('login',       '*',          project='IGCM_OUT_altern2')
cdef('period',      '0001-3000',  project='IGCM_OUT_altern2')
#cdef('SpaceName',   '*',          project='IGCM_OUT')


# Frequency alias
cfreqs('IGCM_OUT_altern2', {'monthly':'1M' , 'daily':'1D' , 'seasonal':'SE', 'annual_cycle':'SE'})

urls_IGCM_OUT_altern2=[
              "${root}/${login}/IGCM_OUT/${model}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/*/${simulation}_YYYYMMDD_YYYYMMDD_${frequency}_${variable}.nc",
              "${root}/${login}/IGCM_OUT/${model}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/${frequency}/${simulation}_${frequency}_${clim_period}_1M_${variable}.nc",
              "${root}/${login}/IGCM_OUT/${model}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/SE_50Y/${simulation}_${frequency}_${clim_period}_1M_${variable}.nc"
              ]

# Next command will lead to explore all directories in 'urls_IGCM_OUT_altern2'
# for searching data for a CliMAF dataset (by function ds) except if
# a more specific dataloc entry matches the arguments to 'ds'
dataloc(project="IGCM_OUT_altern2", organization="generic", url=urls_IGCM_OUT_altern2)


# OCE
calias("IGCM_OUT_altern2", 'tos'     ,'tos'      , offset=273.15   , filenameVar='grid_T')
calias("IGCM_OUT_altern2", 'sos'     ,'sos'                        , filenameVar='grid_T')
calias("IGCM_OUT_altern2", 'to'      ,'thetao'   , offset=273.15   , filenameVar='grid_T')
calias("IGCM_OUT_altern2", 'so'      ,'so'                         , filenameVar='grid_T')
calias("IGCM_OUT_altern2", 'zos'     ,'sossheig'                   , filenameVar='grid_T')
calias("IGCM_OUT_altern2", 'mlotst'  ,'somxl010'                   , filenameVar='grid_T')

# ICE
calias("IGCM_OUT_altern2", 'sic',    'soicecov',   scale=100 ,filenameVar="grid_T") 

# ATM general variables
calias("IGCM_OUT_altern2", 'pr'      ,'precip'  ,filenameVar='histmth')
calias("IGCM_OUT_altern2", 'prw'     ,'prw'     ,filenameVar='histmth')
calias("IGCM_OUT_altern2", 'psl'     ,'slp'     ,filenameVar='histmth')
calias("IGCM_OUT_altern2", 'tas'     ,'t2m'     ,filenameVar='histmth')
calias("IGCM_OUT_altern2", 'huss'    ,'q2m'     ,filenameVar='histmth')
calias("IGCM_OUT_altern2", 'uas'     ,'u10m'    ,filenameVar='histmth')
calias("IGCM_OUT_altern2", 'vas'     ,'v10m'    ,filenameVar='histmth')
calias("IGCM_OUT_altern2", 'sfcWind' ,'wind10m' ,filenameVar='histmth')


# 3D Variables
calias("IGCM_OUT_altern2", 'ta'   ,'ta'    ,filenameVar='histmthNMC')
calias("IGCM_OUT_altern2", 'ua'   ,'ua'    ,filenameVar='histmthNMC')
calias("IGCM_OUT_altern2", 'va'   ,'va'    ,filenameVar='histmthNMC')
calias("IGCM_OUT_altern2", 'zg'   ,'zg'    ,filenameVar='histmthNMC')
calias("IGCM_OUT_altern2", 'hus'  ,'hus'   ,filenameVar='histmthNMC')


# -> Turbulent fluxes
calias("IGCM_OUT_altern2", 'hfls'   ,'flat' , scale=-1 ,filenameVar='histmth')
calias("IGCM_OUT_altern2", 'hfss'   ,'sens' , scale=-1 ,filenameVar='histmth')
calias("IGCM_OUT_altern2", 'tauu'   ,'taux'  ,filenameVar='histmth')
calias("IGCM_OUT_altern2", 'tauv'   ,'tauy'  ,filenameVar='histmth')

# -> Clouds
calias("IGCM_OUT_altern2", 'clt'   ,'cldt'  , scale=100, filenameVar='histmth')
calias("IGCM_OUT_altern2", 'cldl'  ,'cldl'  , scale=100, filenameVar='histmth')
calias("IGCM_OUT_altern2", 'cldm'  ,'cldm'  , scale=100, filenameVar='histmth')
calias("IGCM_OUT_altern2", 'cldh'  ,'cldh'  , scale=100, filenameVar='histmth')

# -> Clouds radiative forcing
calias("IGCM_OUT_altern2", 'rlwcrf'   ,''  ,filenameVar='histmth')
calias("IGCM_OUT_altern2", 'rswcrf'   ,''  ,filenameVar='histmth')

# -> Radiative up at TOA
calias("IGCM_OUT_altern2", 'rlut'   ,'topl'        ,filenameVar='histmth')
calias("IGCM_OUT_altern2", 'rsut'   ,'SWupTOA'     ,filenameVar='histmth')
calias("IGCM_OUT_altern2", 'rlutcs' ,'topl0'       ,filenameVar='histmth')
calias("IGCM_OUT_altern2", 'rsutcs' ,'SWupTOAclr'  ,filenameVar='histmth')

# -> Radiative down at TOA
calias("IGCM_OUT_altern2", 'rsdt'   ,'SWdnTOA'     ,filenameVar='histmth')

# -> Radiative up at Surface
calias("IGCM_OUT_altern2", 'rlus'   ,'LWupSFC'  ,filenameVar='histmth')
calias("IGCM_OUT_altern2", 'rsus'   ,'SWupSFC'  ,filenameVar='histmth')
calias("IGCM_OUT_altern2", 'rsuscs' ,'SWupSFCclr'  ,filenameVar='histmth')
calias("IGCM_OUT_altern2", 'rluscs' ,'LWupSFCclr'  ,filenameVar='histmth')

# -> Radiative down at Surface
calias("IGCM_OUT_altern2", 'rlds'   ,'LWdnSFC'  ,filenameVar='histmth')
calias("IGCM_OUT_altern2", 'rsds'   ,'SWdnSFC'  ,filenameVar='histmth')
calias("IGCM_OUT_altern2", 'rldscs' ,'LWdnSFCclr'  ,filenameVar='histmth')
calias("IGCM_OUT_altern2", 'rsdscs' ,'SWdnSFCclr'  ,filenameVar='histmth')


