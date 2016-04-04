"""
This module declares locations for searching data for IGCM outputs produced by libIGCM for all frequencies, and where the data is
at IPSL and on Ciclad

Example for an IGCM_OUT_interm1 dataset declaration ::

 >>> tas1pc=ds(project='IGCM_OUT_interm1', model='IPSLCM6', experiment='piControl', variable='tas', frequency='monthly', period='1860-1861')


"""

import os
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef
from climaf.site_settings import atTGCC, onCiclad, onSpip

# Rajouter login et disk (ou filesystem) = scratch/store/work

# !! Old names for NEMO, CMIP5 names for LMDz


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


p=cproject("IGCM_OUT_altern1", "clim_period", "model", "status", "simulation", "variable", "frequency", "experiment", "OUT", "DIR", "login", "period", "root", ensemble=["model","simulation"], separator="%")

cdef('root',        root,         project='IGCM_OUT_altern1')
cdef('clim_period', '????_????',  project='IGCM_OUT_altern1')
cdef('model',       '*',          project='IGCM_OUT_altern1')
cdef('status',      '*',          project='IGCM_OUT_altern1')
cdef('simulation',  '*',          project='IGCM_OUT_altern1')
cdef('variable',    '*',          project='IGCM_OUT_altern1')
cdef('frequency',   'monthly',    project='IGCM_OUT_altern1')
cdef('experiment',  '*',          project='IGCM_OUT_altern1')
cdef('OUT',         '*',          project='IGCM_OUT_altern1')
cdef('DIR',         '*',          project='IGCM_OUT_altern1')
cdef('login',       '*',          project='IGCM_OUT_altern1')
cdef('period',      '0001-3000',  project='IGCM_OUT_altern1')
#cdef('SpaceName',   '*',          project='IGCM_OUT')


# Frequency alias
cfreqs('IGCM_OUT_altern1', {'monthly':'1M' , 'daily':'1D' , 'seasonal':'SE', 'annual_cycle':'SE'})

urls_IGCM_OUT_altern1=[
              "${root}/${login}/IGCM_OUT/${model}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/*/${simulation}_YYYYMMDD_YYYYMMDD_${frequency}_${variable}.nc",
              "${root}/${login}/IGCM_OUT/${model}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/${frequency}/${simulation}_${frequency}_${clim_period}_1M_${variable}.nc",
              "${root}/${login}/IGCM_OUT/${model}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/SE_50Y/${simulation}_${frequency}_${clim_period}_1M_${variable}.nc"
              ]

# Next command will lead to explore all directories in 'urls_IGCM_OUT_altern1'
# for searching data for a CliMAF dataset (by function ds) except if 
# a more specific dataloc entry matches the arguments to 'ds'
dataloc(project="IGCM_OUT_altern1", organization="generic", url=urls_IGCM_OUT_altern1)

# OCE
calias("IGCM_OUT_altern1", 'tos'     ,'sosstsst' , offset=273.15   ,filenameVar='grid_T')
calias("IGCM_OUT_altern1", 'sos'     ,'sosaline'                   ,filenameVar='grid_T')
calias("IGCM_OUT_altern1", 'to'      ,'thetao'   , offset=273.15   ,filenameVar='grid_T')
calias("IGCM_OUT_altern1", 'so'      ,'vosaline'                   ,filenameVar='grid_T')
calias("IGCM_OUT_altern1", 'zos'     ,'sossheig'                   ,filenameVar='grid_T')
calias("IGCM_OUT_altern1", 'mlotst'  ,'somxl010'                   ,filenameVar='grid_T')

# ICE
calias("IGCM_OUT_altern1", 'sic',    'soicecov',   scale=100 ,filenameVar="grid_T") 

# ATM general variables
calias("IGCM_OUT_altern1", 'pr'      ,'pr'  ,filenameVar='histmth')
calias("IGCM_OUT_altern1", 'prw'     ,'prw'     ,filenameVar='histmth')
calias("IGCM_OUT_altern1", 'psl'     ,'psl'     ,filenameVar='histmth')
calias("IGCM_OUT_altern1", 'tas'     ,'tas'     ,filenameVar='histmth')
calias("IGCM_OUT_altern1", 'huss'    ,'q2m'     ,filenameVar='histmth')
calias("IGCM_OUT_altern1", 'uas'     ,'u10m'    ,filenameVar='histmth')
calias("IGCM_OUT_altern1", 'vas'     ,'v10m'    ,filenameVar='histmth')
calias("IGCM_OUT_altern1", 'sfcWind' ,'wind10m' ,filenameVar='histmth')


# 3D Variables
calias("IGCM_OUT_altern1", 'ta'   ,'ta'    ,filenameVar='histmthNMC')
calias("IGCM_OUT_altern1", 'ua'   ,'ua'    ,filenameVar='histmthNMC')
calias("IGCM_OUT_altern1", 'va'   ,'va'    ,filenameVar='histmthNMC')
calias("IGCM_OUT_altern1", 'zg'   ,'zg'    ,filenameVar='histmthNMC')
calias("IGCM_OUT_altern1", 'hus'  ,'hus'   ,filenameVar='histmthNMC')


# -> Turbulent fluxes
calias("IGCM_OUT_altern1", 'hfls'   ,'flat' , scale=-1 ,filenameVar='histmth')
calias("IGCM_OUT_altern1", 'hfss'   ,'sens' , scale=-1 ,filenameVar='histmth')
calias("IGCM_OUT_altern1", 'tauu'   ,'taux'  ,filenameVar='histmth')
calias("IGCM_OUT_altern1", 'tauv'   ,'tauy'  ,filenameVar='histmth')

# -> Clouds
calias("IGCM_OUT_altern1", 'clt'   ,'cldt'  , scale=100, filenameVar='histmth')
calias("IGCM_OUT_altern1", 'cldl'  ,'cldl'  , scale=100, filenameVar='histmth')
calias("IGCM_OUT_altern1", 'cldm'  ,'cldm'  , scale=100, filenameVar='histmth')
calias("IGCM_OUT_altern1", 'cldh'  ,'cldh'  , scale=100, filenameVar='histmth')

# -> Clouds radiative forcing
calias("IGCM_OUT_altern1", 'rlwcrf'   ,''  ,filenameVar='histmth')
calias("IGCM_OUT_altern1", 'rswcrf'   ,''  ,filenameVar='histmth')

# -> Radiative up at TOA
calias("IGCM_OUT_altern1", 'rlut'   ,'topl'        ,filenameVar='histmth')
calias("IGCM_OUT_altern1", 'rsut'   ,'SWupTOA'     ,filenameVar='histmth')
calias("IGCM_OUT_altern1", 'rlutcs' ,'topl0'       ,filenameVar='histmth')
calias("IGCM_OUT_altern1", 'rsutcs' ,'SWupTOAclr'  ,filenameVar='histmth')

# -> Radiative down at TOA
calias("IGCM_OUT_altern1", 'rsdt'   ,'SWdnTOA'     ,filenameVar='histmth')

# -> Radiative up at Surface
calias("IGCM_OUT_altern1", 'rlus'   ,'LWupSFC'  ,filenameVar='histmth')
calias("IGCM_OUT_altern1", 'rsus'   ,'SWupSFC'  ,filenameVar='histmth')
calias("IGCM_OUT_altern1", 'rsuscs' ,'SWupSFCclr'  ,filenameVar='histmth')
calias("IGCM_OUT_altern1", 'rluscs' ,'LWupSFCclr'  ,filenameVar='histmth')

# -> Radiative down at Surface
calias("IGCM_OUT_altern1", 'rlds'   ,'LWdnSFC'  ,filenameVar='histmth')
calias("IGCM_OUT_altern1", 'rsds'   ,'SWdnSFC'  ,filenameVar='histmth')
calias("IGCM_OUT_altern1", 'rldscs' ,'LWdnSFCclr'  ,filenameVar='histmth')
calias("IGCM_OUT_altern1", 'rsdscs' ,'SWdnSFCclr'  ,filenameVar='histmth')


